"""Añade identificaciones documentadas a CSV bpy, sin sobrescribir el mapa existente.

python SCRIPT --base CSV --datos JSON --identificaciones JSON --salida CSV_NUEVO
Para futuras sesiones editar identificaciones o añadir notas manuales a una copia
versionada del mapa. No regenerar encima del mapa enriquecido.
"""
import argparse
import csv
import json
from pathlib import Path


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    for name in ('base', 'datos', 'identificaciones', 'salida'):
        parser.add_argument('--' + name, type=Path, required=True)
    args = parser.parse_args()
    root = Path(__file__).resolve().parents[2]
    target = args.salida.resolve()
    if root / 'assets' in target.parents or target == root / 'assets':
        raise RuntimeError('Salida en assets prohibida')
    if target.exists():
        raise FileExistsError('No sobrescribir identificaciones; usar otra salida')
    data = json.loads(args.datos.read_text(encoding='utf-8'))
    config = json.loads(args.identificaciones.read_text(encoding='utf-8'))
    if data['source_sha256'] != config['source_sha256']:
        raise RuntimeError('Identificaciones de otra versión de escena')
    with args.base.open(encoding='utf-8-sig', newline='') as stream:
        reader = csv.DictReader(stream)
        fields, rows = reader.fieldnames, list(reader)
    indexed = {r['nombre_tecnico']: r for r in rows}
    objects = {o['name']: o for o in data['objects']}
    for annotation in config['identifications']:
        for name in annotation['objects']:
            if name not in indexed:
                raise KeyError(name)
            row = indexed[name]
            for field in ('funcion', 'certeza', 'accion_theurgy', 'evidencia', 'captura', 'observaciones'):
                row[field] = annotation.get(field, '')
            row['objetos_relacionados'] = '|'.join(annotation['objects'] + objects[name]['children'])
    for plan in config.get('planned_rows', []):
        row = {f: '' for f in fields}
        row.update(plan)
        row['sha256_escena'] = data['source_sha256']
        rows.append(row)
    with target.open('x', encoding='utf-8-sig', newline='') as stream:
        writer = csv.DictWriter(stream, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)
    print('Mapa:', len(data['objects']), 'objetos reales +', len(config.get('planned_rows', [])), 'filas funcionales sin objeto')


if __name__ == '__main__':
    main()
