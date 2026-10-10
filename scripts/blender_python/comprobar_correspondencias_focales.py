"""Complemento focal: forma local de sillas, anclas y prisma posterior.
Reutiliza la comparación anterior; no BVH, renders, importaciones ni guardados.
Huellas locales expresadas en unidades de los datos, no metros mundiales.
"""
import argparse, hashlib, json, sys
from collections import defaultdict
from pathlib import Path
import bpy
import numpy as np
from mathutils import Vector
sys.dont_write_bytecode = True
sys.path.insert(0, str(Path(__file__).resolve().parent))
from comparar_puentes_dae import SCENES, canonical, subtree, sha, clip_triangle
ROOT = Path(__file__).resolve().parents[2]
ANCHORS = ['ID13059','ID19639','ID13069','ID19649','ID13285','ID13295','ID19865','ID19875',
           'ID14178','ID20751','ID1471','ID1836','ID1651','ID1908','ID11576.001','ID18193.001',
           'ID11576','ID18193','ID11750','ID220','ID475','ID13545','ID16806','ID13907','ID13917']

def digest(keys):
    return hashlib.sha256(np.unique(keys).tobytes()).hexdigest()

def collect(label, folder):
    path=SCENES[label]; before=sha(path)
    bpy.ops.wm.open_mainfile(filepath=str(path))
    prior=json.loads((folder/(label.upper()+'_ENSAYO.json')).read_text(encoding='utf-8'))
    low=np.array(prior['rear_prism']['min']); high=np.array(prior['rear_prism']['max'])
    rear_names=set(prior['rear_prism']['candidates'])
    all_objects=[o for o in bpy.context.scene.objects if o.type=='MESH' and o.data.polygons and any(c.name=='model.dae' for c in o.users_collection)]
    cache={}; rows=[]; rear=[]
    modules={n:subtree(bpy.data.objects[v['root']]) for n,v in prior['modules'].items()}
    for o in all_objects:
        m=o.data
        if m.name not in cache:
            co=np.empty((len(m.vertices),3),np.float32); m.vertices.foreach_get('co',co.ravel())
            m.calc_loop_triangles(); ids=np.empty((len(m.loop_triangles),3),np.int32)
            m.loop_triangles.foreach_get('vertices',ids.ravel()); local=co[ids]
            cache[m.name]=(local, {'local_raw_1e5':digest(canonical(local,.00001)),
              'local_centered_1e5':digest(canonical(local-(co.max(axis=0)+co.min(axis=0))/2,.00001)),
              'local_distinct_triangles':len(np.unique(canonical(local,.00001)))})
        local, local_row=cache[m.name]; matrix=np.array(o.matrix_world,dtype=np.float64)
        world=local@matrix[:3,:3].T+matrix[:3,3]; keys=canonical(world,.0001)
        row={'name':o.name,'mesh':m.name,'triangles':len(local),**local_row,
             'world_distinct_hash':digest(keys),'world_multiset_hash':hashlib.sha256(np.sort(keys).tobytes()).hexdigest(),
             'modules':[n for n,s in modules.items() if o in s], 'materials':sorted({p.material_index for p in m.polygons})}
        rows.append(row)
        if o.name in rear_names:
            mask=(world.max(axis=1)>=low).all(axis=1)&(world.min(axis=1)<=high).all(axis=1)
            for p in world[mask]:
                clipped=clip_triangle([Vector(v) for v in p],Vector(low),Vector(high))
                if len(clipped)>2 and sum((clipped[k]-clipped[0]).cross(clipped[k+1]-clipped[0]).length*.5 for k in range(1,len(clipped)-1))>1e-8:
                    rear.append(p)
    assert sha(path)==before
    print('FOCAL_LEIDO',label,len(rows),len(rear),flush=True)
    return rows, canonical(np.array(rear),.0001)

def main():
    parser=argparse.ArgumentParser();parser.add_argument('--datos',type=Path,required=True)
    args=parser.parse_args(sys.argv[sys.argv.index('--')+1:]); folder=args.datos.resolve()
    target=folder/'CORRESPONDENCIAS_FOCALES.json'
    if target.exists() or ROOT/'assets' in target.parents: raise RuntimeError('Informe nuevo fuera de assets requerido')
    e,ke=collect('enterprise',folder); a,ka=collect('ascendant',folder)
    indexes={k:defaultdict(list) for k in ['world_multiset_hash','world_distinct_hash','local_raw_1e5','local_centered_1e5']}
    for row in a:
        for k,index in indexes.items():index[row[k]].append(row)
    anchors=[]
    for row in e:
        if row['name'] not in ANCHORS:continue
        anchors.append({'enterprise':row['name'],'triangles':row['triangles'],
          'world_multiset_matches':[r['name'] for r in indexes['world_multiset_hash'][row['world_multiset_hash']]],
          'world_distinct_matches':[{'ascendant':r['name'],'triangles':r['triangles']} for r in indexes['world_distinct_hash'][row['world_distinct_hash']]]})
    chairs=[]
    for row in e:
        if 'silla_frontal_izq' not in row['modules']:continue
        matches=indexes['local_raw_1e5'][row['local_raw_1e5']]
        centered=indexes['local_centered_1e5'][row['local_centered_1e5']]
        chairs.append({'enterprise':row['name'],'triangles':row['triangles'],'distinct_local_keys':row['local_distinct_triangles'],
           'ascendant_front_raw_local_matches':[{'name':r['name'],'triangles':r['triangles'],'distinct_local_keys':r['local_distinct_triangles']} for r in matches if 'silla_frontal_izq' in r['modules']],
           'ascendant_front_centered_local_matches':[r['name'] for r in centered if 'silla_frontal_izq' in r['modules']]})
    ue,ce=np.unique(ke,return_counts=True);ua,ca=np.unique(ka,return_counts=True)
    common,ie,ia=np.intersect1d(ue,ua,return_indices=True)
    result={'method':'World quantization .1mm, full triangles intersecting prior rear prism, multiset/winding ignored. Raw local shape set quantization 1e-5 mesh units, ignores duplicated triangles and winding; no normalization of scale/rotation.',
      'anchors':anchors,'front_chair_left_local_shape_matches':chairs,
      'rear_prism_world_matches':{'enterprise_triangles':len(ke),'ascendant_triangles':len(ka),'multiset_common':int(np.minimum(ce[ie],ca[ia]).sum()),'distinct_common':len(common)},
      'limits':'Local shape matching does not prove same pose/UV/materials/face orientation. Nonmatching hashes do not prove exclusive surfaces.',
      'scenes_unchanged':True}
    with target.open('x',encoding='utf-8') as f:json.dump(result,f,ensure_ascii=False,indent=2)
    print('FOCAL_FINAL',json.dumps(result['rear_prism_world_matches']),flush=True)
if __name__=='__main__':main()
