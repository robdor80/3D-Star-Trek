"""Ocho vistas locales comparables, mismas cámaras/escala/Workbench.
No guarda escenas, no modifica mallas/materiales, no envía contenido a IA.
"""
import argparse,hashlib,json,sys
from pathlib import Path
import bpy
from mathutils import Vector
sys.dont_write_bytecode=True
sys.path.insert(0,str(Path(__file__).resolve().parent))
from comparar_puentes_dae import SCENES,subtree
ROOT=Path(__file__).resolve().parents[2]
def sha(p):
    with p.open('rb') as f:return hashlib.file_digest(f,'sha256').hexdigest()
def main():
    parser=argparse.ArgumentParser();parser.add_argument('--salida',type=Path,required=True);args=parser.parse_args(sys.argv[sys.argv.index('--')+1:]);out=args.salida.resolve()
    if out.exists() or ROOT/'assets' in out.parents:raise RuntimeError('Destino nuevo fuera de assets requerido')
    out.mkdir(parents=True);rows=[]
    views=[('superior',(0,0,30),(0,0,0),25),('general',(24,-28,24),(0,0,1.3),29),
           ('central',(9,-8,9),(0,2,1),9),('posterior',(11,16,11),(0,5,1),11)]
    for label,path in SCENES.items():
        before=sha(path);bpy.ops.wm.open_mainfile(filepath=str(path));scene=bpy.context.scene
        roof=subtree(bpy.data.objects['group_1' if label=='enterprise' else 'group_11'])
        for o in scene.objects:
            if o.type=='MESH':o.hide_render=o in roof
        camdata=bpy.data.cameras.new('COMPARATIVA_CAMERA');cam=bpy.data.objects.new('COMPARATIVA_CAMERA',camdata);scene.collection.objects.link(cam);scene.camera=cam
        scene.render.engine='BLENDER_WORKBENCH';scene.render.resolution_x=960;scene.render.resolution_y=720;scene.render.resolution_percentage=100
        scene.render.image_settings.file_format='PNG';scene.render.film_transparent=False;scene.display.render_aa='8'
        shading=scene.display.shading;shading.light='STUDIO';shading.color_type='SINGLE';shading.single_color=(.65,.65,.65)
        shading.show_shadows=True;shading.show_cavity=True;shading.cavity_type='BOTH';shading.background_type='VIEWPORT';shading.background_color=(.08,.08,.08)
        for name,position,target,scale in views:
            cam.location=position;cam.rotation_euler=(Vector(target)-cam.location).to_track_quat('-Z','Y').to_euler();camdata.type='ORTHO';camdata.ortho_scale=scale;camdata.clip_start=.01;camdata.clip_end=100
            dest=out/(label+'_'+name+'.png');scene.render.filepath=str(dest);bpy.ops.render.render(write_still=True)
            rows.append({'model':label,'view':name,'path':dest.relative_to(ROOT).as_posix(),'resolution':[960,720],
                'camera':position,'target':target,'ortho_scale_m':scale,'roof_hidden_in_memory':True,'sha256':sha(dest),'source_sha256':before})
            print('COMPARATIVA_CAPTURA',label,name,flush=True)
        assert sha(path)==before
    manifest={'captures':rows,'ai_visual_review':False,'materials_and_meshes_unchanged':True,'no_scene_saved':True,'only_local':True,'engine':'Workbench SINGLE .65 grey AA8'}
    (out/'MANIFIESTO_COMPARATIVA.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2),encoding='utf-8')
    html='<meta charset="utf-8"><title>Comparativa local</title><style>body{font-family:Arial;background:#ddd}section{display:flex;gap:12px}img{width:46vw}figure{margin:0}h2{margin-top:32px}</style><h1>Enterprise / Ascendant — revisión humana local</h1><p>CC BY 4.0, Cpt.Kirk / CaptainJamesKirk, Sketchfab. Importaciones y capturas locales. Cubierta oculta temporalmente; color gris común. Estas vistas no comparan texturas/PBR. No inspeccionadas visualmente por IA.</p>'
    for name,*_ in views:
        html+='<h2>'+name+'</h2><section>'+''.join('<figure><figcaption>'+label+'</figcaption><img src="'+label+'_'+name+'.png"></figure>' for label in SCENES)+'</section>'
    html+='<p>Fuentes: <a href="https://sketchfab.com/3d-models/uss-enterprise-a-new-bridge-a98a3da7570f433684f067c01298ad05">Enterprise</a> / <a href="https://sketchfab.com/3d-models/uss-ascendant-bridge-5c882f022ccd45c285f76321af00da8f">Ascendant</a>; <a href="https://creativecommons.org/licenses/by/4.0/">CC BY 4.0</a>.</p>'
    (out/'REVISION_HUMANA_LOCAL.html').write_text(html,encoding='utf-8')
if __name__=='__main__':main()
