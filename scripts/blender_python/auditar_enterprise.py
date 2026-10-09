"""Inventario de lectura bpy. No guarda .blend ni modifica objetos/materiales.

blender --disable-autoexec --background ESCENA.blend --python ESTE_SCRIPT -- --salida CARPETA_NUEVA
La salida debe estar fuera de assets y no existir. IDs dependen de nombre original.
"""
import argparse
import collections
import csv
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


def identifier(name):
    return 'ENT-' + hashlib.sha256(name.encode('utf-8')).hexdigest()[:12]


def hierarchy(obj):
    names = []
    while obj:
        names.append(obj.name)
        obj = obj.parent
    return '/'.join(reversed(names))


def bounds(points):
    low, high = [math.inf] * 3, [-math.inf] * 3
    for point in points:
        for k in range(3):
            low[k] = min(low[k], point[k])
            high[k] = max(high[k], point[k])
    return None if math.isinf(low[0]) else {'min': low, 'max': high,
                                          'size': [high[k] - low[k] for k in range(3)],
                                          'center': [(high[k] + low[k]) / 2 for k in range(3)]}


def merge_bounds(items):
    return bounds(point for box in items if box for point in (box['min'], box['max']))


def mesh_info(mesh):
    # Triangulación calculada en caché de lectura; no se cambia ninguna cara.
    mesh.calc_loop_triangles()
    parent = list(range(len(mesh.vertices)))

    def find(a):
        while parent[a] != a:
            parent[a] = parent[parent[a]]
            a = parent[a]
        return a

    for edge in mesh.edges:
        a, b = map(find, edge.vertices)
        if a != b:
            parent[b] = a
    groups = collections.defaultdict(list)
    for vertex in mesh.vertices:
        groups[find(vertex.index)].append(vertex.index)
    components = sorted(groups.values(), key=lambda values: (-len(values), values[0]))
    # Segunda medida virtual, sin soldar: conectar coordenadas EXACTAMENTE iguales.
    # Diferentes caras con índices duplicados pueden representar la misma superficie.
    coordinate_parent = parent.copy()

    def find_coordinate(a):
        while coordinate_parent[a] != a:
            coordinate_parent[a] = coordinate_parent[coordinate_parent[a]]
            a = coordinate_parent[a]
        return a

    seen_coordinates = {}
    for vertex in mesh.vertices:
        key = tuple(vertex.co)
        previous = seen_coordinates.setdefault(key, vertex.index)
        a, b = find_coordinate(vertex.index), find_coordinate(previous)
        if a != b:
            coordinate_parent[b] = a
    virtual_groups = collections.defaultdict(list)
    for vertex in mesh.vertices:
        virtual_groups[find_coordinate(vertex.index)].append(vertex.index)
    virtual_samples = sorted(virtual_groups.values(), key=lambda values: (-len(values), values[0]))[:30]
    # Conectividad por índices/aristas: costuras y vértices coincidentes no soldados
    # pueden multiplicar islas. Nunca se presenta como número de piezas mecánicas.
    component_samples = [{'vertices': len(ids), 'first_vertex': ids[0],
                          'bbox_local': bounds(mesh.vertices[i].co for i in ids)}
                         for ids in components[:30]]
    return {'name': mesh.name, 'users': mesh.users, 'vertices': len(mesh.vertices),
            'edges': len(mesh.edges), 'faces': len(mesh.polygons),
            'triangles': len(mesh.loop_triangles), 'loose_edges': sum(e.is_loose for e in mesh.edges),
            'uv_layers': [{'name': uv.name, 'active_render': uv.active_render,
                           'loops': len(uv.data)} for uv in mesh.uv_layers],
            'face_material_indices': dict(collections.Counter(p.material_index for p in mesh.polygons)),
            'materials': [m.name if m else None for m in mesh.materials],
            'bbox_local': bounds(v.co for v in mesh.vertices),
            'edge_connected_components': len(components),
            'component_size_histogram': dict(collections.Counter(len(ids) for ids in components)),
            'largest_components': component_samples,
            'exact_coincident_components': len(virtual_groups),
            'exact_coincident_largest_components': [
                {'vertices': len(ids), 'first_vertex': ids[0],
                 'bbox_local': bounds(mesh.vertices[i].co for i in ids)} for ids in virtual_samples],
            'attributes': [{'name': a.name, 'domain': a.domain, 'type': a.data_type} for a in mesh.attributes]}


def serialize_value(value):
    if isinstance(value, (str, bool, int, float)) or value is None:
        return value
    try:
        return list(value)
    except TypeError:
        return str(value)


def main():
    args = argparse.ArgumentParser(description=__doc__)
    args.add_argument('--salida', type=Path, required=True)
    parsed = args.parse_args(sys.argv[sys.argv.index('--') + 1:])
    root = Path(__file__).resolve().parents[2]
    out = parsed.salida.resolve()
    if out == root / 'assets' or root / 'assets' in out.parents:
        raise RuntimeError('Salida dentro de assets prohibida')
    if out.exists():
        raise FileExistsError('La salida debe ser nueva; se evita sobrescribir inventarios/mapas')
    source = Path(bpy.data.filepath).resolve()
    if not source.is_file():
        raise RuntimeError('Debe abrirse una escena guardada; no se reconstruye la importación')
    source_hash = sha_file(source)
    out.mkdir(parents=True)
    objects = sorted(bpy.data.objects, key=lambda obj: obj.name)
    child_names = collections.defaultdict(list)
    for obj in objects:
        if obj.parent:
            child_names[obj.parent.name].append(obj.name)
    meshes = {m.name: mesh_info(m) for m in bpy.data.meshes}
    print('AUDIT: mallas analizadas', len(meshes), flush=True)
    records = []
    mesh_objects = collections.defaultdict(list)
    material_objects = collections.defaultdict(list)
    for obj in objects:
        box = bounds(obj.matrix_world @ v.co for v in obj.data.vertices) if obj.type == 'MESH' else None
        row = {'id': identifier(obj.name), 'name': obj.name, 'type': obj.type,
               'path': hierarchy(obj), 'parent': obj.parent.name if obj.parent else None,
               'children': child_names[obj.name],
               'collections': [c.name for c in obj.users_collection],
               'data': obj.data.name if obj.data else None,
               'instance_type': obj.instance_type,
               'instance_collection': obj.instance_collection.name if obj.instance_collection else None,
               'location': list(obj.location), 'rotation_mode': obj.rotation_mode,
               'rotation_euler': list(obj.rotation_euler), 'rotation_quaternion': list(obj.rotation_quaternion),
               'scale': list(obj.scale), 'dimensions_api': list(obj.dimensions),
               'matrix_world': [list(r) for r in obj.matrix_world],
               'matrix_local': [list(r) for r in obj.matrix_local],
               'world_determinant': obj.matrix_world.to_3x3().determinant(),
               'bbox_world_vertices': box, 'hide_render': obj.hide_render,
               'hide_viewport': obj.hide_viewport, 'hide_get': obj.hide_get(),
               'modifiers': [{'name': m.name, 'type': m.type, 'show_viewport': m.show_viewport,
                              'show_render': m.show_render} for m in obj.modifiers],
               'constraints': [{'name': c.name, 'type': c.type} for c in obj.constraints],
               'material_slots': [{'name': s.material.name if s.material else None, 'link': s.link}
                                  for s in obj.material_slots],
               'animation_data': bool(obj.animation_data),
               'shape_keys': bool(obj.type == 'MESH' and obj.data.shape_keys)}
        records.append(row)
        if obj.type == 'MESH':
            mesh_objects[obj.data.name].append(obj.name)
        for slot in obj.material_slots:
            if slot.material:
                material_objects[slot.material.name].append(obj.name)
    by_name = {r['name']: r for r in records}

    def aggregate(name):
        row = by_name[name]
        if 'subtree_mesh_objects' in row:
            return
        for child in row['children']:
            aggregate(child)
        row['subtree_mesh_objects'] = int(row['type'] == 'MESH') + sum(by_name[c]['subtree_mesh_objects'] for c in row['children'])
        row['subtree_bbox_world'] = merge_bounds([row['bbox_world_vertices']] + [by_name[c]['subtree_bbox_world'] for c in row['children']])
    for row in records:
        aggregate(row['name'])
    for mesh_name, users in mesh_objects.items():
        meshes[mesh_name]['object_names'] = users
    materials, image_nodes = [], collections.defaultdict(list)
    for material in bpy.data.materials:
        nodes, links = [], []
        if material.node_tree:
            for node in material.node_tree.nodes:
                image = node.image if node.type == 'TEX_IMAGE' else None
                if image:
                    image_nodes[image.name].append({'material': material.name, 'node': node.name})
                nodes.append({'name': node.name, 'type': node.type, 'image': image.name if image else None,
                              'inputs': {s.name: serialize_value(s.default_value) for s in node.inputs
                                         if hasattr(s, 'default_value') and not s.is_linked}})
            links = [{'from_node': l.from_node.name, 'from_socket': l.from_socket.name,
                      'to_node': l.to_node.name, 'to_socket': l.to_socket.name} for l in material.node_tree.links]
        signature = hashlib.sha256(json.dumps({'nodes': nodes, 'links': links,
                                               'diffuse': list(material.diffuse_color)}, sort_keys=True).encode()).hexdigest()
        materials.append({'name': material.name, 'data_users': material.users,
                          'object_users': sorted(set(material_objects[material.name])),
                          'diffuse': list(material.diffuse_color), 'use_nodes': material.use_nodes,
                          'nodes': nodes, 'links': links, 'exact_node_signature': signature})
    images = []
    for image in bpy.data.images:
        packed = list(image.packed_files)
        resolved = str(Path(bpy.path.abspath(image.filepath)).resolve()) if image.filepath else None
        images.append({'name': image.name, 'source': image.source, 'filepath': image.filepath,
                       'absolute_resolved': resolved, 'exists_external': bool(resolved and Path(resolved).is_file()),
                       'packed_files': len(packed),
                       'packed_sha256': [hashlib.sha256(p.packed_file.data).hexdigest() for p in packed],
                       'packed_bytes': [p.packed_file.size for p in packed],
                       'size': list(image.size), 'channels': image.channels,
                       'colorspace': image.colorspace_settings.name, 'users': image.users,
                       'image_nodes': image_nodes[image.name],
                       'usable_source': bool(packed or (resolved and Path(resolved).is_file()) or image.source != 'FILE')})
    scene = bpy.context.scene
    bridge = [r for r in records if 'model.dae' in r['collections']]
    summary = {'objects': len(records), 'scene_objects': len(scene.objects),
               'types': dict(collections.Counter(r['type'] for r in records)),
               'bridge_collection_objects': len(bridge),
               'bridge_types': dict(collections.Counter(r['type'] for r in bridge)),
               'unique_meshes': len(meshes), 'mesh_datablocks_shared': sum(len(m['object_names']) > 1 for m in meshes.values()),
               'mesh_objects_using_shared_data': sum(len(m['object_names']) for m in meshes.values() if len(m['object_names']) > 1),
               'unique_vertices': sum(m['vertices'] for m in meshes.values()),
               'unique_faces': sum(m['faces'] for m in meshes.values()),
               'unique_triangles': sum(m['triangles'] for m in meshes.values()),
               'object_vertices_sum': sum(meshes[r['data']]['vertices'] for r in records if r['type'] == 'MESH'),
               'object_faces_sum': sum(meshes[r['data']]['faces'] for r in records if r['type'] == 'MESH'),
               'object_triangles_sum': sum(meshes[r['data']]['triangles'] for r in records if r['type'] == 'MESH'),
               'bbox_bridge_world': merge_bounds(r['bbox_world_vertices'] for r in bridge),
               'negative_world_determinants': sum(r['world_determinant'] < 0 for r in records if r['type'] == 'MESH'),
               'nonidentity_object_scale': sum(any(abs(v - 1) > 1e-6 for v in r['scale']) for r in records),
               'materials': len(materials), 'shared_materials': sum(len(m['object_users']) > 1 for m in materials),
               'file_images': sum(i['source'] == 'FILE' for i in images),
               'packed_file_images': sum(i['source'] == 'FILE' and i['packed_files'] > 0 for i in images),
               'missing_required_file_images': [i['name'] for i in images if i['source'] == 'FILE' and not i['usable_source']],
               'mesh_datablocks_multiple_components': sum(m['edge_connected_components'] > 1 for m in meshes.values()),
               'mesh_datablocks_multiple_exact_coincident_components': sum(m['exact_coincident_components'] > 1 for m in meshes.values()),
               'empty_mesh_datablocks': sum(not m['vertices'] for m in meshes.values()),
               'empty_mesh_objects': sum(not meshes[r['data']]['vertices'] for r in records if r['type'] == 'MESH'),
               'objects_with_modifiers': sum(bool(r['modifiers']) for r in records),
               'objects_with_constraints': sum(bool(r['constraints']) for r in records)}
    payload = {'schema': 'enterprise-bpy-audit-v1', 'source': str(source), 'source_sha256': source_hash,
               'blender_version': bpy.app.version_string, 'summary': summary,
               'scene': {'name': scene.name, 'unit_system': scene.unit_settings.system,
                         'scale_length': scene.unit_settings.scale_length,
                         'length_unit': scene.unit_settings.length_unit,
                         'frame': scene.frame_current, 'render_engine': scene.render.engine},
               'collections': [{'name': c.name, 'objects': len(c.objects), 'all_objects': len(c.all_objects),
                                'children': [v.name for v in c.children], 'hide_render': c.hide_render,
                                'hide_viewport': c.hide_viewport} for c in bpy.data.collections],
               'roots': [r['name'] for r in records if not r['parent']],
               'objects': records, 'meshes': meshes, 'materials': materials, 'images': images,
               'notes': ['Conteos base, no evaluación de modificadores.',
                         'Islas por índices/aristas no equivalen a componentes físicos.',
                         'IDs basados en nombre; CSV asociado al SHA-256 fuente; no IDs glTF.',
                         'No se guarda el .blend; calc_loop_triangles solo calcula caché.']}
    (out / 'AUDITORIA_ENTERPRISE_DATOS.json').write_text(json.dumps(payload, ensure_ascii=False, separators=(',', ':')), encoding='utf-8')
    fields = ['id', 'nombre_tecnico', 'tipo', 'ruta_jerarquica', 'padre', 'malla', 'malla_compartida_objetos',
              'vertices', 'caras', 'triangulos', 'islas_por_aristas', 'islas_coordenadas_exactas', 'materiales', 'uv', 'bbox_world',
              'mallas_descendientes', 'funcion', 'certeza', 'accion_theurgy', 'evidencia', 'objetos_relacionados',
              'captura', 'observaciones', 'sha256_escena']
    with (out / 'MAPA_OBJETOS_ENTERPRISE.csv').open('x', encoding='utf-8-sig', newline='') as stream:
        writer = csv.DictWriter(stream, fieldnames=fields)
        writer.writeheader()
        for row in records:
            mesh = meshes.get(row['data'], {}) if row['type'] == 'MESH' else {}
            writer.writerow({'id': row['id'], 'nombre_tecnico': row['name'], 'tipo': row['type'],
                             'ruta_jerarquica': row['path'], 'padre': row['parent'], 'malla': row['data'],
                             'malla_compartida_objetos': len(mesh.get('object_names', [])),
                             'vertices': mesh.get('vertices', ''), 'caras': mesh.get('faces', ''),
                             'triangulos': mesh.get('triangles', ''), 'islas_por_aristas': mesh.get('edge_connected_components', ''),
                             'islas_coordenadas_exactas': mesh.get('exact_coincident_components', ''),
                             'materiales': '|'.join(s['name'] or '' for s in row['material_slots']),
                             'uv': '|'.join(v['name'] for v in mesh.get('uv_layers', [])),
                             'bbox_world': json.dumps(row['bbox_world_vertices'], separators=(',', ':')),
                             'mallas_descendientes': row['subtree_mesh_objects'], 'funcion': '',
                             'certeza': 'PENDIENTE DE VERIFICACIÓN VISUAL', 'accion_theurgy': '',
                             'evidencia': 'Inventario bpy; identificación funcional pendiente',
                             'sha256_escena': source_hash})
    if sha_file(source) != source_hash:
        raise RuntimeError('La escena fuente cambió durante la lectura (posible guardado externo)')
    print('AUDIT_SUMMARY=' + json.dumps(summary, ensure_ascii=False), flush=True)


if __name__ == '__main__':
    main()
