"""Fase 3: lectura geométrica en metros y auxiliares en una copia explícita.

No edita mallas, materiales, padres o transformaciones importados. No exporta
colisiones ni simula CharacterMovement. Salidas nuevas; --preparar-copia solo
admite una copia byte a byte del original en blender/principal/theurgy_*.blend.
"""
import argparse
from array import array
from collections import Counter, defaultdict
import csv
import hashlib
import json
import math
from pathlib import Path
import struct
import sys
import time

import bpy
from mathutils import Vector
from mathutils.bvhtree import BVHTree
from mathutils.geometry import closest_point_on_tri, intersect_ray_tri

ROOT = Path(__file__).resolve().parents[2]
ORIGINAL = ROOT / 'blender/principal/enterprise_importacion_inicial.blend'
RADIUS, HEIGHT = .34, 1.76


def sha(path):
    with path.open('rb') as handle:
        return hashlib.file_digest(handle, 'sha256').hexdigest()


def fingerprint(objects):
    """Huella de geometría local, UV, slots, matrices y jerarquía importados."""
    digest = hashlib.sha256()
    meshes = set()
    for obj in sorted(objects, key=lambda o: o.name):
        row = [obj.name, obj.type, obj.parent.name if obj.parent else None,
               obj.data.name if obj.data else None, sorted(c.name for c in obj.users_collection),
               list(v for r in obj.matrix_world for v in r),
               [(s.name, s.link) for s in obj.material_slots],
               obj.hide_render, obj.hide_viewport, obj.hide_get()]
        digest.update(json.dumps(row, sort_keys=True).encode())
        if obj.type == 'MESH' and obj.data.name not in meshes:
            mesh = obj.data
            meshes.add(mesh.name)
            for prop, items, count, kind in [('co', mesh.vertices, 3, 'f'),
                                              ('vertex_index', mesh.loops, 1, 'i'),
                                              ('material_index', mesh.polygons, 1, 'i')]:
                buf = array(kind, [0]) * (len(items) * count)
                items.foreach_get(prop, buf)
                digest.update(buf.tobytes())
            for uv in mesh.uv_layers:
                buf = array('f', [0]) * (len(uv.data) * 2)
                uv.data.foreach_get('uv', buf)
                digest.update(uv.name.encode() + buf.tobytes())
    return digest.hexdigest()


def segment_distance(a, b, c, d):
    u, v, w = b-a, d-c, a-c
    aa, bb, cc = u.dot(u), u.dot(v), v.dot(v)
    dd, ee = u.dot(w), v.dot(w)
    den = aa*cc-bb*bb
    s = max(0., min(1., (bb*ee-cc*dd)/den)) if den > 1e-20 else 0.
    t = (bb*s+ee)/cc if cc > 1e-20 else 0.
    if t < 0.:
        t, s = 0., max(0., min(1., -dd/aa)) if aa else 0.
    elif t > 1.:
        t, s = 1., max(0., min(1., (bb-dd)/aa)) if aa else 0.
    return (w+s*u-t*v).length


def segment_triangle(a, b, p, q, r):
    direction = b-a
    hit = intersect_ray_tri(p, q, r, direction, a, True)
    if hit is not None and -1e-7 <= (hit-a).dot(direction) <= direction.length_squared+1e-7:
        return 0.
    return min((a-closest_point_on_tri(a, p, q, r)).length,
               (b-closest_point_on_tri(b, p, q, r)).length,
               segment_distance(a, b, p, q), segment_distance(a, b, q, r),
               segment_distance(a, b, r, p))


def clip_triangle(points, low, high):
    """Recorte exacto de triángulo por seis semiespacios; no cambia la malla."""
    for axis in range(3):
        for bound, sign in ((low[axis], 1), (high[axis], -1)):
            output = []
            for a, b in zip(points, points[1:]+points[:1]):
                da, db = sign*(a[axis]-bound), sign*(b[axis]-bound)
                if da >= 0:
                    output.append(a)
                if (da >= 0) != (db >= 0):
                    output.append(a+(b-a)*(da/(da-db)))
            points = output
            if not points:
                return []
    return points


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--salida', type=Path, required=True)
    parser.add_argument('--preparar-copia', action='store_true')
    parser.add_argument('--paso-grid', type=float, default=.25)
    parser.add_argument('--solo-rutas', action='store_true', help='Lectura focalizada; omite grid y no prepara copia')
    args = parser.parse_args(sys.argv[sys.argv.index('--')+1:])
    start = time.monotonic()
    source, output = Path(bpy.data.filepath).resolve(), args.salida.resolve()
    if not ORIGINAL.is_file():
        raise FileNotFoundError(ORIGINAL)
    if source == ORIGINAL.resolve() or source.parent != ORIGINAL.parent.resolve() or not source.name.startswith('theurgy_'):
        raise RuntimeError('Cargar una copia theurgy_*.blend en blender/principal')
    if output.exists() or output == ROOT/'assets' or ROOT/'assets' in output.parents:
        raise RuntimeError('Salida nueva, fuera de assets, obligatoria')
    if not .1 <= args.paso_grid <= .5:
        raise ValueError('Paso de grid permitido: .1.. .5 m')
    original_hash, source_before = sha(ORIGINAL), sha(source)
    if args.preparar_copia and source_before != original_hash:
        raise RuntimeError('Preparar solo una copia inicial idéntica; no sobrescribir trabajo previo')
    if bpy.context.scene.unit_settings.system != 'METRIC' or bpy.context.scene.unit_settings.scale_length != 1.:
        raise RuntimeError('Esta medición presupone METRIC y scale_length=1')
    audit = json.loads((ROOT/'docs/auditorias/enterprise_bpy_v2/AUDITORIA_ENTERPRISE_DATOS.json').read_text(encoding='utf-8'))
    if audit['source_sha256'] != original_hash:
        raise RuntimeError('La fuente cambió respecto a la auditoría fase 2')
    records = {o['name']: o for o in audit['objects']}
    if args.solo_rutas and args.preparar_copia:
        raise RuntimeError('Modo rutas no guarda copia')
    objects = [obj for obj in bpy.context.scene.objects if obj.name in records]
    if len(objects)!=len(records):
        raise RuntimeError('Faltan objetos importados; detener medición')
    initial_fingerprint = fingerprint(objects)
    annotations = json.loads((ROOT/'docs/auditorias/IDENTIFICACIONES_ENTERPRISE.json').read_text(encoding='utf-8'))
    output.mkdir(parents=True)
    vertices, triangles, owners, polygon_indices = [], [], array('I'), array('I')
    mesh_objects = sorted((o for o in objects if o.type == 'MESH' and len(o.data.polygons)), key=lambda o: o.name)
    mesh_cache = {}
    for owner, obj in enumerate(mesh_objects):
        mesh = obj.data
        if mesh.name not in mesh_cache:
            mesh.calc_loop_triangles()
            mesh_cache[mesh.name] = [(tuple(t.vertices), t.polygon_index) for t in mesh.loop_triangles]
        offset = len(vertices)
        vertices.extend(obj.matrix_world @ v.co for v in mesh.vertices)
        local = mesh_cache[mesh.name]
        triangles.extend(tuple(offset+k for k in ids) for ids, _ in local)
        owners.extend([owner]*len(local))
        polygon_indices.extend(poly for _, poly in local)
    print('FASE3_BVH_TRIANGULOS=' + str(len(triangles)), flush=True)
    bvh = BVHTree.FromPolygons(vertices, triangles, all_triangles=True)
    print('FASE3_BVH_LISTO', flush=True)

    def name(index):
        return mesh_objects[owners[index]].name if index is not None else None

    def ray(origin, direction, distance=100):
        loc, normal, index, dist = bvh.ray_cast(Vector(origin), Vector(direction), distance)
        if loc is None:
            return None
        return {'point': list(loc), 'normal': list(normal), 'object': name(index),
                'polygon_index': polygon_indices[index], 'distance': dist}

    def floor(x, y):
        hit = ray((x, y, .60), (0, 0, -1), 1.5)
        if hit and abs(hit['normal'][2]) >= math.cos(math.radians(45)):
            return hit
        return None

    def capsule(x, y, z, radius=RADIUS):
        # Siete bolas de búsqueda cubren el segmento central completo. Recopilan
        # todos los triángulos a distancia <= radio; después distancia exacta
        # segmento/triángulo. Tolerancia de contacto 1 mm, sin eliminar el suelo.
        a, b = Vector((x, y, z+radius)), Vector((x, y, z+HEIGHT-radius))
        spacing = (b-a).length/6
        ids = set()
        for k in range(7):
            for _, _, index, _ in bvh.find_nearest_range(a+(b-a)*(k/6), radius+spacing/2+.032):
                ids.add(index)
        best, blocker, poly = radius+.002, None, None
        exterior = radius+.032
        for index in ids:
            p, q, r = (vertices[t] for t in triangles[index])
            dist = segment_triangle(a, b, p, q, r)
            # Para comprobar margen en rutas planas, omitir del segundo mínimo
            # geometría completamente debajo de los pies (tolerancia 1 mm).
            # Sigue incluida en el ensayo estático principal de la cápsula.
            if max(v.z for v in (p,q,r))>z+.001:
                exterior=min(exterior,dist)
            if dist < best:
                best, blocker, poly = dist, name(index), polygon_indices[index]
        return {'clear': best >= radius-.001, 'min_axis_distance': best,
                'penetration': max(0., radius-best), 'nearest_object': blocker,
                'polygon_index': poly,
                'nonground_clearance_lower_bound': exterior-radius}

    def point(x, y):
        hit = floor(x, y)
        row = {'x': x, 'y': y, 'floor_z': None, 'floor_object': None, 'clear': False}
        if hit:
            z = hit['point'][2]
            row.update(floor_z=z, floor_object=hit['object'], slope_degrees=math.degrees(math.acos(min(1, abs(hit['normal'][2])))))
            row.update(capsule(x, y, z))
            ceiling = ray((x, y, z+.005), (0, 0, 1), 5)
            row['headroom_axis'] = ceiling['distance']+.005 if ceiling else None
            row['overhead_object'] = ceiling['object'] if ceiling else None
        return row

    grid = []
    step = args.paso_grid
    for ix in range(0 if args.solo_rutas else round(21/step)+1):
        x = -10.5+ix*step
        for iy in range(round(16/step)+1):
            grid.append(point(x, -8+iy*step))
        if ix % 12 == 0:
            print('FASE3_GRID_X=' + str(round(x, 2)), flush=True)

    stations = {'frente_centro': (0, -4), 'central_izquierda': (-3, 0),
                'central_derecha': (3, 0), 'tras_CONN': (0, 2.5),
                'capitan_acceso_izq': (-1.2, 4.7), 'capitan_acceso_der': (1.2, 4.7),
                'capitan_detras': (0, 5.9), 'fondo_detras_X': (0, 7.2),
                'perimetro_izq': (-8, 0), 'perimetro_der': (8, 0),
                'soporte_izq': (-4.5, -3), 'soporte_der': (4.5, -3),
                'entre_soportes': (0,-3), 'CONN_lado_neg':(-2.45,1.3),
                'CONN_lado_pos':(2.45,1.3),'secundario_neg':(-3.3,1.3),
                'soporte_exterior_neg':(-6.5,-3)}
    probes = {}
    for label, (x, y) in stations.items():
        row = point(x, y)
        if row['floor_z'] is not None:
            z = row['floor_z']
            row['sections'] = []
            for dz in (.35, .75, 1.25, 1.65):
                sides = {axis: ray((x, y, z+dz), direction, 12)
                         for axis, direction in {'+X': (1, 0, 0), '-X': (-1, 0, 0), '+Y': (0, 1, 0), '-Y': (0, -1, 0)}.items()}
                row['sections'].append({'height_above_floor': dz, 'rays': sides,
                    'width_X': sum(sides[k]['distance'] for k in ('+X', '-X')) if all(sides[k] for k in ('+X', '-X')) else None,
                    'width_Y': sum(sides[k]['distance'] for k in ('+Y', '-Y')) if all(sides[k] for k in ('+Y', '-Y')) else None})
        probes[label] = row

    routes_spec = {
        'frontal_libre': [(0, -4.5), (0, -2), (0, -.6)],
        'CONN_izquierda': [(-3, -1), (-3, 2), (-1.2, 3.5), (-1.2, 4.7)],
        'CONN_derecha': [(3, -1), (3, 2), (1.2, 3.5), (1.2, 4.7)],
        'tras_CONN_a_capitan': [(0, 2.3), (0, 3.8)],
        'rodear_capitan_izq': [(-1.2, 4.7), (-1.2, 5.9), (0, 5.9)],
        'rodear_capitan_der': [(1.2, 4.7), (1.2, 5.9), (0, 5.9)],
        'conexion_posterior_actual': [(0, 5.9), (0, 7.5)],
        'perimetro_izquierdo': [(-8, -2), (-8, 2), (-6, 4), (-3, 5.5)],
        'perimetro_derecho': [(8, -2), (8, 2), (6, 4), (3, 5.5)],
    }
    routes = {}
    for label, waypoints in routes_spec.items():
        samples = []
        for a, b in zip(waypoints, waypoints[1:]):
            length = math.dist(a, b)
            count = math.ceil(length/.02)
            samples.extend(point(a[0]+(b[0]-a[0])*i/count, a[1]+(b[1]-a[1])*i/count) for i in range(count))
        samples.append(point(*waypoints[-1]))
        gaps = [abs(a['floor_z']-b['floor_z']) for a, b in zip(samples, samples[1:]) if a['floor_z'] is not None and b['floor_z'] is not None]
        routes[label] = {'waypoints': waypoints, 'sample_step_max': .02, 'samples': samples,
                         'clear_count': sum(r['clear'] for r in samples), 'count': len(samples),
                         'max_adjacent_floor_change': max(gaps, default=0),
                         'blocked_objects': dict(Counter(r.get('nearest_object') for r in samples if not r['clear']))}
        ground_values=[s['floor_z'] for s in samples if s['floor_z'] is not None]
        routes[label]['flat_floor_range']=max(ground_values)-min(ground_values) if ground_values else None
        routes[label]['nonground_clearance_lower_bound_min']=min((s.get('nonground_clearance_lower_bound',-1) for s in samples),default=-1)
        routes[label]['continuous_flat_route_certified']=all(s['clear'] and s.get('nonground_clearance_lower_bound',-1)>.011 for s in samples) and len(ground_values)==len(samples) and max(ground_values)-min(ground_values)<.001
        print('FASE3_RUTA=' + label, flush=True)

    # Perfiles: cotas y obstáculos reales, no solo envolventes de objetos.
    profiles = {}
    for label, coords in {
        'eje_central': [(0, -5+i*.05) for i in range(256)],
        'acceso_capitan_X': [(-2+i*.025, 4.7) for i in range(161)],
        'detras_capitan_X': [(-2+i*.025, 5.9) for i in range(161)],
        'lado_CONN_X': [(-4+i*.025, 1.3) for i in range(321)],
        'paso_soporte_X': [(-7+i*.025, -3) for i in range(561)],
        'posterior_Y_0': [(0, 5.4+i*.025) for i in range(121)],
        'posterior_Y_izq': [(-1.2, 5.4+i*.025) for i in range(121)],
        'posterior_Y_der': [(1.2, 5.4+i*.025) for i in range(121)],
    }.items():
        profiles[label] = [point(x, y) for x, y in coords]

    # Volumen preliminar de conexión: 3 m x 1.9 m x 2.2 m; no es hueco hecho.
    low, high = Vector((-1.5, 6.4, .43)), Vector((1.5, 8.3, 2.63))
    candidate = defaultdict(lambda: {'polygon_indices': set(), 'clipped_area_m2': 0., 'roles': Counter(), 'clipped_min': [math.inf]*3, 'clipped_max': [-math.inf]*3})
    for index, ids in enumerate(triangles):
        points = [vertices[t] for t in ids]
        if any(max(p[k] for p in points) < low[k] or min(p[k] for p in points) > high[k] for k in range(3)):
            continue
        clipped = clip_triangle(points, low, high)
        if len(clipped) < 3:
            continue
        area = sum((clipped[j]-clipped[0]).cross(clipped[j+1]-clipped[0]).length*.5 for j in range(1, len(clipped)-1))
        if area < 1e-8:
            continue
        row = candidate[name(index)]
        row['polygon_indices'].add(polygon_indices[index])
        row['clipped_area_m2'] += area
        normal = (points[1]-points[0]).cross(points[2]-points[0]).normalized()
        role = 'CONTACTO_SUELO_CONSERVAR' if max(p.z for p in clipped) <= .431 else ('HORIZONTAL_REVISAR' if abs(normal.z) > .7 else 'CERRAMIENTO_OBSTACULO_REVISAR')
        row['roles'][role] += 1
        for p in clipped:
            for k in range(3):
                row['clipped_min'][k] = min(row['clipped_min'][k], p[k])
                row['clipped_max'][k] = max(row['clipped_max'][k], p[k])
    rear = []
    for obj_name, row in sorted(candidate.items()):
        record = records[obj_name]
        rear.append(dict(object=obj_name, id=record['id'], path=record['path'],
                         mesh=record['data'], mesh_users=bpy.data.objects[obj_name].data.users,
                         total_polygons=len(bpy.data.objects[obj_name].data.polygons),
                         polygon_indices=sorted(row['polygon_indices']), clipped_area_m2=row['clipped_area_m2'],
                         roles=dict(row['roles']), clipped_min=row['clipped_min'], clipped_max=row['clipped_max'],
                         caution='Índices ligados a esta versión. Intersección con volumen, NO selección aprobada de borrado.'))

    seat_measurements = {}
    support_vertices,support_faces=[],[]
    for support_obj in mesh_objects:
        record=records[support_obj.name]
        if '/Group_31' in record['path'] or '/Captain_s_Chair_1/' in record['path'] or '/Conn/' in record['path']:
            continue
        if support_obj.name not in ['ID13059','ID19639','ID13069','ID19649','ID13079','ID19659'] and record['bbox_world_vertices']['max'][2]>.60:
            continue
        offset=len(support_vertices)
        support_vertices.extend(support_obj.matrix_world@v.co for v in support_obj.data.vertices)
        support_faces.extend(tuple(offset+i for i in p.vertices) for p in support_obj.data.polygons)
    support_bvh=BVHTree.FromPolygons(support_vertices,support_faces)
    for label, obj_name, xy in [('capitan_asiento', 'ID21637', (0, 4.6)),
                               ('silla_CONN_XNEG_asiento','ID21442.001',(-1.02379,1.35)),
                               ('silla_CONN_XPOS_asiento','ID21442',(.94948,1.35))]:
        obj = bpy.data.objects[obj_name]
        local_vertices = [obj.matrix_world @ v.co for v in obj.data.vertices]
        local_bvh = BVHTree.FromPolygons(local_vertices, [tuple(p.vertices) for p in obj.data.polygons])
        loc, _, _, _ = local_bvh.ray_cast(Vector((*xy, 3)), Vector((0, 0, -1)), 4)
        support,_,_,_=support_bvh.ray_cast(Vector((*xy,.60)),Vector((0,0,-1)),1.5)
        seat_measurements[label] = {'object': obj_name, 'xy': xy, 'seat_surface_z': loc.z if loc else None,
                                     'floor_z': support.z if support else None,
                                     'seat_above_floor': loc.z-support.z if loc and support else None,
                                     'floor_method':'BVH arquitectura y módulos bajos maxZ<=.60; excluye jerarquías de sillas/Conn. Incluye paneles GLASS_FLOOR.'}
    console_surfaces={}
    for label,xy in [('Conn_XNEG',(-1,.5)),('Conn_XPOS',(1,.5)),('Conn_centro',(0,.5))]:
        hit=ray((*xy,1.4),(0,0,-1),1.5)
        console_surfaces[label]={'xy':xy,'surface_hit':hit,'standing_floor_front_reference':probes['central_izquierda']['floor_z'],
                                 'standing_floor_rear_reference':probes['tras_CONN']['floor_z']}
    sightlines = []
    for label, origin in [('capitan_sentado_ensayo', (0, 4.6, 1.6)), ('CONN_izq_sentado_ensayo', (-1, 1.48, 1.2)), ('capitan_pie_ensayo', (-1.2, 4.7, 2.03))]:
        for target in [(0, -7.0, 1.6), (0, -6.5, 2.5)]:
            origin_v, target_v = Vector(origin), Vector(target)
            hit = ray(origin, (target_v-origin_v).normalized(), (target_v-origin_v).length)
            sightlines.append({'label': label, 'eye_hypothesis': origin, 'target_on_front_area': target,
                               'hit': hit, 'note': 'Altura ocular elegida para ensayo; no rig ni postura humana certificados.'})

    result = {'schema': 'fase3-1', 'source': str(source.relative_to(ROOT)), 'source_initial_sha256': source_before,
              'original': str(ORIGINAL.relative_to(ROOT)), 'original_sha256': original_hash,
              'blender': bpy.app.version_string, 'units': 'metres, world space',
              'capsule': {'radius': RADIUS, 'height': HEIGHT, 'half_height': .88, 'contact_tolerance': .001},
              'human_height': 1.8, 'geometry_triangles': len(triangles),
              'method': 'Global world BVH; exact segment-triangle distance for capsule at each sample. Two-sided mesh surfaces, not solid occupancy nor UE5 collision. Grid .25 m; routes <=.02 m. Ground ray starts z=.60, slope abs normal <=45 degrees. Flat route obstacle clearance excludes only triangles completely below feet+1mm; margin>.011m covers <=.02m point spacing with floor variation<1mm. Not proof of floor support over microscopic holes. No crouch/jump/step simulation.',
              'grid_step': step, 'grid': grid, 'probes': probes, 'routes': routes,
              'profiles': profiles, 'seats': seat_measurements, 'console_surfaces':console_surfaces, 'sightlines': sightlines,
              'rear_volume': {'min': list(low), 'max': list(high), 'width': 3., 'headroom': 2.2},
              'rear_candidates': rear, 'original_objects': len(objects), 'initial_fingerprint': initial_fingerprint,
              'summary': {'grid_points': len(grid), 'with_ground': sum(r['floor_z'] is not None for r in grid),
                          'clear_capsule_points': sum(r['clear'] for r in grid),
                          'blockers': dict(Counter(r.get('nearest_object') for r in grid if r['floor_z'] is not None and not r['clear']))}}
    if fingerprint(objects) != initial_fingerprint:
        raise RuntimeError('Cambió geometría/transformación/jerarquía importada durante medición')

    if args.preparar_copia:
        for col_name in ['REF_ESCALA', 'REF_TRANSITABILIDAD', 'ANALISIS_POSTERIOR', 'DIAGNOSTICO', 'CANDIDATOS_MISSION_OPS']:
            if bpy.data.collections.get(col_name):
                raise RuntimeError('La copia ya tiene auxiliares; elegir copia inicial nueva')
            collection = bpy.data.collections.new(col_name)
            bpy.context.scene.collection.children.link(collection)
        def mesh_helper(label, points, faces, col_name, color):
            mesh = bpy.data.meshes.new(label)
            mesh.from_pydata(points, [], faces)
            obj = bpy.data.objects.new(label, mesh)
            bpy.data.collections[col_name].objects.link(obj)
            obj.display_type = 'WIRE'
            obj.show_in_front = True
            obj.color = color
            obj['fase3_auxiliar'] = True
            obj['exportar_UE5'] = False
            return obj
        # Cápsula exacta de ensayo, polos incluidos; 32 segmentos y 8 anillos/hemisferio.
        rings = [(RADIUS*math.cos(t), RADIUS+RADIUS*math.sin(t)) for t in [-math.pi/2+i*math.pi/16 for i in range(9)]]
        rings += [(RADIUS*math.cos(t), HEIGHT-RADIUS+RADIUS*math.sin(t)) for t in [i*math.pi/16 for i in range(9)]]
        cap_vertices = [(radius*math.cos(j*math.tau/32), radius*math.sin(j*math.tau/32), z) for radius, z in rings for j in range(32)]
        cap_faces = [(i*32+j, i*32+(j+1)%32, (i+1)*32+(j+1)%32, (i+1)*32+j) for i in range(len(rings)-1) for j in range(32)]
        cap = mesh_helper('REF_CAPSULA_UE5_R034_H176', cap_vertices, cap_faces, 'REF_ESCALA', (.1, .85, .95, 1))
        cap.location = (-1.2, 4.7, probes['capitan_acceso_izq']['floor_z'] or .43)
        cap['radio_m'], cap['altura_m'], cap['half_height_m'] = RADIUS, HEIGHT, .88
        # Silueta humana esquemática por cajas independientes en una malla auxiliar.
        hv, hf = [], []
        for lo, hi in [((-.09,-.10,1.55),(.09,.10,1.8)), ((-.22,-.12,.88),(.22,.12,1.55)),
                       ((-.2,-.10,0),(-.04,.10,.88)), ((.04,-.10,0),(.2,.10,.88)),
                       ((-.32,-.08,.92),(-.22,.08,1.5)), ((.22,-.08,.92),(.32,.08,1.5))]:
            offset = len(hv)
            hv += [(x,y,z) for x in (lo[0],hi[0]) for y in (lo[1],hi[1]) for z in (lo[2],hi[2])]
            hf += [tuple(offset+k for k in face) for face in [(0,1,3,2),(4,6,7,5),(0,4,5,1),(2,3,7,6),(0,2,6,4),(1,5,7,3)]]
        human = mesh_helper('REF_HUMANO_H180_ESQUEMATICO', hv, hf, 'REF_ESCALA', (.95,.65,.12,1))
        human.location = (1.2,4.7,probes['capitan_acceso_der']['floor_z'] or .43)
        human['altura_m'] = 1.8
        for label, row in probes.items():
            obj = bpy.data.objects.new('MEDIDA_'+label, None)
            bpy.data.collections['REF_TRANSITABILIDAD'].objects.link(obj)
            obj.location = (row['x'],row['y'],row['floor_z'] or 0)
            obj.empty_display_type, obj.empty_display_size = 'CIRCLE', .34
            obj['capsula_libre_muestra'] = row['clear']
            obj['fase3_auxiliar'], obj['exportar_UE5'] = True, False
        box_vertices = [(x,y,z) for x in (low.x,high.x) for y in (low.y,high.y) for z in (low.z,high.z)]
        box = mesh_helper('VOLUMEN_CONEXION_PROPUESTO_NO_ABIERTO', box_vertices, [(0,1,3,2),(4,6,7,5),(0,4,5,1),(2,3,7,6),(0,2,6,4),(1,5,7,3)], 'ANALISIS_POSTERIOR', (.95,.2,.1,1))
        box['ancho_m'], box['altura_libre_m'], box['cota_suelo_m'] = 3., 2.2, .43
        for row in rear:
            obj = bpy.data.objects.new('CANDIDATO_'+row['object'], None)
            bpy.data.collections['CANDIDATOS_MISSION_OPS'].objects.link(obj)
            obj.location = [(a+b)/2 for a,b in zip(row['clipped_min'],row['clipped_max'])]
            obj.empty_display_size = .1
            obj['objeto_fuente'], obj['id_fuente'] = row['object'], row['id']
            obj['accion'] = 'REVISAR, NO BORRAR'
            obj['fase3_auxiliar'], obj['exportar_UE5'] = True, False
        for label, coordinates in [('PIVOTE_ASIENTO_CAPITAN_PROPUESTO',(0,4.6,.85)),
                                   ('INTERACCION_CONN_XNEG_PROPUESTA',(-1,1.48,1.2)),
                                   ('INTERACCION_CONN_XPOS_PROPUESTA',(1,1.48,1.2)),
                                   ('UNION_MISSION_OPS_PROPUESTA',(0,6.53,.43))]:
            obj = bpy.data.objects.new(label, None)
            bpy.data.collections['DIAGNOSTICO'].objects.link(obj)
            obj.location, obj.empty_display_size = coordinates, .15
            obj['fase3_auxiliar'], obj['exportar_UE5'] = True, False
            obj['estado'] = 'HIPOTESIS, NO PIVOTE FUNCIONAL UE5'
        scene = bpy.context.scene
        scene['fase3_derivado'], scene['fuente_sha256'] = True, original_hash
        scene['escala_global_aplicada'], scene['validado_UE5'] = 1., False
        # Sin ocultar techo ni cambiar materiales/colores/selección importados.
        if fingerprint(objects) != initial_fingerprint or sha(ORIGINAL) != original_hash or sha(source) != source_before:
            raise RuntimeError('La fuente o datos importados cambiaron antes de guardar')
        bpy.ops.wm.save_as_mainfile(filepath=str(source), check_existing=False)
        result['copy_final_sha256'] = sha(source)
        result['auxiliary_objects'] = [o.name for o in bpy.context.scene.objects if o.name not in {p.name for p in objects}]
        result['fingerprint_after_helpers'] = fingerprint(objects)
    if sha(ORIGINAL) != original_hash:
        raise RuntimeError('Original cambió externamente')
    result['elapsed_seconds'] = time.monotonic()-start
    (output/'MEDICIONES_FASE3.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8')
    with (output/'MUESTRAS_PLANTA.csv').open('w',newline='',encoding='utf-8-sig') as f:
        fields = ['x','y','floor_z','floor_object','clear','penetration','nearest_object','headroom_axis','overhead_object','slope_degrees']
        writer = csv.DictWriter(f,fieldnames=fields,extrasaction='ignore'); writer.writeheader(); writer.writerows(grid)
    (output/'CANDIDATOS_POSTERIOR.json').write_text(json.dumps({'source_sha256':original_hash,'volume':result['rear_volume'],'candidates':rear},ensure_ascii=False,indent=2),encoding='utf-8')
    print('FASE3_COMPLETADA=' + json.dumps(result['summary']),flush=True)


if __name__ == '__main__' and '--' in sys.argv:
    main()
