"""Lectura adicional de puestos: intersecciones verticales y huecos a varias cotas.

Excluye asientos para identificar el apoyo real bajo ellos; no usa únicamente
las dos mitades de arquitectura, porque existen otros módulos de pavimento.
Sin guardar ni alterar el .blend. Nombres/índices de los impactos trazables.
"""
import argparse
import hashlib
import json
from pathlib import Path
import sys
import bpy
from mathutils import Vector


def main():
    p=argparse.ArgumentParser(description=__doc__); p.add_argument('--salida',type=Path,required=True)
    args=p.parse_args(sys.argv[sys.argv.index('--')+1:])
    root=Path(__file__).resolve().parents[2]; output=args.salida.resolve()
    if output.exists() or output==root/'assets' or root/'assets' in output.parents: raise RuntimeError('Salida nueva fuera de assets')
    source=Path(bpy.data.filepath)
    before=hashlib.file_digest(source.open('rb'),'sha256').hexdigest()
    depsgraph=bpy.context.evaluated_depsgraph_get()
    def cast(origin,direction,distance):
        found,loc,normal,index,obj,matrix=bpy.context.scene.ray_cast(depsgraph,Vector(origin),Vector(direction),distance=distance)
        return {'point':list(loc),'normal':list(normal),'polygon_index':index,'object':obj.original.name,'distance':(loc-Vector(origin)).length} if found else None
    records=json.loads((root/'docs/auditorias/enterprise_bpy_v2/AUDITORIA_ENTERPRISE_DATOS.json').read_text(encoding='utf-8'))['objects']
    chairs=set(o['name'] for o in records if '/Group_31' in o['path'] or '/Captain_s_Chair_1/' in o['path'])
    result={}
    for label,x,y in [('capitan',0,4.6),('silla_CONN_XNEG',-1.02379,1.35),('silla_CONN_XPOS',.94948,1.35)]:
        origin=Vector((x,y,2.2)); hits=[]
        for _ in range(80):
            hit=cast(origin,(0,0,-1),3)
            if not hit or hit['point'][2]<-.9: break
            hits.append(hit); origin=Vector(hit['point'])-Vector((0,0,.0002))
        support=next((h for h in hits if h['object'] not in chairs and h['point'][2]<=.6 and abs(h['normal'][2])>.7),None)
        sections=[]
        for z in [.75,.9,1.,1.1]:
            rays={axis:cast((x,y,z),vec,4) for axis,vec in {'-Y':(0,-1,0),'+Y':(0,1,0),'-X':(-1,0,0),'+X':(1,0,0)}.items()}
            sections.append({'world_z':z,'rays':rays,'free_Y':sum(rays[k]['distance'] for k in ['-Y','+Y']) if all(rays[k] for k in ['-Y','+Y']) else None,
                             'free_X':sum(rays[k]['distance'] for k in ['-X','+X']) if all(rays[k] for k in ['-X','+X']) else None})
        result[label]={'xy':[x,y],'vertical_hits':hits,'support_excluding_chairs':support,'free_sections_at_seat_position':sections}
    if hashlib.file_digest(source.open('rb'),'sha256').hexdigest()!=before: raise RuntimeError('Fuente cambió')
    output.parent.mkdir(parents=True,exist_ok=True)
    output.write_text(json.dumps({'copy_sha256':before,'method':'scene.ray_cast; cadenas verticales con avance 0.2 mm; apoyo horizontal inferior a z=.6 excluyendo todos los asientos por jerarquía; secciones no equivalen a volumen libre de cápsula','stations':result},ensure_ascii=False,indent=2),encoding='utf-8')
    print(json.dumps(result,ensure_ascii=False),flush=True)


if __name__=='__main__' and '--' in sys.argv: main()
