"""Agrega evidencias ya calculadas y metadatos XML, sin ejecutar Blender.
Escribe solo informes nuevos; no decodifica ni presenta imágenes de activos.
"""
import csv, hashlib, json, math, xml.etree.ElementTree as ET
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
OUT=ROOT/'docs/auditorias/comparativa_v2'
DAE={'enterprise':ROOT/'assets/enterprise_kelvin/modelo_original/uss-enterprise-a-new-bridge/source/ENT-A1_dae/model.dae',
     'ascendant':ROOT/'assets/otros/bridges/USS Ascendant bridge/uss-ascendant-bridge/source/USS+ASCENDANT+BRIDGE+FINAL/model.dae'}

def read(path):return json.loads(path.read_text(encoding='utf-8'))
def metadata(path):
    root=ET.parse(path).getroot();ns={'c':root.tag.split('}')[0][1:]};a=root.find('c:asset',ns)
    return {'path':path.relative_to(ROOT).as_posix(),'authoring_tool':a.findtext('c:contributor/c:authoring_tool',namespaces=ns),
      'created':a.findtext('c:created',namespaces=ns),'modified':a.findtext('c:modified',namespaces=ns),
      'unit':a.find('c:unit',ns).attrib,'up_axis':a.findtext('c:up_axis',namespaces=ns),
      'material_names':{m.get('id'):m.get('name') for m in root.findall('c:library_materials/c:material',ns)}}

def main():
    target=OUT/'RESUMEN_COMPARATIVO.json';table=OUT/'MODULOS_COMPARADOS.csv'
    if target.exists() or table.exists():raise RuntimeError('No sobrescribir informes existentes')
    data={n:read(OUT/(n.upper()+'_ENSAYO.json')) for n in DAE}
    previous={'enterprise':read(ROOT/'docs/auditorias/enterprise_bpy_v2/AUDITORIA_ENTERPRISE_DATOS.json'),
              'ascendant':read(ROOT/'docs/auditorias/ascendant_bpy_v1/DAE_BLENDER.json')}
    xml={n:metadata(p) for n,p in DAE.items()}
    rows={}
    for n in DAE:
        with (OUT/(n.upper()+'_DIFERENCIAS.csv')).open(encoding='utf-8-sig',newline='') as f:rows[n]=list(csv.DictReader(f))
    signatures={}; material_counts={}; module_rows=[]
    for n,d in data.items():
        old={m['name']:m for m in previous[n]['materials']}
        hashes={i['name']:i['packed_sha256'] for i in d['images']}
        signatures[n]={}
        used=[m for m in d['materials'] if m['face_object_users']]
        for m in used:
            pr=next(node for node in old[m['name']]['nodes'] if node['type']=='BSDF_PRINCIPLED')
            sig={'values':{k:pr['inputs'].get(k,'LINKED_INPUT_NOT_RECORDED_AS_DEFAULT') for k in ['Base Color','Metallic','Roughness','Alpha','Emission Color','Emission Strength','Transmission Weight']},
                 'images_sha256':sorted(h for i in m['images'] for h in hashes[i]),
                 'backface_culling':m['backface_culling'],'render_method':m['render_method']}
            signatures[n][m['name']]=hashlib.sha256(json.dumps(sig,sort_keys=True).encode()).hexdigest()
        surface_meshes={r['data'] for r in rows[n]}
        uv_meshes={r['data'] for r in rows[n] if r['uv']=='True'}
        material_counts[n]={'all_materials':len(d['materials']),'face_materials':len(used),
          'face_materials_shared':sum(m['face_object_users']>1 for m in used),
          'used_images':len({i for m in used for i in m['images']}),
          'surface_mesh_blocks':len(surface_meshes),'surface_mesh_blocks_with_uv':len(uv_meshes),
          'surface_mesh_objects_with_uv':sum(r['uv']=='True' for r in rows[n]),
          'textured_face_objects_without_uv':sum(r['uv']=='False' and any(m['images'] for m in used if m['name'] in json.loads(r['materials'])) for r in rows[n])}
        for name,m in d['modules'].items():
            rs=[r for r in rows[n] if name in json.loads(r['modules'])]
            module_rows.append({'model':n,'module':name,'root':m['root'],
               **{k:m[k] for k in ['mesh_objects_including_empty','surface_mesh_objects','unique_meshes_with_faces','triangles','mesh_blocks_shared_outside']},
               'triangles_with_world_counterpart_key':sum(int(r['triangles_with_counterpart_key']) for r in rs),
               'surface_objects_with_uv':sum(r['uv']=='True' for r in rs),
               'material_ids':json.dumps(m['materials']),
               'material_source_names':json.dumps([xml[n]['material_names'].get(x,x) for x in m['materials']],ensure_ascii=False)})
    matches=[{'enterprise':e,'ascendant':a,'enterprise_source_name':xml['enterprise']['material_names'].get(e),
              'ascendant_source_name':xml['ascendant']['material_names'].get(a)}
       for e,eh in signatures['enterprise'].items() for a,ah in signatures['ascendant'].items() if eh==ah]
    grids={n:{(x,y) for x,y,z in d['grid']['positions_free_main_floor']} for n,d in data.items()}
    common=grids['enterprise']&grids['ascendant'];only_e=grids['enterprise']-grids['ascendant'];only_a=grids['ascendant']-grids['enterprise']
    stairs=[]
    for risers in (6,7,8):
        run=(risers-1)*.28
        stairs.append({'risers':risers,'riser_m':1.11/risers,'tread_trial_m':.28,'horizontal_run_m':run,
            'landing_trial_m_each':.68,'run_plus_two_landings_m':run+1.36,'slope_envelope_deg':math.degrees(math.atan(1.11/run))})
    chairs=read(OUT/'CORRESPONDENCIAS_FOCALES.json')['front_chair_left_local_shape_matches']
    result={'source_xml':xml,'material_counts':material_counts,
      'material_selected_shader_signatures_equal':matches,
      'material_signature_scope':'Exact selected Principled values, packed image SHA256, culling and render mode; excludes UV assignment, whole node graph and appearance.',
      'front_chair_local_shapes':{'enterprise_surface_meshes':len(chairs),'with_raw_local_match_in_ascendant':sum(bool(r['ascendant_front_raw_local_matches']) for r in chairs),
          'enterprise_triangles_in_matched_parts':sum(r['triangles'] for r in chairs if r['ascendant_front_raw_local_matches'])},
      'grid_overlap':{'common_free_XY_points':len(common),'enterprise_only_free_XY_points':len(only_e),'ascendant_only_free_XY_points':len(only_a),
          'enterprise_only_positions':sorted(only_e),'ascendant_only_positions':sorted(only_a),
          'limits':'Static positions only; support may be furniture. XY equality does not certify same support height or connected navigation.'},
      'stairs_unapproved_geometric_trials':stairs,
      'rear_internal_depth_m':8.150263786-6.459950447,
      'rear_captain_bbox_gap_m':{n:6.459950447-d['modules']['capitan']['bbox_m']['max'][1] for n,d in data.items()},
      'recommendation':'A: mantener Enterprise; no cambio del canon ni de la base ejecutado.',
      'recommendation_basis':'Architecture and rear obstacles equivalent; no connected-navigation gain for Ascendant proven; simpler exclusive captain/CONN datasets in Enterprise. Ascendant independent central half groups and larger upper rear gap are real tradeoffs.'}
    with target.open('x',encoding='utf-8') as f:json.dump(result,f,ensure_ascii=False,indent=2)
    with table.open('x',encoding='utf-8-sig',newline='') as f:
        w=csv.DictWriter(f,fieldnames=list(module_rows[0]));w.writeheader();w.writerows(module_rows)
    print('RESUMEN',json.dumps({'material_counts':material_counts,'material_pairs':matches,'chair_shapes':result['front_chair_local_shapes'],'depth':result['rear_internal_depth_m'],'captain_gaps':result['rear_captain_bbox_gap_m']},ensure_ascii=False))
if __name__=='__main__':main()
