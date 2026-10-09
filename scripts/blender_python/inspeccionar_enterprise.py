"""Selección manual y renders de diagnóstico; nunca guarda ni modifica el .blend fuente.

En consola Blender:
  exec(compile(open(RUTA_SCRIPT, encoding='utf-8').read(), RUTA_SCRIPT, 'exec'))
  seleccionar('Captain_s_Chair_1')  # acepta también ENT-<hash del mapa>

En segundo plano:
  blender --disable-autoexec --background ESCENA --python ESTE_SCRIPT -- --salida CARPETA_NUEVA
  ... -- --salida CARPETA_NUEVA --objetos Captain_s_Chair_1 Conn
Renders Workbench grises, no validación de materiales. Cambios de color/cámara solo
en memoria del proceso; se verifica el SHA-256 fuente antes/después y no se guarda.
"""
import argparse
import hashlib
import json
import math
import sys
from pathlib import Path

import bpy
from mathutils import Vector


def sha_file(path):
    digest = hashlib.sha256()
    with Path(path).open('rb') as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b''):
            digest.update(block)
    return digest.hexdigest()


def resolve(value):
    if value in bpy.data.objects:
        return bpy.data.objects[value]
    found = [o for o in bpy.data.objects
             if 'ENT-' + hashlib.sha256(o.name.encode('utf-8')).hexdigest()[:12] == value]
    if len(found) != 1:
        raise KeyError('Nombre/ID no encontrado o ambiguo: ' + value)
    return found[0]


def descendants(obj):
    # Tabla padre/hijo construida una vez: evita obj.children O(total objetos).
    children = {}
    for o in bpy.data.objects:
        if o.parent:
            children.setdefault(o.parent.name, []).append(o)
    result, todo = [], [obj]
    while todo:
        item = todo.pop()
        result.append(item)
        todo.extend(children.get(item.name, []))
    return result


def seleccionar(nombre_o_id, incluir_descendientes=True, encuadrar=True):
    """Solo selección y encuadre UI; no renombra, mueve, oculta ni guarda."""
    target = resolve(nombre_o_id)
    objects = descendants(target) if incluir_descendientes else [target]
    bpy.ops.object.select_all(action='DESELECT')
    for obj in objects:
        if obj.name in bpy.context.view_layer.objects:
            obj.select_set(True)
    bpy.context.view_layer.objects.active = target
    framed = 0
    if encuadrar and bpy.context.window:
        for area in bpy.context.window.screen.areas:
            if area.type != 'VIEW_3D':
                continue
            region = next((r for r in area.regions if r.type == 'WINDOW'), None)
            if region:
                with bpy.context.temp_override(area=area, region=region):
                    bpy.ops.view3d.view_selected(use_all_regions=False)
                framed += 1
    print('Seleccionado:', target.name, 'objetos:', len(objects), 'vistas encuadradas:', framed)
    return [obj.name for obj in objects]


def bbox(objects):
    low, high = [math.inf] * 3, [-math.inf] * 3
    for obj in objects:
        if obj.type != 'MESH':
            continue
        for corner in obj.bound_box:
            p = obj.matrix_world @ Vector(corner)
            for k in range(3):
                low[k], high[k] = min(low[k], p[k]), max(high[k], p[k])
    if math.isinf(low[0]):
        raise RuntimeError('Selección sin geometría MESH')
    return Vector(low), Vector(high)


def render_main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--salida', type=Path, required=True)
    parser.add_argument('--objetos', nargs='*', default=[])
    parser.add_argument('--ocultar', nargs='*', default=[], help='Grupos ocultos solo en el proceso de diagnóstico')
    parser.add_argument('--aislar', action='store_true', help='Mostrar solo el grupo resaltado en cada captura')
    args = parser.parse_args(sys.argv[sys.argv.index('--') + 1:])
    root = Path(__file__).resolve().parents[2]
    output = args.salida.resolve()
    if output == root / 'assets' or root / 'assets' in output.parents:
        raise RuntimeError('No escribir en assets')
    if output.exists():
        raise FileExistsError('Elegir carpeta nueva; no se sobrescriben renders')
    source = Path(bpy.data.filepath).resolve()
    before = sha_file(source)
    output.mkdir(parents=True)
    scene = bpy.context.scene
    scene.render.engine = 'BLENDER_WORKBENCH'
    scene.render.resolution_x = 960
    scene.render.resolution_y = 720
    scene.render.resolution_percentage = 100
    scene.render.image_settings.file_format = 'PNG'
    scene.render.use_compositing = False
    scene.render.use_sequencer = False
    scene.render.film_transparent = False
    shade = scene.display.shading
    shade.light = 'STUDIO'
    shade.color_type = 'OBJECT'
    shade.show_shadows = True
    shade.show_cavity = True
    shade.cavity_type = 'BOTH'
    shade.background_type = 'WORLD'
    scene.world.color = (0.07, 0.07, 0.07)
    scene.display.render_aa = '8'
    scene.view_settings.view_transform = 'Standard'
    original_meshes = [o for o in scene.objects if o.type == 'MESH']
    for obj in original_meshes:
        obj.color = (0.62, 0.65, 0.7, 1)
    camera_data = bpy.data.cameras.new('AUDIT_CAMERA_TEMP')
    camera = bpy.data.objects.new('AUDIT_CAMERA_TEMP', camera_data)
    scene.collection.objects.link(camera)
    scene.camera = camera
    camera_data.type = 'ORTHO'
    camera_data.clip_start = 0.001
    camera_data.clip_end = 100000
    bridge = list(bpy.data.collections['model.dae'].all_objects)
    hidden_names = set()
    for value in args.ocultar:
        for obj in descendants(resolve(value)):
            if obj.type == 'MESH':
                obj.hide_render = True
                hidden_names.add(obj.name)
    low, high = bbox(bridge)
    center = (low + high) / 2
    size = high - low
    directions = {'superior': Vector((0, 0, 1)), 'frontal_eje_menos_Y': Vector((0, -1, 0.3)),
                  'lateral_eje_X': Vector((1, 0, 0.25)), 'perspectiva': Vector((1, -1.4, 1.15))}
    manifest = {'source': str(source), 'source_sha256': before, 'engine': 'BLENDER_WORKBENCH',
                'resolution': [960, 720], 'note': 'Grises/cian temporales; no prueba PBR/texturas; sin guardar escena',
                'hidden_groups': args.ocultar, 'hidden_meshes': sorted(hidden_names),
                'isolate': args.aislar, 'captures': []}

    def capture(stem, low, high, direction, highlighted=None):
        center = (low + high) / 2
        size = high - low
        camera.location = center + direction.normalized() * max(size.length, 1) * 2
        camera.rotation_euler = (center - camera.location).to_track_quat('-Z', 'Y').to_euler()
        inverse_rotation = camera.rotation_euler.to_matrix().transposed()
        corners = [inverse_rotation @ (Vector((x, y, z)) - center)
                   for x in (low.x, high.x) for y in (low.y, high.y) for z in (low.z, high.z)]
        width = max(v.x for v in corners) - min(v.x for v in corners)
        height = max(v.y for v in corners) - min(v.y for v in corners)
        camera_data.ortho_scale = max(width, height * 960 / 720) * 1.15
        scene.render.filepath = str(output / (stem + '.png'))
        bpy.ops.render.render(write_still=True)
        manifest['captures'].append({'file': stem + '.png', 'camera': list(camera.location),
                                     'ortho_scale': camera_data.ortho_scale,
                                     'highlighted': highlighted or [], 'view_vector': list(direction)})
        print('AUDIT_CAPTURE=' + stem, flush=True)

    if not args.objetos:
        for name, direction in directions.items():
            capture(name, low, high, direction)
    else:
        for value in args.objetos:
            target = resolve(value)
            members = descendants(target)
            highlighted = [o for o in members if o.type == 'MESH']
            saved_visibility = {o.name: o.hide_render for o in original_meshes}
            if args.aislar:
                visible_names = {o.name for o in highlighted}
                for obj in original_meshes:
                    obj.hide_render = obj.name not in visible_names
            for obj in highlighted:
                obj.color = (0.03, 0.9, 0.95, 1)
            # Marco local; resto permanece visible para evidenciar dependencias/contexto.
            a, b = bbox(highlighted)
            safe_name = ''.join(c if c.isalnum() or c in '-_' else '_' for c in target.name)
            capture(safe_name, a, b, directions['perspectiva'], [o.name for o in highlighted])
            for obj in highlighted:
                obj.color = (0.62, 0.65, 0.7, 1)
            for obj in original_meshes:
                obj.hide_render = saved_visibility[obj.name]
    manifest['source_hash_after'] = sha_file(source)
    if manifest['source_hash_after'] != before:
        raise RuntimeError('La fuente cambió durante el render (posible guardado externo)')
    (output / 'MANIFIESTO_CAPTURAS.json').write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding='utf-8')


if __name__ == '__main__' and '--' in sys.argv:
    render_main()
