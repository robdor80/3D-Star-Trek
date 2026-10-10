"""Comparación no destructiva de escenas DAE existentes: huellas espaciales,
materiales, conjuntos y pruebas homogéneas. Solo escribe informes nuevos.
No guarda escenas, no importa Theurgy ni modifica geometría/materiales.
"""
import argparse,hashlib,json,sys,time,csv
from pathlib import Path
from collections import Counter,defaultdict
import bpy
import numpy as np
from mathutils import Vector
from mathutils.bvhtree import BVHTree
sys.dont_write_bytecode=True
sys.path.insert(0,str(Path(__file__).resolve().parent))
from medir_transitabilidad_enterprise import segment_triangle,clip_triangle
from auditar_ascendant_blender import topology_extra
ROOT=Path(__file__).resolve().parents[2]
SCENES={'enterprise':ROOT/'blender/principal/enterprise_importacion_inicial.blend',
        'ascendant':ROOT/'blender/analisis/ascendant_v1/ascendant_dae_analisis.blend'}
QUANT=.0001
def sha(p):
    with p.open('rb') as f:return hashlib.file_digest(f,'sha256').hexdigest()
def box(co):
    lo=co.min(axis=0);hi=co.max(axis=0)
    return {k:v.tolist() for k,v in [('min',lo),('max',hi),('size',hi-lo),('center',(hi+lo)/2)]}
def canonical(points,q):
    p=np.rint(points/q).astype('<i4');order=np.lexsort((p[:,:,2],p[:,:,1],p[:,:,0]),axis=1)
    return np.ascontiguousarray(np.take_along_axis(p,order[:,:,None],axis=1)).reshape(-1,9).view('V36').ravel()
def subtree(root):
    result={root};stack=list(root.children)
    while stack:
        o=stack.pop();result.add(o);stack.extend(o.children)
    return result
MODULES={
 'enterprise':{'capitan':'Captain_s_Chair_1','central':'Conn','silla_frontal_izq':'Group_31-002.001','silla_frontal_der':'Group_31-002',
    'techo':'group_1','pantalla':'instance_8','arquitectura_izq':'Component_19','arquitectura_der':'Component_19-001',
    'consola_secundaria_izq':'Console_2','consola_secundaria_der':'Console_2.001',
    'monitores_posteriores_izq':'ID11576.001','monitores_posteriores_der':'ID18193.001'},
 'ascendant':{'capitan':'instance_193','central':'group_1','central_izq':'instance_9','central_der':'instance_80',
    'silla_frontal_izq':'instance_75','silla_frontal_der':'instance_75-001','techo':'group_11','pantalla':'instance_89',
    'arquitectura_izq':'Component_19','arquitectura_der':'Component_19-001','suelo_paneles_izq':'group_16','suelo_paneles_der':'group_16-001',
    'soporte_perimetral_izq':'Component_27','soporte_perimetral_der':'Component_27-001'} }
ROUTES={
 'frontal':[(0,-4.5),(0,-2),(0,-.6)],
 'central_izq':[(-3,-1),(-3,2),(-1.2,3.5),(-1.2,4.7)],
 'central_der':[(3,-1),(3,2),(1.2,3.5),(1.2,4.7)],
 'tras_central_a_capitan':[(0,2.3),(0,3.8)],
 'capitan_izq':[(-1.2,4.7),(-1.2,5.9),(0,5.9)],
 'capitan_der':[(1.2,4.7),(1.2,5.9),(0,5.9)],
 'conexion_posterior':[(0,5.9),(0,7.5)],
 'perimetro_izq':[(-8,-2),(-8,2),(-6,4),(-3,5.5)],
 'perimetro_der':[(8,-2),(8,2),(6,4),(3,5.5)]}
PROBES={'frente':(0,-4),'entre_soportes':(0,-3),'bajo_soporte_izq':(-4.5,-3),'bajo_soporte_der':(4.5,-3),
        'central_izq':(-2.45,1.3),'central_der':(2.45,1.3),'entre_consolas':(0,.8),'tras_central':(0,2.5),
        'capitan_izq':(-1.2,4.7),'capitan_der':(1.2,4.7),'capitan_detras':(0,5.9),
        'perimetro_izq':(-8,0),'perimetro_der':(8,0),'posterior':(0,7.2)}

def analyze(label,out):
    path=SCENES[label];before=sha(path);bpy.ops.wm.open_mainfile(filepath=str(path));start=time.monotonic()
    if bpy.context.scene.unit_settings.system!='METRIC' or bpy.context.scene.unit_settings.scale_length!=1:raise RuntimeError('Escena fuera de contrato métrico')
    objects=sorted((o for o in bpy.context.scene.objects if o.type=='MESH' and o.data.polygons and 'model.dae' in [c.name for c in o.users_collection]),key=lambda o:o.name)
    points=[];owners=[];records=[];coords=[];indices=[];offset=0;mesh_cache={};used_mats=defaultdict(set)
    selections={name:subtree(bpy.data.objects[obj]) for name,obj in MODULES[label].items() if obj in bpy.data.objects}
    for i,o in enumerate(objects):
        m=o.data
        if m.name not in mesh_cache:
            co=np.empty((len(m.vertices),3),np.float32);m.vertices.foreach_get('co',co.ravel());m.calc_loop_triangles()
            tri=np.empty((len(m.loop_triangles),3),np.int32);m.loop_triangles.foreach_get('vertices',tri.ravel())
            mats=np.empty(len(m.polygons),np.int32);m.polygons.foreach_get('material_index',mats)
            mesh_cache[m.name]=(co,tri,mats)
        co,tri,mats=mesh_cache[m.name];matrix=np.array(o.matrix_world,dtype=np.float64);world=co@matrix[:3,:3].T+matrix[:3,3];p=world[tri]
        areas=np.linalg.norm(np.cross(p[:,1]-p[:,0],p[:,2]-p[:,0]),axis=1)*.5
        used=[o.material_slots[j].material.name for j in sorted(set(mats.tolist())) if j<len(o.material_slots) and o.material_slots[j].material]
        for mat in used:used_mats[mat].add(o.name)
        records.append({'name':o.name,'data':m.name,'parent':o.parent.name if o.parent else None,'triangles':len(tri),
            'area_m2':float(areas.sum()),'bbox_m':box(world),'materials':used,'uv':bool(m.uv_layers),'data_users':m.users,
            'reflected':o.matrix_world.determinant()<0,'triangle_start':(records[-1]['triangle_start']+records[-1]['triangles']) if records else 0,'modules':[n for n,s in selections.items() if o in s]})
        points.append(p);owners.append(np.full(len(p),i,np.int32));coords.append(world);indices.append(tri+offset);offset+=len(world)
    p=np.concatenate(points);owner=np.concatenate(owners);co=np.concatenate(coords);tri=np.concatenate(indices)
    del points,owners,coords,indices,mesh_cache
    areas=np.linalg.norm(np.cross(p[:,1]-p[:,0],p[:,2]-p[:,0]),axis=1)*.5
    valid=areas>1e-12;tree=BVHTree.FromPolygons(co.tolist(),tri[valid].tolist(),all_triangles=True)
    bv_tri=tri[valid];bv_owner=owner[valid];verts=[Vector(v) for v in co];del co,tri
    print('COMPARATIVA_BVH',label,len(p),flush=True)
    def ray(x,y,z,direction,distance=5):
        loc,normal,index,dist=tree.ray_cast(Vector((x,y,z)),Vector(direction),distance)
        if loc is None:return None
        return {'z':float(loc.z),'normal_z':float(normal.z),'object':objects[int(bv_owner[index])].name,'distance':float(dist)}
    def point(x,y):
        hit=ray(x,y,.6,(0,0,-1),1.5);r={'x':float(x),'y':float(y),'floor_z':None,'clear':False}
        if not hit:return {**r,'status':'SIN_APOYO'}
        z=hit['z'];r.update(floor_z=z,floor_object=hit['object'])
        if abs(hit['normal_z'])<.70710678:return {**r,'status':'APOYO_PENDIENTE'}
        a=Vector((x,y,z+.34));b=Vector((x,y,z+1.42));ids=set()
        for k in range(7):
            for _,_,index,_ in tree.find_nearest_range(a+(b-a)*(k/6),.432):ids.add(index)
        best=.342;exterior=.372;block=None
        for index in ids:
            v=[verts[j] for j in bv_tri[index]];distance=segment_triangle(a,b,*v)
            if max(t.z for t in v)>z+.001:exterior=min(exterior,distance)
            if distance<best:best=distance;block=objects[int(bv_owner[index])].name
        clear=best>=.339;ceiling=ray(x,y,z+.005,(0,0,1),5)
        r.update(clear=clear,axis_distance_capped=best,nonground_clearance_lower_bound=exterior-.34,blocker=block if not clear else None,
            headroom_axis=ceiling['distance']+.005 if ceiling else None,ground_approved_for_main_floor=z>=-.12,
            status=('LIBRE_ESTATICO' if clear else 'OBSTACULO_O_TRANSICION') if z>=-.12 else 'APOYO_INFERIOR_NO_APROBADO')
        return r
    probes={n:point(*xy) for n,xy in PROBES.items()}
    for r in probes.values():
        if r['floor_z'] is None:continue
        r['sections']=[]
        for h in (.35,.75,1.25,1.65):
            left=ray(r['x'],r['y'],r['floor_z']+h,(-1,0,0),25);right=ray(r['x'],r['y'],r['floor_z']+h,(1,0,0),25)
            r['sections'].append({'height_m':h,'span_X_m':left['distance']+right['distance'] if left and right else None})
    routes={}
    for name,waypoints in ROUTES.items():
        samples=[]
        for a,b in zip(waypoints,waypoints[1:]):
            count=int(np.ceil(np.linalg.norm(np.array(a)-b)/.02))
            samples.extend(point(a[0]+(b[0]-a[0])*k/count,a[1]+(b[1]-a[1])*k/count) for k in range(count))
        samples.append(point(*waypoints[-1]));levels=[s['floor_z'] for s in samples if s['floor_z'] is not None]
        flat=max(levels)-min(levels) if levels else None;margin=min((s.get('nonground_clearance_lower_bound',-1) for s in samples),default=-1)
        all_clear=all(s['clear'] and s.get('ground_approved_for_main_floor',False) for s in samples)
        continuous=all_clear and flat<.001 and margin>.011
        routes[name]={'waypoints':waypoints,'length_m':sum(np.linalg.norm(np.array(a)-b) for a,b in zip(waypoints,waypoints[1:])),
            'sample_step_max_m':.02,'samples':len(samples),'static_clear_count':sum(s['clear'] for s in samples),
            'flat_floor_range_m':flat,'max_adjacent_floor_change_m':max((abs(a['floor_z']-b['floor_z']) for a,b in zip(samples,samples[1:]) if a['floor_z'] is not None and b['floor_z'] is not None),default=0),
            'nonground_clearance_lower_bound_m':margin,'classification':'LIBRE_CONTINUO_PLANO' if continuous else ('LIBRE_MUESTRAS_DESNIVEL_PENDIENTE' if all_clear else 'OBSTACULO_TRANSICION_O_APOYO_PENDIENTE'),
            'blocked_objects':dict(Counter(s.get('blocker') for s in samples if not s['clear']))}
        print('COMPARATIVA_RUTA',label,name,routes[name]['classification'],flush=True)
    # Misma cuadrícula estática para ambos. No equipara puntos libres con rutas.
    grid=[]
    for x in np.round(np.arange(-10.4,10.401,.4),4):
        for y in np.round(np.arange(-8,8.001,.4),4):grid.append(point(float(x),float(y)))
    # Perfil trasero y prisma idéntico a propuesta previa; sin crear abertura.
    profiles={str(x):[point(x,5.4+k*.025) for k in range(121)] for x in (-1.2,0,1.2)}
    low=np.array([-1.5,6.4,.43]);high=np.array([1.5,8.3,2.63]);mask=(p.max(axis=1)>=low).all(axis=1)&(p.min(axis=1)<=high).all(axis=1)
    candidates=defaultdict(lambda:{'triangles_intersecting':0,'area_inside_m2':0.,'min':[float('inf')]*3,'max':[-float('inf')]*3})
    for idx in np.flatnonzero(mask):
        clipped=clip_triangle([Vector(v) for v in p[idx]],Vector(low),Vector(high))
        if len(clipped)<3:continue
        area=sum((clipped[k]-clipped[0]).cross(clipped[k+1]-clipped[0]).length*.5 for k in range(1,len(clipped)-1))
        if area<1e-8:continue
        r=candidates[objects[int(owner[idx])].name];r['triangles_intersecting']+=1;r['area_inside_m2']+=area
        for v in clipped:
            for k in range(3):r['min'][k]=min(r['min'][k],v[k]);r['max'][k]=max(r['max'][k],v[k])
    image_rows=[]
    for img in bpy.data.images:
        if img.source!='FILE':continue
        image_rows.append({'name':img.name,'size':list(img.size),'packed_sha256':[hashlib.sha256(bytes(pk.packed_file.data)).hexdigest() for pk in img.packed_files],
            'packed':bool(img.packed_files),'colorspace':img.colorspace_settings.name})
    materials=[]
    for mat in bpy.data.materials:
        nodes=mat.node_tree.nodes if mat.node_tree else []
        pr=next((n for n in nodes if n.type=='BSDF_PRINCIPLED'),None)
        values={n:float(pr.inputs[n].default_value) for n in ['Metallic','Roughness','Alpha','Emission Strength','Transmission Weight'] if pr and n in pr.inputs}
        materials.append({'name':mat.name,'face_object_users':len(used_mats[mat.name]),'pbr':values,
            'images':sorted({n.image.name for n in nodes if n.type=='TEX_IMAGE' and n.image}),'backface_culling':mat.use_backface_culling,
            'render_method':mat.surface_render_method})
    modules={};data_users=defaultdict(list)
    for o in bpy.data.objects:
        if o.type=='MESH':data_users[o.data.name].append(o)
    for name,selection in selections.items():
        rows=[r for r,o in zip(records,objects) if o in selection];data={r['data'] for r in rows};mids=np.isin(owner,[i for i,o in enumerate(objects) if o in selection]);subset=p[mids]
        all_mesh=[o for o in selection if o.type=='MESH'];outside=sum(any(o not in selection for o in data_users[n]) for n in data)
        modules[name]={'root':MODULES[label][name],'mesh_objects_including_empty':len(all_mesh),'surface_mesh_objects':len(rows),
            'unique_meshes_with_faces':len(data),'triangles':len(subset),'bbox_m':box(subset.reshape(-1,3)) if len(subset) else None,
            'materials':sorted({m for r in rows for m in r['materials']}),'mesh_blocks_shared_outside':outside,
            'fingerprint_0_1mm':hashlib.sha256(np.sort(canonical(subset,QUANT)).tobytes()).hexdigest() if len(subset) else None}
    topology_rows=[topology_extra(m) for m in {o.data for o in objects}]
    topology={k:sum(r[k] or 0 for r in topology_rows) for k in ['exact_zero_area_faces','boundary_edges_by_indices','edges_more_than_two_faces','paired_edges_inconsistent_winding']}
    result={'label':label,'scene':path.relative_to(ROOT).as_posix(),'scene_sha256':before,'units':'metres; identity analytical alignment',
        'triangles':len(p),'bbox_m':box(p.reshape(-1,3)),'area_sum_m2_includes_overlaps':float(areas.sum()),
        'surface_area_weighted_triangle_centroid_m':np.average(p.mean(axis=1),weights=areas,axis=0).tolist(),
        'surface_mesh_objects':len(objects),'modules':modules,'images':image_rows,'materials':materials,'topology_unique_meshes':topology,
        'probes':probes,'routes':routes,'grid':{'count':len(grid),'spacing_m':.4,'status_counts':dict(Counter(r['status'] for r in grid)),
            'positions_free_main_floor':[ [r['x'],r['y'],r['floor_z']] for r in grid if r['status']=='LIBRE_ESTATICO']},
        'rear_profiles':profiles,'rear_prism':{'min':low.tolist(),'max':high.tolist(),'candidates':dict(candidates)},
        'method':'Identical BVH/capsule: exact segment-triangle distance, radius .34m height1.76m; floor ray z=.60 slope<=45; 1mm contact; routes <=.02m; flat<=1mm & nonground margin>11mm for continuous surface clearance; no UE5 simulation/solid occupancy/microhole support proof',
        'scene_hash_unchanged':sha(path)==before,'elapsed_seconds':time.monotonic()-start}
    assert result['scene_hash_unchanged'];(out/(label.upper()+'_ENSAYO.json')).write_text(json.dumps(result,ensure_ascii=False,separators=(',',':')),encoding='utf-8')
    del tree,verts,bv_tri,bv_owner
    return {'points':p,'owners':owner,'records':records,'areas':areas,'modules':modules,'summary':result}

def main():
    parser=argparse.ArgumentParser();parser.add_argument('--salida',type=Path,required=True);args=parser.parse_args(sys.argv[sys.argv.index('--')+1:]);out=args.salida.resolve()
    if out.exists() or ROOT/'assets' in out.parents:raise RuntimeError('Destino nuevo fuera de assets requerido')
    out.mkdir(parents=True);datasets={}
    for label in SCENES:datasets[label]=analyze(label,out)
    a,b=datasets.values();contrasts=[];per_object={}
    for q in (.0001,.0005,.001):
        ka,kb=canonical(a['points'],q),canonical(b['points'],q);ua,ca=np.unique(ka,return_counts=True);ub,cb=np.unique(kb,return_counts=True)
        common,ia,ib=np.intersect1d(ua,ub,return_indices=True);matches=int(np.minimum(ca[ia],cb[ib]).sum());in_a=np.isin(ka,common);in_b=np.isin(kb,common)
        contrasts.append({'quantization_m':q,'shared_triangle_multiset_count':matches,'shared_distinct_triangle_keys':len(common),
            'enterprise_total':len(ka),'ascendant_total':len(kb),'enterprise_percent':100*matches/len(ka),'ascendant_percent':100*matches/len(kb),
            'enterprise_area_with_present_keys_m2':float(a['areas'][in_a].sum()),'ascendant_area_with_present_keys_m2':float(b['areas'][in_b].sum())})
        if q==QUANT:
            for label,d,mask,keys,other_keys in [('enterprise',a,in_a,ka,ub),('ascendant',b,in_b,kb,ua)]:
                per_object[label]=[]
                for i,r in enumerate(d['records']):
                    start=r['triangle_start'];shared=int(mask[start:start+r['triangles']].sum());new={k:v for k,v in r.items() if k!='triangle_start'}
                    new.update(triangles_with_counterpart_key=shared,percent_keys_with_counterpart=100*shared/r['triangles'],
                        geometry_class='EQUIVALENTE_TRIANGULOS_CUANTIZADOS' if shared==r['triangles'] else ('PARCIAL_O_MODIFICADA' if shared else 'SIN_CORRESPONDENCIA_TRIANGULAR_ACREDITADA'))
                    per_object[label].append(new)
        print('COMPARATIVA_MATCH',q,matches,flush=True)
    # Coincidencias completas de subárboles; no deducir función de nombres genéricos.
    group_matches=[{'enterprise':n,'ascendant':m,'triangles':x['triangles']} for n,x in a['modules'].items() for m,y in b['modules'].items() if x['fingerprint_0_1mm']==y['fingerprint_0_1mm']]
    result={'schema':'enterprise-ascendant-comparison-v1','identity_alignment':True,'coordinate_transforms_saved':False,
        'sources':{n:{'path':d['summary']['scene'],'sha256':d['summary']['scene_sha256']} for n,d in datasets.items()},
        'canonical_triangle_method':'Each world vertex rounded to grid; lexicographic vertices then sorted multiset. Ignores winding/UV/materials. Same key implies <=sqrt(3)*q positional difference per vertex; grid-boundary disagreements cause false negatives. Multiplicity retained.',
        'contrasts':contrasts,'subtree_matches':group_matches,'classification_counts':{n:dict(Counter(r['geometry_class'] for r in rows)) for n,rows in per_object.items()},
        'limits':'Triangular difference is not proof of exclusive surface: topology/tessellation/rounding may differ. Historial de derivación no se acredita por geometría sola.'}
    (out/'CORRESPONDENCIA_GEOMETRICA.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8')
    for label,rows in per_object.items():
        fields=['name','data','parent','triangles','triangles_with_counterpart_key','percent_keys_with_counterpart','geometry_class','data_users','reflected','uv','materials','modules','bbox_m']
        with (out/(label.upper()+'_DIFERENCIAS.csv')).open('x',encoding='utf-8-sig',newline='') as stream:
            writer=csv.DictWriter(stream,fieldnames=fields,extrasaction='ignore');writer.writeheader()
            for row in rows:writer.writerow({k:json.dumps(v,ensure_ascii=False) if isinstance(v,(dict,list)) else v for k,v in row.items()})
    print('COMPARATIVA_FINAL',json.dumps(result,ensure_ascii=False),flush=True)
if __name__=='__main__':main()
