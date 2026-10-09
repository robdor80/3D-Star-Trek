"""Contrasta JSON bpy con DAE/texturas inmutables. Python estándar, sin Blender.

python SCRIPT --datos JSON --dae ORIGINAL --salida JSON_NUEVO
No extrae ni escribe recursos. Compara IDs de geometría/material fuente.
"""
import argparse
import collections
import hashlib
import json
from pathlib import Path
import xml.etree.ElementTree as ET


def digest(path):
    value = hashlib.sha256()
    with path.open('rb') as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b''):
            value.update(block)
    return value.hexdigest()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--datos', type=Path, required=True)
    parser.add_argument('--dae', type=Path, required=True)
    parser.add_argument('--salida', type=Path, required=True)
    args = parser.parse_args()
    args.dae = args.dae.resolve()
    root_path = Path(__file__).resolve().parents[2]
    target = args.salida.resolve()
    if target == root_path / 'assets' or root_path / 'assets' in target.parents:
        raise RuntimeError('No escribir en assets')
    if target.exists():
        raise FileExistsError(target)
    data = json.loads(args.datos.read_text(encoding='utf-8'))
    root = ET.parse(args.dae).getroot()
    ns = {'c': root.tag.split('}')[0][1:]}
    diffs, line_only, metadata = [], [], []
    for geometry in root.findall('c:library_geometries/c:geometry', ns):
        name = geometry.get('id')
        mesh = geometry.find('c:mesh', ns)
        triangles = sum(int(p.get('count')) for p in mesh.findall('c:triangles', ns))
        lines = sum(int(p.get('count')) for p in mesh.findall('c:lines', ns))
        imported = data['meshes'].get(name)
        if not triangles and lines:
            line_only.append(name)
        if imported and triangles != imported['triangles']:
            sources = {}
            for source in mesh.findall('c:source', ns):
                array = source.find('c:float_array', ns)
                accessor = source.find('c:technique_common/c:accessor', ns)
                if array is not None and accessor is not None:
                    sources[source.get('id')] = (list(map(float, array.text.split())), int(accessor.get('stride', 1)))
            vertices = {v.get('id'): next(i.get('source')[1:] for i in v.findall('c:input', ns)
                                         if i.get('semantic') == 'POSITION') for v in mesh.findall('c:vertices', ns)}
            zero_area, repeated = 0, 0
            for primitive in mesh.findall('c:triangles', ns):
                inputs = primitive.findall('c:input', ns)
                stride = max(int(i.get('offset')) for i in inputs) + 1
                position_input = next(i for i in inputs if i.get('semantic') == 'VERTEX')
                offset = int(position_input.get('offset'))
                array, step = sources[vertices[position_input.get('source')[1:]]]
                indices = list(map(int, primitive.find('c:p', ns).text.split()))
                for start in range(0, len(indices), stride * 3):
                    ids = [indices[start + k * stride + offset] for k in range(3)]
                    p = [array[i * step:i * step + 3] for i in ids]
                    if len(set(ids)) < 3:
                        repeated += 1
                    a = [p[1][k] - p[0][k] for k in range(3)]
                    b = [p[2][k] - p[0][k] for k in range(3)]
                    cross = [a[1]*b[2]-a[2]*b[1], a[2]*b[0]-a[0]*b[2], a[0]*b[1]-a[1]*b[0]]
                    if all(v == 0 for v in cross):
                        zero_area += 1
            diffs.append({'mesh': name, 'dae_triangles': triangles,
                          'blend_triangles': imported['triangles'],
                          'source_exact_zero_area_triangles': zero_area,
                          'source_triangles_repeated_indices': repeated,
                          'note': 'Contraste estructural; no demuestra por sí solo causa de omisión'})
        metadata.append({'mesh': name, 'source_triangles': triangles, 'source_lines': lines})
    texture_dir = args.dae.parent / 'model'
    textures = []
    for image in data['images']:
        if image['source'] != 'FILE':
            continue
        path = texture_dir / image['name']
        sha = digest(path) if path.is_file() else None
        textures.append({'image': image['name'], 'source_relative': str(path.relative_to(root_path)),
                         'source_exists': path.is_file(), 'source_sha256': sha,
                         'packed_matches_source': sha in image['packed_sha256'] if sha else False})
    material_names = {m.get('id'): m.get('name') for m in root.findall('c:library_materials/c:material', ns)}
    signatures = collections.defaultdict(list)
    for material in data['materials']:
        signatures[material['exact_node_signature']].append(material['name'])
    empty = [m['name'] for m in data['meshes'].values() if not m['vertices']]
    result = {'source_blend_sha256': data['source_sha256'], 'dae_sha256': digest(args.dae),
              'triangle_differences': diffs, 'source_line_only_geometries': line_only,
              'empty_imported_meshes': empty, 'empty_meshes_match_line_only_ids': set(empty) == set(line_only),
              'packed_textures': textures, 'material_original_names': material_names,
              'identical_inspected_node_signatures': [v for v in signatures.values() if len(v) > 1],
              'notes': ['Firma de nodos compara campos inventariados, no equivalencia completa de shaders.',
                        'No elimina duplicados ni corrige geometría; no evalúa tolerancias de soldado.']}
    target.parent.mkdir(parents=True, exist_ok=True)
    with target.open('x', encoding='utf-8') as stream:
        json.dump(result, stream, ensure_ascii=False, indent=2)
    print(json.dumps({'triangle_differences': diffs, 'empty_meshes_match_line_only_ids': result['empty_meshes_match_line_only_ids'],
                      'packed_textures_matching': sum(t['packed_matches_source'] for t in textures),
                      'packed_textures_total': len(textures)}, ensure_ascii=False))


if __name__ == '__main__':
    main()
