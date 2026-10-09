# Puente Enterprise — Inventario y edición 3D

> **Objetivo definitivo:** reproducir el puente de la **USS Theurgy NX-79854**, cubierta 01. Ver [diseño maestro y plano de estaciones](../uss-theurgy/DISENO_MAESTRO.md). El nombre "kelvin" de esta carpeta y de los IDs provisionales es heredado de las primeras conversaciones: **no demuestra la procedencia real de la geometría**. Las capturas del modelo descargado parecen corresponder estrechamente al diseño Theurgy; hay que contrastarlo en Blender antes de modificar o recrear piezas.

## Modelo de referencia

- Título del archivo de Sketchfab: **U.S.S. Enterprise A New Bridge**.
- Autor indicado en su metadato: **Cpt.Kirk**.
- Fuente: https://sketchfab.com/3d-models/uss-enterprise-a-new-bridge-a98a3da7570f433684f067c01298ad05
- Licencia declarada en el propio glTF: **CC BY 4.0**. Mantener la atribución al reutilizar o distribuir.
- Entrada recibida: **u.s.s._enterprise_a_new_bridge.zip** (glTF + BIN + texturas).
- El ZIP original no se incorpora todavía a este repositorio. Preservar el original sin cambios.

## Estado inicial, 9 de octubre de 2026

La inspección estructural del glTF incluido en el ZIP confirma:

| Elemento | Cantidad |
| --- | ---: |
| Escenas | 1 |
| Nodos | 104 |
| Mallas | 99 |
| Nodos con malla | 99 |
| Materiales | 55 |
| Texturas / imágenes | 21 / 21 |
| Triángulos aproximados | 2.138.083 |

**Limitación principal:** las 99 mallas reciben únicamente cinco nombres de nodo: `Material2` (55), `Material3` (32), `Material4` (7), `Material5` (4) y `Material6` (1). No se puede deducir qué malla corresponde a un sillón, una consola, el suelo, etc. por su nombre.

El material **GLASS_FLOOR** sí aparece entre los materiales disponibles, aunque todavía no se ha validado visualmente qué superficies utiliza.

## Pruebas previas comunicadas

El 8 de octubre se probaron modificaciones mediante Codex y Blender: cambio de textura/material del respaldo de un sillón y cambio de aspecto del suelo. El usuario confirma que funcionaron. Falta conservar la referencia exacta a los scripts, comandos y objetos de aquellas pruebas; no considerarlos reproducidos ni documentados en detalle todavía.

## Método de trabajo aprobado

1. Guardar el modelo original como maestro inmutable y crear una copia de trabajo `.blend`.
2. Ejecutar `python tools/inventario_gltf.py "u.s.s._enterprise_a_new_bridge.zip" --salida inventario/kelvin` para generar `mallas.csv`, `mallas.json` e `informe.md`.
3. En Blender, visualizar cada malla y asociarle un **nombre funcional** (por ejemplo, SILLON_CAPITAN_RESPALDO), categoría y captura de referencia.
4. Detectar mallas que agrupan varias piezas y piezas formadas por varias mallas; definir subpiezas cuando haga falta.
5. Acordar modificaciones objeto a objeto antes de escribir operaciones destructivas; aplicar cambios en la copia de trabajo y verificar.
6. Guardar scripts reproducibles y un registro de cada modificación (pieza, acción, resultado, versión, captura).

## Precauciones

- Los IDs `KELVIN-N-0002`, etc., proceden del **índice de nodo del glTF original**. Si se reexporta el modelo pueden cambiar; no reutilizarlos sin comprobar la correspondencia.
- Cambiar el material de una malla compartida o una superficie puede afectar a más partes de lo esperado.
- Nunca usar la identidad de un material repetido como identificador único de pieza.
- No hacer `push` automático de modelos/texturas grandes ni sobrescribir el maestro.
- El primer inventario identifica mallas, **no** asegura haber descompuesto el puente en objetos mecánicamente independientes.
