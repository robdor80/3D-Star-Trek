"""Importa SOLO Ascendant en un proceso background aislado, audita y guarda
escenas locales de análisis nuevas. No cambia archivos fuente ni datos importados.
GLB/DAE se importan por separado; no carga Enterprise/Theurgy ni sus inventarios.
Usa funciones genéricas de inventario existentes, sin ejecutar su main.
"""
import argparse
from array import array
from collections import Counter,defaultdict
import hashlib
import importlib.util
import json
import math
from pathlib import Path
import sys
import time
import bpy
import numpy as np
from mathutils import Vector

sys.dont_write_bytecode=True
sys.path.insert(0,str(Path(__file__).resolve().parent))
from auditar_enterprise import mesh_info,serialize_value,bounds,merge_bounds
ROOT=Path(__file__).resolve().parents[2]
MODEL=ROOT/'assets/otros/bridges/USS Ascendant bridge'


def sha(path):
    with path.open('rb') as f: return hashlib.file_digest(f,'sha256').hexdigest()


def operator_available(operator):
    try: operator.get_rna_type(); return True
    except (AttributeError,RuntimeError): return False


def collada_register_existing():
    addon=Path(bpy.utils.user_resource('EXTENSIONS'))/'blender_org/collada_support'
    if not (addon/'blender_manifest.toml').is_file(): raise RuntimeError('Extensión Collada existente no disponible; no instalar automáticamente')
    sys.path[:0]=[str(p) for p in sorted((addon/'wheels').glob('*.whl'))]
    spec=importlib.util.spec_from_file_location('ascendant_existing_collada',addon/'__init__.py',submodule_search_locations=[str(addon)])
    module=importlib.util.module_from_spec(spec);sys.modules[spec.name]=module;spec.loader.exec_module(module)
    if not module.HAS_COLLADA: raise RuntimeError('Dependencias existentes no importables: '+str(module.COLLADA_IMPORT_ERROR))
    module.register()
    if not operator_available(bpy.ops.import_scene.collada): raise RuntimeError('Operador Collada no se registró')
    return {'addon_path':str(addon),'manifest_sha256':sha(addon/'blender_manifest.toml'),
            'version':module.bl_info['version'],'temporary_registration_only':True,'no_preferences_saved':True}


def topology_extra(mesh):
    nv,ne,nl,nf=len(mesh.vertices),len(mesh.edges),len(mesh.loops),len(mesh.polygons)
    co=np.empty((nv,3),np.float32);mesh.vertices.foreach_get('co',co.ravel())
    edge_indices=np.empty(nl,np.int32);mesh.loops.foreach_get('edge_index',edge_indices)
    counts=np.bincount(edge_indices,minlength=ne) if nl else np.zeros(ne,np.int32)
    areas=np.empty(nf,np.float32);mesh.polygons.foreach_get('area',areas)
    winding=None
    loop_totals=np.empty(nf,np.int32);mesh.polygons.foreach_get('loop_total',loop_totals)
    if nf and np.all(loop_totals==3):
        loop_vertices=np.empty(nl,np.int32);mesh.loops.foreach_get('vertex_index',loop_vertices)
        vs=loop_vertices.reshape(-1,3); next_vs=np.roll(vs,-1,axis=1).ravel()
        signs=np.where(loop_vertices<next_vs,1.,-1.)
        signed=np.bincount(edge_indices,weights=signs,minlength=ne)
        winding=int(np.count_nonzero((counts==2)&(abs(signed)>1.5)))
    return {'vertices_nonfinite':int(np.count_nonzero(~np.isfinite(co).all(axis=1))),
            'exact_zero_area_faces':int(np.count_nonzero(areas==0)),
            'area_local_sum':float(areas.sum(dtype=np.float64)),
            'boundary_edges_by_indices':int(np.count_nonzero(counts==1)),
            'edges_more_than_two_faces':int(np.count_nonzero(counts>2)),
            'edges_without_faces':int(np.count_nonzero(counts==0)),
            'paired_edges_inconsistent_winding':winding}


def audit_scene(label,factor,source,output,import_log):
    start=time.monotonic(); objects=sorted(bpy.context.scene.objects,key=lambda o:o.name)
    child=defaultdict(list)
    for obj in objects:
        if obj.parent:child[obj.parent.name].append(obj.name)
    mesh_cache={}; used_material_objects=defaultdict(set); records=[]
    keys=[]; area_sum=0.
    for obj in objects:
        if obj.type!='MESH': continue
        mesh=obj.data
        if mesh.name not in mesh_cache:
            info=mesh_info(mesh)
            keep=['name','vertices','edges','faces','triangles','loose_edges','uv_layers','face_material_indices','materials','bbox_local','edge_connected_components','exact_coincident_components','exact_coincident_largest_components']
            mesh_cache[mesh.name]={k:info[k] for k in keep}
            mesh_cache[mesh.name].update(topology_extra(mesh))
    print('ASCENDANT_MALLAS_'+label+'='+str(len(mesh_cache)),flush=True)
    for obj in objects:
        record={'id':'ASC-'+label.upper()+'-'+hashlib.sha256(obj.name.encode()).hexdigest()[:12],
                'name':obj.name,'type':obj.type,'parent':obj.parent.name if obj.parent else None,
                'children':child[obj.name],'data':obj.data.name if obj.data else None,
                'collections':[c.name for c in obj.users_collection],
                'local_scale':list(obj.scale),'local_location':list(obj.location),'local_rotation':list(obj.rotation_euler),
                'world_determinant':obj.matrix_world.determinant(),
                'matrix_world':[list(row) for row in obj.matrix_world],
                'modifiers':[{'name':m.name,'type':m.type} for m in obj.modifiers],
                'constraints':[{'name':m.name,'type':m.type} for m in obj.constraints],
                'instance_type':obj.instance_type,'hidden_viewport':obj.hide_get() or obj.hide_viewport,'hidden_render':obj.hide_render,
                'bbox_m':None,'materials':[s.name for s in obj.material_slots]}
        if obj.type=='MESH':
            mesh=obj.data; info=mesh_cache[mesh.name]
            coords=np.empty((len(mesh.vertices),3),np.float32);mesh.vertices.foreach_get('co',coords.ravel())
            matrix=np.array(obj.matrix_world,dtype=np.float64)
            world=(coords@matrix[:3,:3].T+matrix[:3,3])*factor
            if len(world):
                low=world.min(axis=0);high=world.max(axis=0)
                record['bbox_m']={'min':low.tolist(),'max':high.tolist(),'size':(high-low).tolist(),'center':((low+high)/2).tolist()}
            info.setdefault('object_names',[]).append(obj.name)
            for p in mesh.polygons:
                if p.material_index<len(obj.material_slots):
                    mat=obj.material_slots[p.material_index].material
                    if mat:used_material_objects[mat.name].add(obj.name)
            mesh.calc_loop_triangles()
            tri=np.empty((len(mesh.loop_triangles),3),np.int32);mesh.loop_triangles.foreach_get('vertices',tri.ravel())
            if len(tri):
                pts=world[tri]
                cross=np.cross(pts[:,1]-pts[:,0],pts[:,2]-pts[:,0]);area_sum+=np.linalg.norm(cross,axis=1).sum(dtype=np.float64)*.5
                # Huellas completas de triángulos a grid 0.1 mm; no se escriben
                # posiciones. Orden de vértices sin orientación para contraste.
                q=np.rint(pts/.0001).astype('<i4');order=np.lexsort((q[:,:,2],q[:,:,1],q[:,:,0]),axis=1)
                q=np.take_along_axis(q,order[:,:,None],axis=1)
                keys.append(np.ascontiguousarray(q.reshape(-1,9)).view('V36').ravel())
        records.append(record)
    record_by_name={r['name']:r for r in records}
    def subtree(name):
        row=record_by_name[name]
        boxes=[row['bbox_m']];count=int(row['type']=='MESH');tris=mesh_cache.get(row['data'],{}).get('triangles',0)
        for ch in row['children']:
            n,t,b=subtree(ch);count+=n;tris+=t;boxes.append(b)
        row['subtree_mesh_count']=count;row['subtree_triangles']=tris;row['subtree_bbox_m']=merge_bounds(boxes)
        return count,tris,row['subtree_bbox_m']
    for row in records:
        if row['parent'] is None:subtree(row['name'])
    materials=[]; image_users=defaultdict(list)
    for mat in bpy.data.materials:
        nodes=[];links=[]
        if mat.node_tree:
            for node in mat.node_tree.nodes:
                image=node.image if node.type=='TEX_IMAGE' else None
                if image:image_users[image.name].append(mat.name)
                nodes.append({'name':node.name,'type':node.type,'image':image.name if image else None,
                              'inputs':{s.name:serialize_value(s.default_value) for s in node.inputs if hasattr(s,'default_value') and not s.is_linked}})
            links=[{'from':l.from_node.name,'from_socket':l.from_socket.name,'to':l.to_node.name,'to_socket':l.to_socket.name} for l in mat.node_tree.links]
        signature=hashlib.sha256(json.dumps({'nodes':nodes,'links':links,'diffuse':list(mat.diffuse_color)},sort_keys=True).encode()).hexdigest()
        materials.append({'name':mat.name,'used_by_faces':bool(used_material_objects[mat.name]),'object_users':sorted(used_material_objects[mat.name]),
                          'diffuse':list(mat.diffuse_color),'nodes':nodes,'links':links,'inspected_signature':signature,
                          'surface_render_method':getattr(mat,'surface_render_method',None),'use_backface_culling':mat.use_backface_culling})
    images=[]
    for image in bpy.data.images:
        if image.source!='FILE': continue
        packed=list(image.packed_files);path=Path(bpy.path.abspath(image.filepath)) if image.filepath else None
        images.append({'name':image.name,'filepath':image.filepath,'size':list(image.size),'colorspace':image.colorspace_settings.name,
                       'packed_bytes':[p.packed_file.size for p in packed],
                       'packed_sha256':[hashlib.sha256(p.packed_file.data).hexdigest() for p in packed],
                       'external_exists':bool(path and path.is_file()),'material_users':image_users[image.name]})
    signs=defaultdict(list)
    for mat in materials:signs[mat['inspected_signature']].append(mat['name'])
    unique=list(mesh_cache.values());mesh_rows=[r for r in records if r['type']=='MESH']
    summary={'objects':len(records),'types':dict(Counter(r['type'] for r in records)),
             'unique_meshes':len(unique),'unique_vertices':sum(m['vertices'] for m in unique),
             'unique_faces':sum(m['faces'] for m in unique),'unique_triangles':sum(m['triangles'] for m in unique),
             'expanded_vertices':sum(mesh_cache[r['data']]['vertices'] for r in mesh_rows),
             'expanded_triangles':sum(mesh_cache[r['data']]['triangles'] for r in mesh_rows),
             'expanded_edges':sum(mesh_cache[r['data']]['edges'] for r in mesh_rows),
             'shared_mesh_datablocks':sum(len(m['object_names'])>1 for m in unique),
             'objects_using_shared_mesh':sum(len(m['object_names']) for m in unique if len(m['object_names'])>1),
             'empty_mesh_datablocks':sum(m['vertices']==0 for m in unique),
             'empty_mesh_objects':sum(mesh_cache[r['data']]['vertices']==0 for r in mesh_rows),
             'line_only_mesh_datablocks':sum(m['vertices']>0 and m['faces']==0 for m in unique),
             'mesh_datablocks_without_uv':sum(not m['uv_layers'] for m in unique),
             'mesh_datablocks_multicomponent_exact_coordinates':sum(m['exact_coincident_components']>1 for m in unique),
             'negative_world_determinants':sum(r['world_determinant']<0 for r in mesh_rows),
             'nonidentity_local_scale_objects':sum(any(abs(s-1)>1e-6 for s in r['local_scale']) for r in records),
             'materials':len(materials),'materials_used_by_faces':sum(m['used_by_faces'] for m in materials),
             'materials_shared_by_face_objects':sum(len(m['object_users'])>1 for m in materials),
             'images':len(images),'packed_images':sum(bool(i['packed_sha256']) for i in images),
             'missing_required_images':[i['name'] for i in images if not i['packed_sha256'] and not i['external_exists']],
             'bbox_m':merge_bounds(r['bbox_m'] for r in records),
             'surface_area_sum_m2_includes_overlaps':area_sum,
             'modifiers_objects':sum(bool(r['modifiers']) for r in records),
             'constraints_objects':sum(bool(r['constraints']) for r in records),
             'boundary_edges_unique_by_indices':sum(m['boundary_edges_by_indices'] for m in unique),
             'nonmanifold_edges_more_than_two_faces_unique':sum(m['edges_more_than_two_faces'] for m in unique),
             'inconsistent_paired_edge_winding_unique':sum(m['paired_edges_inconsistent_winding'] or 0 for m in unique),
             'zero_area_faces_unique':sum(m['exact_zero_area_faces'] for m in unique),
             'nonfinite_vertices_unique':sum(m['vertices_nonfinite'] for m in unique)}
    result={'schema':'ascendant-bpy-v1','format':label,'source':source.relative_to(ROOT).as_posix(),'source_sha256':sha(source),
            'blender_version':bpy.app.version_string,'import':import_log,'raw_world_to_metre_factor_analysis_only':factor,
            'units':{'system':bpy.context.scene.unit_settings.system,'scale_length':bpy.context.scene.unit_settings.scale_length,'length_unit':bpy.context.scene.unit_settings.length_unit},
            'summary':summary,'roots':[r['name'] for r in records if r['parent'] is None],
            'collections':[{'name':c.name,'objects':len(c.objects),'children':[ch.name for ch in c.children]} for c in bpy.data.collections],
            'objects':records,'meshes':mesh_cache,'materials':materials,'images':images,
            'identical_inspected_material_signatures':[v for v in signs.values() if len(v)>1],
            'limits':'Boundary/islas por índices no equivalen a agujeros/piezas físicas. Islas por coordenadas exactas no certifican manifold. Normales se evalúan por winding, sin corregir. Campos bbox_m son interpretación métrica, no transformaciones aplicadas.',
            'elapsed_seconds':time.monotonic()-start}
    (output/(label.upper()+'_BLENDER.json')).write_text(json.dumps(result,ensure_ascii=False,separators=(',',':')),encoding='utf-8')
    combined=np.concatenate(keys) if keys else np.empty(0,dtype='V36')
    values,counts=np.unique(combined,return_counts=True)
    print('ASCENDANT_RESUMEN_'+label+'='+json.dumps(summary),flush=True)
    return result,values,counts


def main():
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--fuentes',type=Path,required=True)
    parser.add_argument('--salida',type=Path,required=True);parser.add_argument('--escenas',type=Path,required=True)
    args=parser.parse_args(sys.argv[sys.argv.index('--')+1:]);output=args.salida.resolve();scenes=args.escenas.resolve()
    for path in [output,scenes]:
        if path.exists() or path==ROOT/'assets' or ROOT/'assets' in path.parents:raise RuntimeError('Destinos nuevos fuera de assets')
    if ROOT/'blender' not in scenes.parents:raise RuntimeError('Escenas de análisis dentro de blender/')
    baseline=json.loads(args.fuentes.read_text(encoding='utf-8'))
    if any('noai' in t.lower() for t in baseline['provenance_public_metadata'].get('tags',[])):raise RuntimeError('Restricción NoAI detectada; detener parte afectada')
    def verify():
        for row in baseline['files']:
            if sha(MODEL/row['path'])!=row['sha256']:raise RuntimeError('Original Ascendant cambiado: '+row['path'])
        for row in baseline['protected_scenes_hashes_only_no_geometry_read']:
            if sha(ROOT/row['path'])!=row['sha256']:raise RuntimeError('Escena protegida cambió externamente')
    verify();output.mkdir(parents=True);scenes.mkdir(parents=True)
    bpy.ops.wm.read_factory_settings(use_empty=True)
    if not operator_available(bpy.ops.import_scene.gltf):raise RuntimeError('Importador GLB existente no registrado')
    glb=MODEL/'uss_ascendant_bridge.glb'
    gltf_options={'filepath':str(glb),'import_pack_images':True,'merge_vertices':False,'import_shading':'NORMALS'}
    props=bpy.ops.import_scene.gltf.get_rna_type().properties
    gltf_options={k:v for k,v in gltf_options.items() if k in props}
    status=bpy.ops.import_scene.gltf(**gltf_options)
    if 'FINISHED' not in status:raise RuntimeError('Importación GLB no completada')
    # Conversión analítica provisional basada en las unidades explícitas del DAE.
    # No escalar objetos, raíz o datos de malla del GLB.
    factor=baseline['dae']['unit_meter']
    glb_result,gkeys,gcounts=audit_scene('glb',factor,glb,output,{'operator':'import_scene.gltf','options':gltf_options})
    bpy.ops.wm.save_as_mainfile(filepath=str(scenes/'ascendant_glb_analisis.blend'),compress=True,check_existing=False)
    verify()
    bpy.ops.wm.read_factory_settings(use_empty=True)
    registration=collada_register_existing()
    dae=next(MODEL.rglob('*.dae'))
    dae_options={'filepath':str(dae),'transformation':'PARENT','recognize_blender_extensions':True}
    status=bpy.ops.import_scene.collada(**dae_options)
    if 'FINISHED' not in status:raise RuntimeError('Importación DAE no completada')
    dae_result,dkeys,dcounts=audit_scene('dae',1.,dae,output,{'operator':'import_scene.collada','options':dae_options,'extension':registration})
    bpy.ops.wm.save_as_mainfile(filepath=str(scenes/'ascendant_dae_analisis.blend'),compress=True,check_existing=False)
    verify()
    common,gi,di=np.intersect1d(gkeys,dkeys,return_indices=True)
    matched=int(np.minimum(gcounts[gi],dcounts[di]).sum())
    comparison={'schema':'ascendant-glb-vs-dae-v1','comparison_only_within_ascendant':True,'glb_source_sha256':sha(glb),'dae_source_sha256':sha(dae),
                'analysis_glb_factor_m':factor,'actual_global_transform_applied':False,
                'triangles_glb_imported':glb_result['summary']['expanded_triangles'],'triangles_dae_imported':dae_result['summary']['expanded_triangles'],
                'triangle_count_delta_dae_minus_glb':dae_result['summary']['expanded_triangles']-glb_result['summary']['expanded_triangles'],
                'triangle_vertices_quantization_m':.0001,'canonical_triangle_multiset_matches':matched,
                'glb_nonmatching_keys_count':int(gcounts.sum())-matched,'dae_nonmatching_keys_count':int(dcounts.sum())-matched,
                'limitations':'Ignora winding y materiales en huella espacial. Coincidencia a grid 0.1 mm no prueba igualdad exacta; desacuerdos pueden proceder del redondeo en límites. No se interpreta todo desacuerdo como pérdida de superficie.',
                'glb_bbox_m':glb_result['summary']['bbox_m'],'dae_bbox_m':dae_result['summary']['bbox_m'],
                'glb_surface_area_m2':glb_result['summary']['surface_area_sum_m2_includes_overlaps'],'dae_surface_area_m2':dae_result['summary']['surface_area_sum_m2_includes_overlaps'],
                'scenes':{'glb':{'path':(scenes/'ascendant_glb_analisis.blend').relative_to(ROOT).as_posix(),'sha256':sha(scenes/'ascendant_glb_analisis.blend')},
                          'dae':{'path':(scenes/'ascendant_dae_analisis.blend').relative_to(ROOT).as_posix(),'sha256':sha(scenes/'ascendant_dae_analisis.blend')}},
                'originals_sha256_verified_after_import':True,'other_scenes_hashes_unchanged':True}
    (output/'CONTRASTE_FORMATOS_ASCENDANT.json').write_text(json.dumps(comparison,ensure_ascii=False,indent=2),encoding='utf-8')
    print('ASCENDANT_CONTRASTE='+json.dumps(comparison),flush=True)


if __name__=='__main__' and '--' in sys.argv:main()
