"""Ocho capturas Workbench locales. No guarda ni modifica la copia importada.
No analiza imágenes con IA. Los títulos funcionales son candidatos numéricos.
"""
import argparse,hashlib,json,math,sys,time
from pathlib import Path
import bpy
from mathutils import Vector
ROOT=Path(__file__).resolve().parents[2]
def sha(p):
    with p.open('rb') as f:return hashlib.file_digest(f,'sha256').hexdigest()
def descendants(obj):
    result={obj};stack=list(obj.children)
    while stack:
        o=stack.pop();result.add(o);stack.extend(o.children)
    return result
def main():
    parser=argparse.ArgumentParser();parser.add_argument('--escena',required=True);parser.add_argument('--salida',required=True)
    args=parser.parse_args(sys.argv[sys.argv.index('--')+1:]);path=Path(args.escena).resolve();out=Path(args.salida).resolve()
    if out.exists() or (ROOT/'assets').resolve() in out.parents:raise RuntimeError('Destino nuevo fuera de assets requerido')
    before=sha(path);bpy.ops.wm.open_mainfile(filepath=str(path));scene=bpy.context.scene
    meshes=[o for o in scene.objects if o.type=='MESH'];roof=descendants(scene.objects['group_11'])
    camera_data=bpy.data.cameras.new('ASC_AUDIT_CAMERA');camera=bpy.data.objects.new('ASC_AUDIT_CAMERA',camera_data)
    scene.collection.objects.link(camera);scene.camera=camera
    scene.render.engine='BLENDER_WORKBENCH';scene.render.resolution_x=960;scene.render.resolution_y=720;scene.render.resolution_percentage=100
    scene.render.image_settings.file_format='PNG';scene.render.film_transparent=False
    shading=scene.display.shading;shading.light='STUDIO';shading.color_type='MATERIAL';shading.show_shadows=True
    shading.show_cavity=True;shading.cavity_type='BOTH';shading.background_type='WORLD'
    if not scene.world:scene.world=bpy.data.worlds.new('ASC_AUDIT_WORLD')
    scene.world.color=(.09,.09,.09);scene.display.render_aa='8';out.mkdir(parents=True)
    views=[
        ('01_general_exterior',(24,-28,24),(0,0,1.3),None,False,29,'Exterior completo; cubierta visible'),
        ('02_cenital_sin_cubierta',(0,0,30),(0,0,0),None,True,25,'Cenital; se oculta group_11 solo para render temporal'),
        ('03_frontal',(0,-22,9),(0,1,1),None,True,24,'Desde lado Y negativo; frente inferido por superficie VIEWSCREEN'),
        ('04_posterior',(0,22,10),(0,0,1),None,True,24,'Desde lado Y positivo; posterior inferido'),
        ('05_conjunto_central_aislado',(6,-7,6),(0,1,.7),'group_1',False,5.8,'Conjunto central independiente; función pendiente de revisión humana'),
        ('06_silla_central_candidata',(2,-.5,3.6),(0,3.91,1.1),'instance_193',False,2.0,'Candidato a silla central aislado; identificación funcional probable'),
        ('07_zona_posterior',(11,16,11),(0,4,1),None,True,15,'Recorte posterior de diagnóstico, sin crear habitaciones'),
        ('08_pieza_perimetral_aislada',(-6,-4,3),(-8.96,-.99,1),'instance_185',False,1.65,'Pieza repetida perimetral candidata a silla; 72 MESH en subárbol'),
    ];manifest=[]
    for filename,location,target,isolated,hide_roof,scale,note in views:
        keep=descendants(scene.objects[isolated]) if isolated else None
        for o in meshes:o.hide_render=(o not in keep) if keep is not None else (hide_roof and o in roof)
        camera.location=location;camera.rotation_euler=(Vector(target)-camera.location).to_track_quat('-Z','Y').to_euler()
        camera_data.type='ORTHO';camera_data.ortho_scale=scale;camera_data.clip_start=.01;camera_data.clip_end=100
        dest=out/(filename+'.png');scene.render.filepath=str(dest);bpy.ops.render.render(write_still=True)
        manifest.append({'path':str(dest.relative_to(ROOT)),'bytes':dest.stat().st_size,'sha256':sha(dest),'camera':location,'target':target,
                         'ortho_scale_m':scale,'isolated_subtree':isolated,'roof_temporarily_hidden':hide_roof,'note':note})
        print('ASCENDANT_CAPTURE',filename,flush=True)
    result={'scene':str(path.relative_to(ROOT)),'scene_sha256_before':before,'scene_sha256_after':sha(path),
        'engine':'Workbench','resolution':[960,720],'antialiasing':8,'third_party_content_not_sent_to_ai':True,
        'visual_review_by_ai':False,'geometry_and_materials_untouched':True,'scene_not_saved':True,'captures':manifest}
    (out/'MANIFIESTO_CAPTURAS.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8')
    items='\n'.join('<figure><img src="'+Path(r['path']).name+'" width="960"><figcaption>'+r['note']+'</figcaption></figure>' for r in manifest)
    (out/'GALERIA_LOCAL.html').write_text('<!doctype html><meta charset="utf-8"><title>Ascendant: diagnóstico local</title><h1>Capturas técnicas locales</h1><p>Funciones candidatas; requieren identificación humana. CC BY 4.0: Cpt.Kirk / Sketchfab, modelo 5c882f022ccd45c285f76321af00da8f. Sin revisión visual por IA. Cubierta ocultada en vistas indicadas; renders Workbench locales.</p>'+items,encoding='utf-8')
if __name__=='__main__':main()
