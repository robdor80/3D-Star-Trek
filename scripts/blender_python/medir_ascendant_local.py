"""Diagnóstico numérico local sobre la copia DAE auditada, sin guardar la escena.
BVH de triángulos originales; cápsula conservadora por muestras del eje.
No modifica mallas/materiales y no importa ni compara otros puentes.
"""
import argparse,json,math,sys,time,hashlib
from pathlib import Path
from collections import Counter,deque
import bpy
import numpy as np
from mathutils import Vector
from mathutils.bvhtree import BVHTree

ROOT=Path(__file__).resolve().parents[2]
def sha(p):
    with p.open('rb') as f:return hashlib.file_digest(f,'sha256').hexdigest()

def main():
    parser=argparse.ArgumentParser();parser.add_argument('--escena',required=True);parser.add_argument('--salida',required=True)
    args=parser.parse_args(sys.argv[sys.argv.index('--')+1:]);scene=Path(args.escena).resolve();out=Path(args.salida).resolve()
    if (ROOT/'assets').resolve() in out.parents or out.exists():raise RuntimeError('Destino debe ser nuevo y fuera de assets')
    before=sha(scene);bpy.ops.wm.open_mainfile(filepath=str(scene));start=time.monotonic()
    coords=[];triangles=[];offset=0;horizontal=Counter();rejects=[]
    for o in bpy.context.scene.objects:
        if o.type!='MESH' or not o.data.polygons:continue
        m=o.data;m.calc_loop_triangles()
        co=np.empty((len(m.vertices),3),np.float32);m.vertices.foreach_get('co',co.ravel())
        matrix=np.array(o.matrix_world,dtype=np.float64);co=co@matrix[:3,:3].T+matrix[:3,3]
        t=np.empty((len(m.loop_triangles),3),np.int32);m.loop_triangles.foreach_get('vertices',t.ravel())
        points=co[t];cross=np.cross(points[:,1]-points[:,0],points[:,2]-points[:,0]);area=np.linalg.norm(cross,axis=1)
        valid=area>1e-12;flat=valid & (abs(cross[:,2])>area*.999)
        for height,n in zip(*np.unique(np.round(points[flat,:,2].mean(axis=1),3),return_counts=True)):horizontal[float(height)]+=int(n)
        coords.append(co);triangles.append(t[valid]+offset);offset+=len(co)
    print('ASCENDANT_BVH_BUILD',offset,flush=True)
    co=np.concatenate(coords);tri=np.concatenate(triangles);del coords,triangles
    tree=BVHTree.FromPolygons(co.tolist(),tri.tolist(),all_triangles=True,epsilon=0.0)
    del co,tri
    print('ASCENDANT_BVH_READY',round(time.monotonic()-start,2),flush=True)
    floor_levels=(-.02,.27,.43);radius=.34;height=1.76;lift=.04
    axis=np.linspace(radius+lift,height-radius+lift,19);half_step=float((axis[1]-axis[0])/2)
    def ray(origin,direction,limit):
        p,n,i,dist=tree.ray_cast(Vector(origin),Vector(direction),limit)
        return None if p is None else (p,n,i,dist)
    def probe(x,y):
        hit=ray((x,y,.6),(0,0,-1),1.35)
        if not hit:return {'x':x,'y':y,'floor':None,'status':'sin_soporte'}
        p,n,_,_=hit;z=float(p.z)
        if abs(n.z)<.95 or min(abs(z-k) for k in floor_levels)>.018:
            return {'x':x,'y':y,'floor':z,'status':'soporte_no_identificado_como_suelo'}
        distance=min(float(tree.find_nearest(Vector((x,y,z+float(a))))[3]) for a in axis)
        up=ray((x,y,z+.045),(0,0,1),5)
        headroom=float(up[0].z-z) if up else None
        return {'x':x,'y':y,'floor':z,'axis_distance_min':distance,'headroom':headroom,
                'status':'libre_conservador' if distance>=radius+half_step else 'obstaculo_o_margen_insuficiente'}
    xs=np.round(np.arange(-10.4,10.401,.4),4);ys=np.round(np.arange(-8,8.001,.4),4)
    grid={};records=[]
    for i,x in enumerate(xs):
        for j,y in enumerate(ys):
            r=probe(float(x),float(y));grid[i,j]=r;records.append(r)
        if i%13==0:print('ASCENDANT_GRID',i+1,len(xs),flush=True)
    # Cada enlace se verifica cada <=0.10 m: no se atribuye conectividad a nodos aislados.
    free={ij for ij,r in grid.items() if r['status']=='libre_conservador'};adj={ij:[] for ij in free}
    for i,j in sorted(free):
        for other in [(i+1,j),(i,j+1)]:
            if other not in free:continue
            a,b=grid[i,j],grid[other]
            if abs(a['floor']-b['floor'])>.18:continue
            if all(probe(a['x']+(b['x']-a['x'])*k/4,a['y']+(b['y']-a['y'])*k/4)['status']=='libre_conservador' for k in (1,2,3)):
                adj[i,j].append(other);adj[other].append((i,j))
    labels={};sizes=[]
    for ij in sorted(free):
        if ij in labels:continue
        tag=len(sizes);q=deque([ij]);labels[ij]=tag;n=0
        while q:
            u=q.popleft();n+=1
            for v in adj[u]:
                if v not in labels:labels[v]=tag;q.append(v)
        sizes.append(n)
    targets={'frontal':(0,-3),'acceso_consola_izq':(-1,2.4),'acceso_consola_der':(1,2.4),
             'delante_silla_central':(0,3),'detras_silla_central':(0,5.2),'lateral_izq':(-6,0),'lateral_der':(6,0),'posterior':(0,6)}
    refs={}
    for name,(x,y) in targets.items():
        exact=probe(x,y);near=min(free,key=lambda ij:(grid[ij]['x']-x)**2+(grid[ij]['y']-y)**2) if free else None
        dist=math.hypot(grid[near]['x']-x,grid[near]['y']-y) if near else None
        refs[name]={'target':exact,'nearest_free_grid':grid[near] if near else None,'offset_m':dist,
                    'connected_component':labels[near] if near and dist<=.65 else None}
    # Anchuras entre primeras superficies a tres alturas, en puntos libres concretos.
    sections=[]
    for name,ref in refs.items():
        p=ref['nearest_free_grid']
        if not p or ref['offset_m']>.65:continue
        for h in (.4,.9,1.5):
            left=ray((p['x'],p['y'],p['floor']+h),(-1,0,0),25);right=ray((p['x'],p['y'],p['floor']+h),(1,0,0),25)
            sections.append({'name':name,'x':p['x'],'y':p['y'],'height_above_floor':h,
                'left_distance':float(left[3]) if left else None,'right_distance':float(right[3]) if right else None,
                'span_between_first_surfaces':float(left[3]+right[3]) if left and right else None})
    result={'schema':'ascendant-circulation-preliminary-v1','scene':str(scene.relative_to(ROOT)),'scene_sha256':before,
        'only_ascendant':True,'method':'BVH local, caras con área>1e-12 m2, rayos y distancia a triángulos; sin colisiones UE5',
        'capsule':{'radius_m':radius,'total_height_m':height,'human_reference_m':1.8,'lift_for_floor_m':lift,
                    'axis_samples':19,'max_half_spacing_m':half_step,'pass_threshold_m':radius+half_step},
        'ground':{'ray_start_z_m':.6,'accepted_levels_m':floor_levels,'tolerance_m':.018,'min_abs_normal_z':.95},
        'grid':{'spacing_m':.4,'count':len(records),'status_counts':dict(Counter(r['status'] for r in records)),
                'connected_component_sizes':sizes,'edge_samples_every_m':.1,'allowed_endpoint_step_m':.18},
        'horizontal_triangle_height_counts_top30':horizontal.most_common(30),'targets':refs,'cross_sections':sections,
        'probes':records,'limits':['Rechaza otros niveles de suelo y soportes no identificados; resultado conservador, no cobertura completa.',
            'Cápsula elevada 4 cm; no simula apoyo, gravedad, escalones dinámicos ni movimiento continuo de un Character.',
            'Enlaces discretos con muestras: no prueban barrido continuo ni NavMesh.',
            'Rayos a superficies visuales incluyen vidrio transparente; no equivalen a colisiones configuradas.',
            'No identifica puertas funcionales, salidas ni salas exteriores.'],
        'scene_hash_unchanged':sha(scene)==before,'elapsed_seconds':time.monotonic()-start}
    out.parent.mkdir(parents=True,exist_ok=True);out.write_text(json.dumps(result,ensure_ascii=False,separators=(',',':')),encoding='utf-8')
    print('ASCENDANT_TRANSITO',json.dumps(result['grid']),flush=True)
    print('ASCENDANT_TARGETS',json.dumps(refs),flush=True)

if __name__=='__main__':main()
