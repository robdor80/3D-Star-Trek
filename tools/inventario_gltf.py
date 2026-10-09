#!/usr/bin/env python3
"""Inventario NO destructivo de un glTF 2.0 (archivo .gltf o ZIP de Sketchfab).

Uso:
    python tools/inventario_gltf.py "u.s.s._enterprise_a_new_bridge.zip" --salida inventario/kelvin

Solo lee el JSON glTF: no necesita Blender, no extrae texturas y nunca modifica el original.
Los identificadores dependen de los índices del archivo de origen; si se reexporta,
hay que revisar la correspondencia antes de reutilizarlos.
"""
import argparse
import csv
import json
from collections import Counter
from pathlib import Path
from zipfile import ZipFile

FIELDS = [
    "id", "node_index", "nombre_original", "mesh_index", "nombre_malla",
    "materiales", "primitivas", "triangulos_estimados", "hijos",
    "clasificacion", "nombre_funcional", "estado_revision", "observaciones",
]


def cargar_gltf(origen: Path):
    if origen.suffix.lower() == ".zip":
        with ZipFile(origen) as paquete:
            candidatos = [n for n in paquete.namelist() if n.lower().endswith(".gltf")]
            if len(candidatos) != 1:
                raise ValueError(f"Se esperaba un solo glTF en el ZIP; encontrados: {len(candidatos)}")
            return json.loads(paquete.read(candidatos[0]).decode("utf-8")), candidatos[0]
    if origen.suffix.lower() == ".gltf":
        return json.loads(origen.read_text(encoding="utf-8")), origen.name
    raise ValueError("Formato no admitido. Utiliza .gltf o .zip con un .gltf.")


def contar_triangulos(primitiva, accesores):
    if primitiva.get("mode", 4) != 4:  # TRIANGLES
        return 0
    indice = primitiva.get("indices")
    if indice is None:
        indice = primitiva.get("attributes", {}).get("POSITION")
    if indice is None or indice < 0 or indice >= len(accesores):
        return 0
    return accesores[indice].get("count", 0) // 3


def inventariar(documento):
    nodos = documento.get("nodes", [])
    mallas = documento.get("meshes", [])
    materiales = documento.get("materials", [])
    accesores = documento.get("accessors", [])
    filas = []
    for indice_nodo, nodo in enumerate(nodos):
        indice_malla = nodo.get("mesh")
        if indice_malla is None:
            continue
        if not 0 <= indice_malla < len(mallas):
            raise ValueError(f"Nodo {indice_nodo}: índice de malla inválido {indice_malla}")
        malla = mallas[indice_malla]
        primitivas = malla.get("primitives", [])
        nombres_material = []
        for primitiva in primitivas:
            indice_material = primitiva.get("material")
            if indice_material is None:
                nombre = "(sin material)"
            elif 0 <= indice_material < len(materiales):
                nombre = materiales[indice_material].get("name", f"material_{indice_material}")
            else:
                nombre = f"(índice de material inválido: {indice_material})"
            if nombre not in nombres_material:
                nombres_material.append(nombre)
        filas.append({
            "id": f"KELVIN-N-{indice_nodo:04d}",
            "node_index": indice_nodo,
            "nombre_original": nodo.get("name", ""),
            "mesh_index": indice_malla,
            "nombre_malla": malla.get("name", ""),
            "materiales": " | ".join(nombres_material),
            "primitivas": len(primitivas),
            "triangulos_estimados": sum(contar_triangulos(p, accesores) for p in primitivas),
            "hijos": len(nodo.get("children", [])),
            "clasificacion": "POR_IDENTIFICAR",
            "nombre_funcional": "",
            "estado_revision": "PENDIENTE",
            "observaciones": "",
        })
    return filas


def ejecutar():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("origen", type=Path, help="Archivo .zip (Sketchfab) o .gltf")
    parser.add_argument("--salida", type=Path, default=Path("inventario/kelvin"))
    args = parser.parse_args()
    documento, nombre_gltf = cargar_gltf(args.origen)
    filas = inventariar(documento)
    salida = args.salida
    salida.mkdir(parents=True, exist_ok=True)

    with (salida / "mallas.csv").open("w", encoding="utf-8-sig", newline="") as archivo:
        writer = csv.DictWriter(archivo, fieldnames=FIELDS)
        writer.writeheader()
        writer.writerows(filas)

    extras = documento.get("asset", {}).get("extras", {})
    resultado = {
        "archivo_origen": args.origen.name,
        "archivo_gltf": nombre_gltf,
        "asset": extras,
        "resumen": {
            "nodos_total": len(documento.get("nodes", [])),
            "mallas_total": len(documento.get("meshes", [])),
            "objetos_con_malla": len(filas),
            "materiales_total": len(documento.get("materials", [])),
            "imagenes_total": len(documento.get("images", [])),
            "triangulos_estimados": sum(f["triangulos_estimados"] for f in filas),
            "nombres_repetidos": dict(Counter(f["nombre_original"] for f in filas)),
        },
        "mallas": filas,
    }
    (salida / "mallas.json").write_text(
        json.dumps(resultado, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    resumen = resultado["resumen"]
    informe = [
        "# Inventario técnico preliminar",
        "",
        f"- Origen: `{args.origen.name}` / `{nombre_gltf}`",
        f"- Nodos: **{resumen['nodos_total']}**; mallas: **{resumen['mallas_total']}**.",
        f"- Objetos con malla: **{resumen['objetos_con_malla']}**.",
        f"- Materiales: **{resumen['materiales_total']}**; imágenes: **{resumen['imagenes_total']}**.",
        f"- Triángulos estimados: **{resumen['triangulos_estimados']:,}**.",
        "",
        "## Advertencias",
        "",
        "- Un objeto con malla NO equivale necesariamente a una pieza física independiente.",
        "- Los nombres originales pueden repetirse; usar el ID provisional para referenciar filas.",
        "- Los IDs basados en índices solo son estables mientras no cambie el glTF de origen.",
        "- La clasificación semántica y la correspondencia visual requieren revisión en Blender.",
        "- Este script no cambia ni abre el modelo en Blender.",
        "",
        "## Nombres originales repetidos",
        "",
    ]
    informe.extend(
        f"- `{nombre}`: {veces}" for nombre, veces in
        sorted(resumen["nombres_repetidos"].items(), key=lambda x: (-x[1], x[0]))
    )
    (salida / "informe.md").write_text("\n".join(informe) + "\n", encoding="utf-8")
    print(f"Inventariadas {len(filas)} mallas. Resultados en: {salida}")


if __name__ == "__main__":
    ejecutar()
