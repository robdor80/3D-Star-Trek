"""Conciliación de triángulos fuente/importador, UV y conjuntos candidatos.
Lee metadatos, índices locales y documentos propios; no escribe activos.
"""
import argparse,json,struct,xml.etree.ElementTree as ET
from pathlib import Path
from collections import Counter
import numpy as np
ROOT=Path(__file__).resolve().parents[2]
BASE=ROOT/'docs/auditorias/ascendant_bpy_v1'
f=json.loads((ROOT/'docs/auditorias/ascendant_fuentes_v1/FUENTES_ASCENDANT.json').read_text(encoding='utf-8'))
d=json.loads((BASE/'DAE_BLENDER.json').read_text(encoding='utf-8'));g=json.loads((BASE/'GLB_BLENDER.json').read_text(encoding='utf-8'))
parser=argparse.ArgumentParser();parser.add_argument('--salida',type=Path,default=BASE/'CONCILIACION_Y_MODULOS.json');args=parser.parse_args()
target=args.salida.resolve()
if (ROOT/'assets').resolve() in target.parents:raise RuntimeError('Salida prohibida en assets')
if target.exists():raise RuntimeError('Salida ya existe')
model=ROOT/'assets/otros/bridges/USS Ascendant bridge';source={x['id']:x for x in f['dae']['geometries']}
root=ET.parse(ROOT/d['source']).getroot();ns={'c':root.tag.split('}')[0][1:]}
diffs=[]
for ge in root.findall('c:library_geometries/c:geometry',ns):
    name=ge.get('id');m=d['meshes'][name];original=source[name]['triangles'];difference=original-m['triangles']
    if not difference:continue
    repeats=0;duplicates=0
    for t in ge.findall('c:mesh/c:triangles',ns):
        inputs=t.findall('c:input',ns);width=max(int(i.get('offset','0')) for i in inputs)+1
        offset=next(int(i.get('offset','0')) for i in inputs if i.get('semantic')=='VERTEX')
        text=t.find('c:p',ns).text;indices=np.fromstring(text,sep=' ',dtype=np.int64).reshape(-1,3,width)[:,:,offset]
        repeats+=int(np.count_nonzero((indices[:,0]==indices[:,1])|(indices[:,1]==indices[:,2])|(indices[:,0]==indices[:,2])))
        duplicates+=len(indices)-len(np.unique(np.sort(indices,axis=1),axis=0))
    diffs.append({'mesh':name,'source_triangles':original,'imported_triangles':m['triangles'],'discarded':difference,
                  'source_triangles_repeated_vertex_indices':repeats,'source_duplicate_index_triplets_ignore_winding':duplicates,'object_instances':len(m['object_names'])})
raw=(ROOT/g['source']).read_bytes();jsonlen,_=struct.unpack_from('<II',raw,12);header=json.loads(raw[20:20+jsonlen]);binstart=20+jsonlen+8
def accessor(index):
    a=header['accessors'][index];v=header['bufferViews'][a['bufferView']];components={'SCALAR':1,'VEC2':2,'VEC3':3,'VEC4':4}[a['type']]
    dtype={5121:'u1',5123:'<u2',5125:'<u4',5126:'<f4'}[a['componentType']];size=np.dtype(dtype).itemsize
    return np.ndarray((a['count'],components),dtype=dtype,buffer=raw,offset=binstart+v.get('byteOffset',0)+a.get('byteOffset',0),strides=(v.get('byteStride',components*size),size))
glb_repeat=0;glb_duplicates=0
for mesh in header['meshes']:
    for primitive in mesh['primitives']:
        if primitive.get('mode',4)!=4:continue
        indices=accessor(primitive['indices']).reshape(-1,3)
        glb_repeat+=int(np.count_nonzero((indices[:,0]==indices[:,1])|(indices[:,1]==indices[:,2])|(indices[:,0]==indices[:,2])))
        glb_duplicates+=len(indices)-len(np.unique(np.sort(indices,axis=1),axis=0))
objects={o['name']:o for o in d['objects']}
selected=['instance_193','instance_75','instance_75-001','instance_185','instance_185-001','instance_185.001','instance_185-001.001',
          'instance_187','instance_187-001','instance_187.001','instance_187-001.001','group_1','instance_9','instance_80',
          'instance_11','instance_11-001','group_11','group_16','group_16-001','instance_89','Component_27','Component_27-001',
          'Component_19','Component_19-001']
modules=[]
for name in selected:
    o=objects[name];nodes=[];stack=[name]
    while stack:
        current=objects[stack.pop()];nodes.append(current);stack.extend(current['children'])
    meshes=[x for x in nodes if x['type']=='MESH'];data={x['data'] for x in meshes}
    materials=set(m['name'] for m in d['materials'] if any(x['name'] in m['object_users'] for x in meshes))
    shared_outside=[name for name in data if any(user not in {o['name'] for o in meshes} for user in d['meshes'][name]['object_names'])]
    modules.append({'name':name,'id':o['id'],'parent':o['parent'],'subtree_mesh_objects':len(meshes),'unique_meshes':len(data),
        'triangles_expanded':o['subtree_triangles'],'bbox_m':o['subtree_bbox_m'],'materials_used':sorted(materials),
        'mesh_datablocks_shared_outside_subtree':len(shared_outside),'technical_independence':'subárbol seleccionable confirmado; función candidata'})
uv={}
for label,audit in [('glb',g),('dae',d)]:
    textured={m['name'] for m in audit['materials'] if any(n.get('image') for n in m['nodes'])};missing=[]
    for name,m in audit['meshes'].items():
        used={m['materials'][int(i)] for i,n in m['face_material_indices'].items() if n and int(i)<len(m['materials'])}
        if used & textured and not m['uv_layers']:missing.append(name)
    uv[label]={'meshes_with_uv':sum(bool(m['uv_layers']) for m in audit['meshes'].values()),
               'mesh_datablocks_textured_but_no_uv':missing,'uv_layer_names':sorted({x['name'] if isinstance(x,dict) else x for m in audit['meshes'].values() for x in m['uv_layers']})}
result={'schema':'ascendant-reconciliation-v1','dae_source_expanded_triangles':sum(source[n]['triangles']*len(m['object_names']) for n,m in d['meshes'].items()),
        'dae_discarded_faces':diffs,'glb_source_repeated_index_triangles':glb_repeat,'glb_source_duplicate_index_triplets_ignore_winding':glb_duplicates,'glb_discarded_triangles':f['glb']['triangles']-g['summary']['expanded_triangles'],
        'dae_import_does_not_preserve_source_lines':True,'uv':uv,'modules':modules,
        'limits':'Subárboles se solapan en la tabla; no sumar todos. Compartir malla/material transmite ediciones de datos; transformar padre independiente no edita esa malla.'}
target.write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps({k:v for k,v in result.items() if k!='modules'},ensure_ascii=False,indent=2))
