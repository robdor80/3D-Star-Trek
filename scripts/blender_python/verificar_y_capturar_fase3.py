"""Reabre copia fase 3, verifica invariantes y crea dos capturas de diagnóstico.

No guarda escenas. Visibilidad/colores/cámara solo en memoria del proceso.
Incluye ensayos analíticos del cálculo de distancia usado en la medición.
"""
import argparse
from collections import defaultdict
import hashlib
import json
from pathlib import Path
import sys
import bpy
from mathutils import Vector

sys.path.insert(0, str(Path(__file__).resolve().parent))
from medir_transitabilidad_enterprise import fingerprint, segment_triangle, clip_triangle, sha, ORIGINAL, ROOT


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--datos', type=Path, required=True)
    parser.add_argument('--salida', type=Path, required=True)
    args = parser.parse_args(sys.argv[sys.argv.index('--')+1:])
    output = args.salida.resolve()
    if output.exists() or output == ROOT/'assets' or ROOT/'assets' in output.parents:
        raise RuntimeError('Salida nueva fuera de assets obligatoria')
    data = json.loads(args.datos.read_text(encoding='utf-8'))
    source = Path(bpy.data.filepath).resolve()
    if source == ORIGINAL.resolve() or sha(source) != data['copy_final_sha256']:
        raise RuntimeError('Cargar exactamente la copia de trabajo guardada')
    original_objects = [o for o in bpy.context.scene.objects if o.name not in data['auxiliary_objects']]
    observed = fingerprint(original_objects)
    if observed != data['initial_fingerprint'] or sha(ORIGINAL) != data['original_sha256']:
        raise RuntimeError('Cambió contenido original o importado')
    # Suelo tangente, pared penetrada, cruce interior y aproximación a arista.
    p,q,r = Vector((-3,-3,0)),Vector((3,-3,0)),Vector((0,3,0))
    assert abs(segment_triangle(Vector((0,0,.34)),Vector((0,0,1.42)),p,q,r)-.34) < 1e-6
    assert segment_triangle(Vector((0,0,-1)),Vector((0,0,1)),p,q,r) < 1e-6
    p,q,r = Vector((.2,-3,-3)),Vector((.2,3,-3)),Vector((.2,0,3))
    assert abs(segment_triangle(Vector((0,0,.34)),Vector((0,0,1.42)),p,q,r)-.2) < 1e-6
    p,q,r = Vector((0,0,0)),Vector((1,0,0)),Vector((0,1,0))
    assert abs(segment_triangle(Vector((2,0,.3)),Vector((2,0,1.3)),p,q,r)-1.04403065) < 1e-6
    assert not clip_triangle([p,q,r],Vector((2,2,2)),Vector((3,3,3)))
    references = {}
    for label in ['REF_HUMANO_H180_ESQUEMATICO','REF_CAPSULA_UE5_R034_H176']:
        obj = bpy.data.objects[label]
        points = [obj.matrix_world @ v.co for v in obj.data.vertices]
        dimensions = [max(p[k] for p in points)-min(p[k] for p in points) for k in range(3)]
        references[label] = {'location':list(obj.location),'world_dimensions':dimensions}
    assert abs(references['REF_HUMANO_H180_ESQUEMATICO']['world_dimensions'][2]-1.8)<1e-5
    assert all(abs(a-b)<1e-5 for a,b in zip(references['REF_CAPSULA_UE5_R034_H176']['world_dimensions'],(.68,.68,1.76)))
    # Conservación de shaders y bytes de imágenes empaquetadas por comparación
    # con auditoría fase 2. Fingerprint anterior cubre slots/UV, no nodos.
    baseline=json.loads((ROOT/'docs/auditorias/enterprise_bpy_v2/AUDITORIA_ENTERPRISE_DATOS.json').read_text(encoding='utf-8'))
    sys.path.insert(0,str(Path(__file__).resolve().parent))
    from auditar_enterprise import serialize_value
    current_materials={}
    for material in bpy.data.materials:
        nodes,links=[],[]
        if material.node_tree:
            for node in material.node_tree.nodes:
                image=node.image if node.type=='TEX_IMAGE' else None
                nodes.append({'name':node.name,'type':node.type,'image':image.name if image else None,
                              'inputs':{s.name:serialize_value(s.default_value) for s in node.inputs if hasattr(s,'default_value') and not s.is_linked}})
            links=[{'from_node':l.from_node.name,'from_socket':l.from_socket.name,'to_node':l.to_node.name,'to_socket':l.to_socket.name} for l in material.node_tree.links]
        current_materials[material.name]={'nodes':nodes,'links':links}
    # Los registros incluyen usuarios; comparar nodos/enlaces sin asumir nombres de claves.
    baseline_materials=baseline['materials']
    if isinstance(baseline_materials,list):
        baseline_materials={m['name']:m for m in baseline_materials}
    shader_checks=[]
    unused_not_saved=[]
    for key, record in baseline_materials.items():
        if key not in current_materials and not record['object_users'] and record['data_users']==0:
            unused_not_saved.append(key)
            continue
        current=current_materials[key]
        for field in ['nodes','links']:
            if record.get(field)!=current.get(field):
                raise RuntimeError('Shader importado cambió: '+key+'/'+field)
        shader_checks.append(key)
    packed=[]
    baseline_images=baseline['images']
    if isinstance(baseline_images,dict): baseline_images=baseline_images.values()
    for record in baseline_images:
        if record.get('source')=='FILE':
            img=bpy.data.images[record['name']]
            digests=[hashlib.sha256(p.packed_file.data).hexdigest() for p in img.packed_files]
            expected=record.get('packed_sha256')
            if expected is None or digests!=expected: raise RuntimeError('Textura empaquetada cambió o falta hash de referencia')
            packed.append({'name':img.name,'sha256':digests,'baseline_hash_compared':True})
    output.mkdir(parents=True)
    children=defaultdict(list)
    for obj in bpy.context.scene.objects:
        if obj.parent: children[obj.parent.name].append(obj)
    stack=[bpy.data.objects['group_1']]
    hidden=[]
    while stack:
        obj=stack.pop(); stack.extend(children[obj.name])
        if obj.type=='MESH': obj.hide_render=True; hidden.append(obj.name)
    for obj in original_objects:
        if obj.type=='MESH': obj.color=(.58,.62,.68,1)
    box=bpy.data.objects['VOLUMEN_CONEXION_PROPUESTO_NO_ABIERTO']
    box.hide_render=True
    # Jaula dibujada solo para capturas; nunca guardada ni exportada.
    curve=bpy.data.curves.new('DIAGNOSTICO_JAULA_TEMP','CURVE'); curve.dimensions='3D'; curve.bevel_depth=.015; curve.bevel_resolution=0
    points=[v.co.copy() for v in box.data.vertices]
    for i,a in enumerate(points):
        for b in points[i+1:]:
            if sum(abs(a[k]-b[k])>1e-5 for k in range(3))==1:
                spline=curve.splines.new('POLY'); spline.points.add(1)
                spline.points[0].co=(*a,1); spline.points[1].co=(*b,1)
    cage=bpy.data.objects.new('DIAGNOSTICO_JAULA_TEMP',curve); bpy.context.scene.collection.objects.link(cage); cage.color=(1,.18,.05,1)
    scene=bpy.context.scene
    scene.render.engine='BLENDER_WORKBENCH'; scene.render.resolution_x=1100; scene.render.resolution_y=800; scene.render.resolution_percentage=100
    scene.render.image_settings.file_format='PNG'; scene.render.use_compositing=False; scene.render.use_sequencer=False
    scene.display.render_aa='8'; scene.display.shading.color_type='OBJECT'; scene.display.shading.light='STUDIO'
    scene.display.shading.show_cavity=True; scene.display.shading.cavity_type='BOTH'; scene.display.shading.show_shadows=True
    scene.display.shading.background_type='WORLD'; scene.world.color=(.055,.055,.055); scene.view_settings.view_transform='Standard'
    camera_data=bpy.data.cameras.new('FASE3_CAMERA_TEMP'); camera=bpy.data.objects.new('FASE3_CAMERA_TEMP',camera_data); scene.collection.objects.link(camera); scene.camera=camera
    camera_data.type='ORTHO'; camera_data.clip_start=.01; camera_data.clip_end=100
    captures=[]
    for label,center,position,scale in [('capitan_escala_posterior',(0,5.3,1.25),(6,-2,6),7.5),
                                        ('posterior_planta',(0,6,1.5),(0,6,12),7.0)]:
        camera.location=position; camera.rotation_euler=(Vector(center)-camera.location).to_track_quat('-Z','Y').to_euler(); camera_data.ortho_scale=scale
        scene.render.filepath=str(output/(label+'.png')); bpy.ops.render.render(write_still=True)
        captures.append({'file':label+'.png','camera':position,'target':center,'ortho_scale':scale})
    if sha(source)!=data['copy_final_sha256'] or sha(ORIGINAL)!=data['original_sha256']:
        raise RuntimeError('Se alteró archivo guardado durante capturas')
    manifest={'source_sha256':data['copy_final_sha256'],'original_sha256':data['original_sha256'],
              'imported_fingerprint_matches_after_reload':True,'original_objects_checked':len(original_objects),
              'helper_dimensions_verified':references,'distance_analytic_tests':5,'shaders_checked':len(shader_checks),
              'unused_orphan_materials_not_persisted_by_blender_save':unused_not_saved,
              'packed_images':packed,'hidden_roof_meshes_only_in_render_process':hidden,
              'captures':captures,'note':'Workbench grises y auxiliares cian/amarillo/naranja artificiales. No PBR. No guardado.'}
    (output/'VERIFICACION_Y_CAPTURAS.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2),encoding='utf-8')
    print('VERIFICACION_FASE3_OK',flush=True)


if __name__=='__main__' and '--' in sys.argv:
    main()
