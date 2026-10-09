"""Inventario Ascendant: solo lectura de originales, ZIP sin extracción e imágenes
por metadatos/huellas calculadas localmente. No publica imágenes ni geometría.
Ejecutar con Python/Pillow preinstalado; no instalar dependencias.
"""
import argparse
from collections import Counter, defaultdict
import csv
import hashlib
import io
import json
from pathlib import Path
import struct
import urllib.request
import xml.etree.ElementTree as ET
import zipfile
from PIL import Image

ROOT=Path(__file__).resolve().parents[2]
MODEL=ROOT/'assets/otros/bridges/USS Ascendant bridge'


def sha(path):
    with path.open('rb') as f: return hashlib.file_digest(f,'sha256').hexdigest()


def image_info(data):
    with Image.open(io.BytesIO(data)) as im:
        pixels=im.convert('RGB')
        return {'width':im.width,'height':im.height,'mode':im.mode,'format':im.format,
                'bytes':len(data),'sha256':hashlib.sha256(data).hexdigest(),
                'decoded_rgb_sha256':hashlib.sha256(pixels.tobytes()).hexdigest()}


def main():
    p=argparse.ArgumentParser(description=__doc__); p.add_argument('--salida',type=Path,required=True)
    args=p.parse_args(); output=args.salida.resolve()
    if output.exists() or output==ROOT/'assets' or ROOT/'assets' in output.parents: raise RuntimeError('Salida nueva fuera de assets')
    if not MODEL.is_dir(): raise FileNotFoundError(MODEL)
    files=[]
    for path in sorted(MODEL.rglob('*')):
        if not path.is_file(): continue
        row={'path':path.relative_to(MODEL).as_posix(),'bytes':path.stat().st_size,'format':path.suffix.lower(),'sha256':sha(path)}
        if path.suffix.lower() in ['.jpg','.jpeg','.png']: row['image']=image_info(path.read_bytes())
        files.append(row)
    glb=MODEL/'uss_ascendant_bridge.glb'
    raw=glb.read_bytes(); magic,version,total=struct.unpack_from('<4sII',raw)
    assert magic==b'glTF' and version==2 and total==len(raw)
    length,kind=struct.unpack_from('<II',raw,12); assert kind==0x4E4F534A
    gltf=json.loads(raw[20:20+length]); offset=20+length
    blen,bkind=struct.unpack_from('<II',raw,offset); assert bkind==0x004E4942
    binary=memoryview(raw)[offset+8:offset+8+blen]
    embedded=[]
    for index,im in enumerate(gltf['images']):
        view=gltf['bufferViews'][im['bufferView']]; start=view.get('byteOffset',0); data=bytes(binary[start:start+view['byteLength']])
        row=image_info(data); row.update(index=index,mime=im.get('mimeType'),bufferView=im['bufferView'])
        row['matching_external_bytes']=[f['path'] for f in files if f['sha256']==row['sha256']]
        row['matching_external_decoded_rgb']=[f['path'] for f in files if f.get('image',{}).get('decoded_rgb_sha256')==row['decoded_rgb_sha256']]
        embedded.append(row)
    dae=next(MODEL.rglob('*.dae')); tree=ET.parse(dae); doc=tree.getroot(); ns={'c':doc.tag.split('}')[0][1:]}
    geometry=[]
    for geom in doc.findall('c:library_geometries/c:geometry',ns):
        mesh=geom.find('c:mesh',ns)
        geometry.append({'id':geom.get('id'),'triangles':sum(int(t.get('count')) for t in mesh.findall('c:triangles',ns)),
                         'lines':sum(int(t.get('count')) for t in mesh.findall('c:lines',ns))})
    dependencies=[]
    for im in doc.findall('c:library_images/c:image',ns):
        uri=im.findtext('c:init_from',namespaces=ns)
        path=(dae.parent/uri).resolve()
        if MODEL.resolve() not in path.parents: raise RuntimeError('Dependencia de textura sale del modelo; revisar antes de importar')
        dependencies.append({'id':im.get('id'),'uri':uri,'exists':path.is_file(),'sha256':sha(path) if path.is_file() else None})
    materials=[]
    effect_by_id={e.get('id'):e for e in doc.findall('c:library_effects/c:effect',ns)}
    for mat in doc.findall('c:library_materials/c:material',ns):
        effect=effect_by_id[mat.find('c:instance_effect',ns).get('url')[1:]]
        technique=effect.find('c:profile_COMMON/c:technique',ns)
        materials.append({'id':mat.get('id'),'name':mat.get('name'),'effect':effect.get('id'),
                          'technique':technique[0].tag.split('}')[-1],
                          'parameters':[{'tag':e.tag.split('}')[-1],'text':(e.text or '').strip(),'attrib':e.attrib} for e in technique[0].iter()]})
    archives=[]
    for path in MODEL.rglob('*.zip'):
        members=[]
        with zipfile.ZipFile(path) as z:
            for info in z.infolist():
                if info.is_dir(): continue
                with z.open(info) as stream: digest=hashlib.file_digest(stream,'sha256').hexdigest()
                extracted=path.with_suffix('')/info.filename
                members.append({'name':info.filename,'bytes':info.file_size,'compressed_bytes':info.compress_size,'sha256':digest,
                                'extracted_exists':extracted.is_file(),'matches_extracted':extracted.is_file() and sha(extracted)==digest})
        archives.append({'path':path.relative_to(MODEL).as_posix(),'members':members})
    provenance_url='https://api.sketchfab.com/v3/models/5c882f022ccd45c285f76321af00da8f'
    try:
        req=urllib.request.Request(provenance_url,headers={'User-Agent':'Local technical audit; public metadata only'})
        api=json.load(urllib.request.urlopen(req,timeout=20))
        provenance={'url':provenance_url,'date':'2026-10-10','uid':api['uid'],'name':api['name'],
                    'license':api['license'],'author':{k:api['user'][k] for k in ['displayName','username','profileUrl']},
                    'tags':[t['name'] for t in api['tags']],'isDownloadable':api['isDownloadable'],
                    'publishedAt':api['publishedAt'],'vertexCount':api['vertexCount'],'faceCount':api['faceCount'],
                    'description_paraphrase':'El publicador presenta el puente como perteneciente al mismo tipo de nave/prototipo que Vengeance; menciona puestos y silla de mando. Es afirmación del publicador, no canon verificado.'}
    except Exception as error: provenance={'url':provenance_url,'error':str(error)}
    exact=defaultdict(list); pixel=defaultdict(list)
    for row in files:
        exact[row['sha256']].append(row['path'])
        if 'image' in row: pixel[row['image']['decoded_rgb_sha256']].append(row['path'])
    protected=[]
    for name in ['enterprise_importacion_inicial.blend','theurgy_trabajo_v0_1.blend']:
        path=ROOT/'blender/principal'/name
        if path.exists(): protected.append({'path':path.relative_to(ROOT).as_posix(),'sha256':sha(path),'bytes':path.stat().st_size})
    result={'schema':'ascendant-source-v1','date':'2026-10-10','root':MODEL.relative_to(ROOT).as_posix(),
            'files':files,'directories':[p.relative_to(MODEL).as_posix() for p in sorted(MODEL.rglob('*')) if p.is_dir()],
            'counts':dict(Counter(f['format'] for f in files)),'total_bytes':sum(f['bytes'] for f in files),
            'glb':{'asset':gltf['asset'],'counts':{k:len(gltf.get(k,[])) for k in ['scenes','nodes','meshes','materials','images','textures','skins','animations','cameras']},
                   'primitive_modes':dict(Counter(p.get('mode',4) for m in gltf['meshes'] for p in m['primitives'])),
                   'position_entries':sum(gltf['accessors'][p['attributes']['POSITION']]['count'] for m in gltf['meshes'] for p in m['primitives']),
                   'triangles':sum(gltf['accessors'][p['indices']]['count']//3 for m in gltf['meshes'] for p in m['primitives'] if p.get('mode',4)==4),
                   'line_segments':sum(gltf['accessors'][p['indices']]['count']//2 for m in gltf['meshes'] for p in m['primitives'] if p.get('mode',4)==1),
                   'materials':gltf['materials'],'embedded_images':embedded,'nodes':gltf['nodes'],'extensionsUsed':gltf.get('extensionsUsed',[])},
            'dae':{'version':doc.get('version'),'asset_xml':ET.tostring(doc.find('c:asset',ns),encoding='unicode'),
                   'unit_meter':float(doc.find('c:asset/c:unit',ns).get('meter')),'up_axis':doc.findtext('c:asset/c:up_axis',namespaces=ns),
                   'geometries':geometry,'unique_triangles':sum(r['triangles'] for r in geometry),
                   'unique_lines':sum(r['lines'] for r in geometry),'library_nodes':len(doc.findall('c:library_nodes/c:node',ns)),
                   'images':dependencies,'materials':materials},'zip_archives':archives,
            'exact_duplicate_files':[v for v in exact.values() if len(v)>1],
            'external_images_identical_decoded_rgb':[v for v in pixel.values() if len(v)>1],
            'provenance_public_metadata':provenance,'protected_scenes_hashes_only_no_geometry_read':protected,
            'privacy':'No modelos, texturas ni capturas enviados a servicios externos. Petición GET de metadatos públicos sin adjuntos.'}
    output.mkdir(parents=True)
    (output/'FUENTES_ASCENDANT.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8')
    with (output/'ARCHIVOS_ASCENDANT.csv').open('x',encoding='utf-8-sig',newline='') as f:
        writer=csv.DictWriter(f,fieldnames=['path','format','bytes','sha256','width','height']); writer.writeheader()
        for row in files: writer.writerow({**{k:row[k] for k in ['path','format','bytes','sha256']},'width':row.get('image',{}).get('width',''),'height':row.get('image',{}).get('height','')})
    print(json.dumps({'files':len(files),'bytes':result['total_bytes'],'counts':result['counts'],'zip_members_matching':sum(m['matches_extracted'] for a in archives for m in a['members']),'identical_external_image_pairs':len(result['external_images_identical_decoded_rgb'])},ensure_ascii=False))


if __name__=='__main__': main()
