# Auditoría geométrica Enterprise — fase 2

Fecha: 10 de octubre de 2026, MSI Windows. Fuente: `blender/principal/enterprise_importacion_inicial.blend`. Blender **5.2.2 LTS**. Rama: `audit/inventario-inicial-3d`.

## 1. Resultado y alcance

El puente ya está importado y es seleccionable por piezas y grupos, pero **no está descompuesto íntegramente en componentes funcionales**. Hay mucha geometría compartida, superficies divididas por importación, y arquitectura que integra suelo y paredes. La silla del capitán se identifica con certeza; su respaldo/asiento y sus dos reposabrazos no son piezas mecánicas independientes. La consola central es un conjunto doble: no equivale a dos consolas independientes.

Se leyó la escena guardada, sin reconstruir la importación ni guardar cambios sobre ella. No se renombraron, movieron, separaron, fusionaron o borraron objetos, ni se aplicaron transformaciones. Los renders usan una escena cargada en un proceso independiente y cambios de cámara, color y visibilidad **solo en memoria**, sin guardar .blend. No se examinó visualmente ninguna imagen Theurgy.

Se contrastaron AGENTS, los documentos Theurgy/UE5/PBR/Enterprise y la auditoría inicial. La extensión COLLADA instalada por el usuario y la nueva escena resuelven la dependencia de importación registrada en fase 1. El informe histórico se conserva; véase `ESTADO_IMPORTACION_BLENDER.md` para el estado actual.

## 2. Cantidades: objetos, geometría y auxiliares

| Concepto | Cantidad |
| --- | ---: |
| Objetos de escena / bpy.data.objects | 12.453 |
| Objetos en colección model.dae | 12.451 |
| MESH | 10.721 |
| MESH con vértices | 9.785 |
| MESH sin vértices/caras | 936 |
| EMPTY | 1.729 |
| CAMERA | 2 (una importada; una auxiliar) |
| LIGHT | 1 (auxiliar, fuera del puente) |
| Bloques de malla únicos | 2.526 |
| Bloques de malla compartidos por varios objetos | 1.497 |
| Objetos MESH que usan datos compartidos | 9.692 |
| Vértices de bloques únicos | 1.011.864 |
| Caras/triángulos de bloques únicos | 713.486 / 713.486 |
| Suma de vértices por objetos, contando instancias | 3.118.098 |
| Suma de caras/triángulos por objetos | 2.138.266 / 2.138.266 |
| Materiales | 56: 55 usados y Material sin uso |
| Materiales usados en más de un objeto | 51 |
| Imágenes FILE | 20, todas empaquetadas |
| Imágenes VIEWER auxiliares | 2: Render Result y Viewer Node |
| Objetos con modificadores / constraints | 0 / 0 |

Los aproximadamente 99 meshes del glTF histórico **no describen esta escena COLLADA**. No se equiparan objetos MESH, bloques de malla, grupos EMPTY, zonas funcionales ni componentes del juego.

Todos los objetos tienen `instance_type=NONE`: aquí «instancias» significa **objetos separados que referencian el mismo Mesh datablock**, no instancias de colección. Los EMPTY organizan transformaciones y componentes.

## 3. Organización y jerarquía

Dos colecciones planas: `Collection` contiene Camera y Light auxiliares; `model.dae` contiene los 12.451 objetos importados. El árbol funcional se expresa mediante **parenting**, no mediante colecciones anidadas. Raíces: Camera, Light y SketchUp. `model.dae` es colección, no un objeto raíz adicional.

```text
Scene
├─ Collection: Camera, Light
└─ model.dae [colección]
   └─ SketchUp [EMPTY, raíz]
      ├─ group_0 [EMPTY, 10.457 MESH descendientes]
      │  ├─ group_1 [techo; 222 MESH]
      │  ├─ instance_9 / Component_19 [mitad X negativa; 5.060 MESH]
      │  ├─ instance_124 / Component_19-001 [mitad X positiva; 5.060 MESH]
      │  ├─ instance_8 / ID1471 [pantalla principal]
      │  ├─ instance_125 / Conn [consola doble; 42 MESH]
      │  └─ instance_130 / Group_31-002 [silla delantera X positiva; 72 MESH]
      ├─ instance_131 / Group_31-002.001 [silla delantera X negativa; 72 MESH]
      ├─ instance_132 / Captain_s_Chair_1 [capitán; 15 MESH]
      ├─ instance_133 / Window_Display [3 MESH]
      ├─ instance_134 / Window_Display.001 [3 MESH]
      ├─ instance_135 / Console_2 [11 MESH]
      ├─ instance_136 / Console_2.001 [11 MESH]
      ├─ instance_137 / Group_31-002.002 [silla; 72 MESH]
      ├─ instance_138 / Group_31-002.003 [silla; 72 MESH]
      ├─ ID1 [cámara importada]
      └─ ID21920, ID21928, ID21932, ID21936, ID21940
```

Es un resumen, no sustituye el árbol completo del CSV/JSON. Los nombres se conservaron exactamente. Hay además grupos Group_31 de asientos laterales/posteriores, y familias Component_30 con monitores y consolas; sus puestos departamentales no están asignados.

## 4. Identificaciones funcionales y certeza

**CONFIRMADA:** forma observada en renders Enterprise y evidencia técnica/contextual concordantes, o requisito explícito de nueva construcción. **PROBABLE:** posición, material, simetría y jerarquía concordantes, sin inspección individual concluyente. **PENDIENTE DE VERIFICACIÓN VISUAL:** falta identificar objeto/caras o asignar función exacta.

El mapa conserva 12.453 filas de objetos y **seis filas REQUISITO_SIN_OBJETO** para funciones pendientes/nuevas. Estas seis no aumentan el recuento de objetos Blender. Los IDs `ENT-…` se derivan del nombre original mediante SHA-256 truncado y están vinculados al hash de escena; no son índices glTF. Renombrar objetos o cambiar la escena requiere revisar correspondencias.

La tabla detallada de correspondencias figura al final. Resultados esenciales:

- Capitán: `SketchUp/instance_132/Captain_s_Chair_1`, confirmado, 15 MESH. Mantenerlo.
- CONN/OPS: `SketchUp/group_0/instance_125/Conn`, consola doble confirmada, 42 MESH. **La atribución individual CONN frente a OPS sigue pendiente**; el nombre Conn no identifica por sí solo una mitad.
- Sillas delanteras: instance_131 confirmado como silla junto a la consola; instance_130 probable por simetría y datos. Son grupos transformables separadamente, con 72 MESH cada uno y geometría compartida con otros asientos.
- Consolas frontales laterales: Console_2 confirmado como consola curva; Console_2.001 probable variante simétrica. No asignarlas automáticamente a puestos Theurgy.
- Arquitectura: ID13059 confirmado como mitad que incluye suelo y paredes; ID19639 probable contraparte. Borde ID14178 confirmado y ID20751 probable contraparte.
- Plataforma de mando: superficies alrededor del capitán a z≈0,43, con candidatos ID13285, ID13295, ID19865 e ID19875. Lista de plataforma completa pendiente.
- Pavimento hexagonal/azul: paneles bajos con material ID221/HONEYCOMB_GLOW_2, incluyendo ID13717, clasificados probables por textura y altura. Los renders de diagnóstico son grises; no se afirma haber comprobado ahí el color/patrón. ID221 también aparece en techo. Paneles GLASS_FLOOR son objetos distintos.
- Pantalla principal: ID1471 confirmado, superficie curva frontal Y negativa y textura VIEWSCREEN_GLOW. Window_Display confirmado como display vertical, no identificado como puerta.
- Soporte inclinado: ID1836 confirmado; otras partes/variantes ID1651, ID14508, ID14693, ID1908 e ID14765 probables.
- Techo/anillos: group_1 confirmado; ocultarlo en memoria permite observar interior. No está ausente de este .blend.
- Monitores perimetrales/posteriores: ID11576.001 confirmado como banda curva con NewTrekLCARS; otras bandas de la misma familia probables.
- Cerramiento posterior: marco triangular ID13907 y panel ID13917 confirmados; miembros simétricos/proximales probables. **La selección completa del conjunto azul en X sigue pendiente**: no confundir paneles separados con toda la estructura en X ni asumir que el marco no pertenece a la arquitectura integrada.
- Puertas/accesos: huecos arquitectónicos visibles; hojas, pivotes y operación no identificados. Pendiente.
- Iluminación: geometría/materiales heredados, pero **cero LIGHT en model.dae**. La Light auxiliar no demuestra iluminación funcional del puente. Nombre WHITE_GLOW no demuestra intensidad emisiva ni implementación UE5.

## 5. Independencia y operaciones futuras necesarias

| Elemento | Hecho observado | Operación futura, nunca ejecutada aquí |
| --- | --- | --- |
| Capitán completo | Grupo propio, 15 datos de malla exclusivos | Transformar el grupo en copia; conservar puesto |
| Asiento/respaldo capitán | ID21637 contiene ambos en una superficie conjunta | Selección de caras y separación diseñada si necesitan editarse por separado |
| Carcasa capitán | ID21647 separado de tapicería | Editar en copia; revisar relación con asiento/base |
| Reposabrazos capitán | ID21655 contiene ambos unidos por estructura | Separar por regiones si se requieren brazos independientes; no por islas automáticamente |
| Base capitán | ID21628 candidato inferior separado | Confirmar visualmente antes de tratarlo como pivote/anclaje definitivo |
| Sillas delanteras | Grupos independientes, mallas compartidas | Mover grupo afecta solo a sus objetos; editar Mesh puede afectar otras sillas: copiar datos primero |
| Consola central doble | Conn integra pedestal/cuerpo y ambos puestos | Definir mitad funcional y recortar/separar cuerpo común antes de pretender mover CONN/OPS separadamente |
| Pantallas/controles centrales | Varios objetos texturizados distintos del cuerpo | Identificar caras/pantallas exactas, asignar UI/pivotes; no certificar todos como displays solo por tener textura |
| HONEYCOMB y GLASS_FLOOR | Paneles distintos, por cotas y materiales | Seleccionar panel y borde de forma explícita; material compartido exige instancia/copia según cambio |
| Pared posterior | Parte de arquitectura integrada + paneles/marcos separados | Mapear caras y dependencias, conservar suelo y silla; sustituir solo región aprobada |
| Soporte inclinado | Varias mallas de carcasa/detalle | Seleccionar conjunto completo; comprobar reflejos y normales antes de exportar |
| Techo | Grupo propio de 222 MESH | Mostrar/ocultar conjunto en copia; no eliminar cubierta por confundirla con obstrucción |

Ejemplos de superficies texturizadas de Conn: ID20999, ID21022, ID21056, ID21071, ID21086, ID21096, ID21111, ID21126, ID21136, ID21172, ID21187, ID21197 e ID21207. Enlaces y tamaños constan en el JSON; la función exacta de cada una sigue pendiente. ID20991 abarca aproximadamente 4,080 × 1,935 × 1,023 unidades mundiales, por lo que no es el cuerpo independiente de una sola mitad.

**Conectividad:** 2.138 bloques de malla tienen varias islas por índices/aristas. Sin embargo, conectando **virtualmente coordenadas exactamente coincidentes**, sin soldar ni modificar nada, solo dos bloques conservan dos componentes: ID3473 e ID15247; en ambos el componente extra es un vértice aislado. En los restantes datos no vacíos las aparentes islas se conectan al identificar coordenadas repetidas. Esto evidencia duplicación de índices de importación, **no miles de piezas físicas desconectadas**. No constituye prueba manifold ni excluye geometría que solo se toca en un punto. No usar Separate by Loose Parts como descomposición funcional automática.

Ejemplos: ID21637 pasa de 58 islas por aristas a una por coincidencia exacta; ID21655 de 192 a una; ID13059 de 3.300 a una. Respaldo/asiento, brazos y suelo/pared no se separan mecánicamente por ese criterio.

## 6. Fidelidad de importación y objetos sin geometría

388 bloques de malla vacíos dan lugar a 936 objetos MESH vacíos. El contraste por ID confirma que los 388 corresponden exactamente a geometrías DAE **solo de líneas**. No se presentan como superficies del puente ni como pérdida de 388 muebles. Tampoco se afirma que dichas líneas sean irrelevantes para cualquier revisión futura.

**24 de esos objetos tienen hijos**: actúan como nodos de transformación y se clasifican CONSERVAR. Borrarlos podría afectar a descendientes. Los **912 restantes son hojas vacías**, CANDIDATO A ELIMINAR en una futura limpieza de copia con respaldo y revisión, nunca eliminación realizada.

El DAE fuente suma 713.534 triángulos únicos; Blender 713.486: diferencia de **48**. Se localiza en ID1651, ID1836, ID14508 e ID14693: cada fuente tiene 13.818 y cada malla importada 13.806. Cada fuente contiene exactamente **12 triángulos con índices repetidos y área cero**. La diferencia es consistente con omisión de degenerados; no se ejecutó ni trazó el importador para afirmar causalidad absoluta. No se detecta aquí una diferencia de 48 superficies con área positiva. Recuentos de vértices pueden diferir por tratamiento de líneas/índices; no prueban por sí solos deformación.

## 7. Escala, orientación y transformaciones

Configuración guardada: METRIC, `scale_length=1.0`, longitud METERS. Los números mundiales son unidades de escena que la configuración representa como metros. El DAE declara pulgadas y el cociente de cajas DAE→Blender coincide con **0,0254** dentro del redondeo flotante. Está verificada la **conversión numérica de importación**, no la dimensión física ideal del puente ni la ergonomía del juego.

| Caja global de MESH importados | X | Y | Z |
| --- | ---: | ---: | ---: |
| Mínimo | -10,676847 | -8,150266 | -0,680000 |
| Máximo | 10,676850 | 8,150264 | 3,880298 |
| Extensión | 21,353697 | 16,300529 | 4,560298 |
| Centro de caja | ≈0 | ≈0 | 1,600149 |

Z es vertical. Pantalla principal hacia Y negativa; capitán hacia Y positiva. X distingue lados geométricos: no se asigna babor/estribor sin confirmar orientación náutica. Centro horizontal ≈(0,0), no equivale al pivote de cada pieza ni al centro del suelo útil.

Referencias por caja de conjunto:

- Capitán: centro ≈(0,009; 4,797; 1,048), extensión ≈1,208 × 1,022 × 1,449.
- Conn: centro ≈(-0,038; 0,841; 0,461), extensión ≈4,080 × 2,067 × 1,132.
- Silla delantera X negativa: centro ≈(-1,024; 1,481; 0,686); X positiva ≈(0,949; 1,472; 0,687).
- Console_2 y .001: centros ≈(-2,881; -3,292; 0,295) y (3,021; -3,289; 0,305).
- Plataforma posterior: candidatos horizontales a z≈0,43; HONEYCOMB aparece a cotas -0,11 / 0,18 / 0,34. No todo el pavimento está en una sola cota.
- Techo group_1: z≈2,85..3,8803. Extensión vertical global incluye base por debajo de z=0; no representa altura libre interior.

486 objetos tienen escala local distinta de identidad; **5.363 MESH tienen determinante mundial negativo**, indicando reflexiones heredadas. El capitán hereda escala no uniforme de instance_132 ≈(1,0434; 1,1059; 1,1176). Una malla local con scale=(1,1,1) puede seguir afectada por escala/reflexión de sus padres. Conn tiene determinante mundial ≈2,4863. No se aplicó ninguna transformación ni se invirtieron normales.

Calibración futura: figura de altura explícita (por ejemplo 1,80 m como referencia de ensayo, no medida inferida de un personaje), cápsula/locomoción reales UE5, altura de silla/consolas, puertas, escalones y pasos libres. Comprobar conversión metros→centímetros mediante dimensiones de ensayo y evitar doble ×100/×0,01. Registrar factor global aprobado antes de Mission Ops; no corregir ergonomía deformando un eje a ciegas.

## 8. Texturas, materiales y UV

20 imágenes FILE, todas empaquetadas. **Sus SHA-256 coinciden con las 20 imágenes originales asociadas al DAE.** Ninguna textura requerida falta; las 20 tienen nodos de imagen en materiales. Render Result y Viewer Node son buffers auxiliares, no mapas ausentes.

Las rutas guardadas son relativas, con forma `//textures\nombre.jpg`. Actualmente **cero de las 20 rutas externas resuelven** bajo blender/principal. La escena funciona por los bytes empaquetados; no se debe confundir referencia externa rota con textura perdida. No hay rutas FILE absolutas originales problemáticas. Desempaquetar sin preparar destino o depender después de esas rutas rompería portabilidad.

Los 56 materiales incluyen 55 heredados usados y `Material` sin uso. 51 se comparten entre objetos. Hay familias con idéntica firma de los campos de nodos inventariados (16 materiales de una firma, ID14/ID21638 y ID56/ID99); **no es certificación completa de equivalencia de shaders ni autorización para fusionarlos**. Los IDs del DAE y sus nombres semánticos se conservan en CONTRASTE_DAE_BLENDER.json. ID221→HONEYCOMB_GLOW_2; ID6958→GLASS_FLOOR; ID1472→VIEWSCREEN_GLOW; ID3030→NewTrekLCARS. Un material no identifica un objeto único.

1.350 bloques tienen UVMap; 1.176 no tienen UV, incluidos los 388 vacíos. **Ningún objeto con material de imagen carece de capa UV** según el inventario de slots. Esto acredita presencia, no orientación correcta, ausencia de costuras/solapes o densidad de texel. Asiento/respaldo ID21637 y estructura ID21655 no tienen UV: requerirán estrategia UV si se les aplica cuero u otro mapa nuevo.

Materiales importados usan Principled BSDF y nodos de imagen; todos los mapas FILE están configurados sRGB. Es coherente como estado de importación de imágenes de color, no una biblioteca PBR completa. No se certifican roughness, metallic, normales, transparencia, emisivos o apariencia final UE5. El usuario confirmó previamente texturas visibles; nuestros renders Workbench grises solo validan forma/selección. Las advertencias de espacio de color emitidas al leer buffers VIEWER no correspondían a las veinte FILE sRGB; la lectura use_nodes emite además aviso de obsolescencia futura, sin fallo de auditoría.

Para una futura maestra: conservar copias versionadas, empaquetado y manifiesto de hashes; si se requiere exportar imágenes, hacerlo a carpeta derivada fuera de assets y fijar rutas relativas allí. Revisar materiales compartidos antes de cambios; nuevas instancias UE5 y mapas PBR propios según el contrato y licencias. No desempaquetar ni sustituir ahora.

## 9. Identificación visual reproducible

Se generaron **24 PNG de 960×720, Workbench, AA 8**, sin Cycles: cuatro generales con techo; cuatro con group_1 oculto temporalmente; ocho piezas aisladas; ocho detalles. En las vistas llamadas frontal/lateral la cámara tiene ligera elevación (vectores completos en manifiestos); no son alzados arquitectónicos horizontales puros. Las siluetas generales pueden quedar ocultas por cubierta/paredes; por eso existen vistas sin techo y aisladas. Ningún render modifica el contenido guardado.

Rutas:

- `output/capturas_revision/enterprise_geometria_v1/`
- `output/capturas_revision/enterprise_corte_v1/`
- `output/capturas_revision/enterprise_piezas_v1/`
- `output/capturas_revision/enterprise_detalles_v1/`

Cada carpeta tiene MANIFIESTO_CAPTURAS.json con hash de fuente, cámara, resolución, objetos resaltados y visibilidad temporal. El cian es **resaltado artificial de diagnóstico**, no acabado original. No se ejecutó render masivo ni se mostraron referencias restringidas.

Procedimiento manual en la consola Python de Blender, sobre la misma escena, sin renombrar:

```python
import sys
sys.path.append(r'C:\Users\andro\Documents\GitHub\3D Star Trek\scripts\blender_python')
from inspeccionar_enterprise import seleccionar
seleccionar('Captain_s_Chair_1')
# Equivalente para esta escena:
seleccionar('ENT-9f29509575b8')
```

La función selecciona grupo/descendientes y encuadra vistas 3D disponibles; no mueve, oculta, modifica datos ni guarda. Prueba realizada en background: nombre e ID seleccionaron los mismos **17 objetos (15 MESH + 2 EMPTY)**. El encuadre interactivo se prepara pero no se verificó en la ventana abierta; se omite en el ensayo background. Si una selección no es visible, revisar visibilidad manualmente antes de editar. Seleccionar un EMPTY sin descendientes no resalta por sí solo todas sus piezas.

## 10. Clasificación Theurgy y riesgos antes del modelado

- **CONSERVAR:** silla del capitán; estructura/sillas aprovechables; 24 MESH vacíos con descendientes. No altera jerarquía.
- **POSIBLEMENTE AJUSTAR:** consola doble, arquitectura/suelo, paneles, monitores, techo y sus acabados; validar función/escala primero.
- **POSIBLEMENTE SUSTITUIR:** paneles/marcos posteriores identificados parcialmente. El conjunto X necesita selección exhaustiva y trazado de dependencias con suelo/arquitectura.
- **CANDIDATO A ELIMINAR:** únicamente 912 hojas MESH vacías como propuesta técnica de limpieza futura con respaldo. No se ejecutó eliminación ni se declaró demolición de arquitectura aprobada.
- **CREAR NUEVO:** extensión rectangular Mission Ops y mesa holográfica posterior, requisitos documentados sin objeto fuente. La mesa no es el pavimento holográfico frontal.

Antes de modificar: decidir escala operativa, delimitar caras del cerramiento X, completar asignación CONN/OPS/puertas/luces, verificar single-user para datos que deban variar y preparar UV de tapicería. Los reflejos, geometría duplicada por índices y 10.721 objetos obligan a revisar rendimiento/draw calls/colisiones tras exportar; 2,1 M triángulos no bastan para predecir FPS. El puente no tiene colisiones UE5, Blueprints, pivotes de interacción certificados ni navegación validada.

**Siguiente fase concreta:** copia Blender versionada para calibración funcional y mapa fino del cerramiento posterior/pantallas. Primero referencia humana y ensayo UE5 de escala/circulación; después delimitar operaciones reversibles para la unión de Mission Ops, conservando capitán/suelo. No construir ampliación ni demoler paredes hasta contar con esa selección y validación. La lógica de juego seguirá en UE5, no bpy.

## 11. Scripts, datos y pruebas

Scripts en scripts/blender_python:

1. `auditar_enterprise.py`: inventario completo bpy, jerarquías, transformaciones, cajas exactas por vértices, topología, UV, materiales/imágenes y CSV técnico. Solo calc_loop_triangles en caché; no modifica caras.
2. `contrastar_importacion_enterprise.py`: lectura estándar Python del DAE y comparación de texturas/triángulos/IDs.
3. `inspeccionar_enterprise.py`: selección manual e imágenes Workbench; cámara/color/visibilidad temporales, nunca save.
4. `generar_mapa_enterprise.py`: aplicar anotaciones comprobadas a CSV, con hash de versión y salida nueva.

Los scripts rechazan escribir dentro de assets y evitan sobrescribir salidas. Conservar notas futuras en el mapa enriquecido; **no regenerar encima**. Editar IDENTIFICACIONES_ENTERPRISE.json y producir una nueva versión; no repetir anotaciones inferidas como confirmadas. El mapa actual se completó conservando columnas técnicas y anotaciones, incluida limpieza propuesta de vacíos.

Datos finales en `docs/auditorias/enterprise_bpy_v2/`: AUDITORIA_ENTERPRISE_DATOS.json, CSV técnico base, CONTRASTE_DAE_BLENDER.json y VERIFICACION_FINAL.json. v1 es la corrida preliminar; v2 añade conectividad por coordenadas exactas y optimiza traversal padre/hijo. Son dos fases del análisis, no dos versiones del puente. No reutilizar v1 para conclusiones de independencia. Los JSON detallados son extensos por las 12.453 matrices/rutas/registros, **sin arrays de vértices, caras ni binarios originales**.

Pruebas completadas: lectura real de .blend; inventario final con retorno correcto; sintaxis de cuatro scripts; comparación DAE por IDs; veinte hashes de imágenes; 24 renders terminados y revisión visual de vistas/candidatos Enterprise; selección equivalente por nombre/ID; validación de 12.453 filas técnicas y seis requisitos; hash de escena y 81 activos originales al cierre. No se ensayaron movimiento, edición, exportación, materiales PBR o jugabilidad.

SHA-256 fuente antes/después: **0a55058552623995200fd5e16ddc327d5a6b2f6c54bbb9754f8340d01c885148**. 21.386.736 bytes. 81 activos del inventario anterior comprobados, cero diferencias de contenido o ausencias. No se hizo commit/push. Se conservó la eliminación local previa de output/exportaciones/.gitkeep; no se restauró ni atribuyó a esta fase.

## 12. Tabla de correspondencias verificadas y probables

| Función | Objetos / ruta de ejemplo | Certeza | Evidencia / acción propuesta |
| --- | --- | --- | --- |
| Silla del capitán (conjunto) | `Captain_s_Chair_1, instance_132`<br>Ruta: `SketchUp/instance_132/Captain_s_Chair_1` | CONFIRMADA | Nombre de origen + posición posterior central + render aislado<br>CONSERVAR |
| Tapicería conjunta de asiento y respaldo del capitán | `ID21637`<br>Ruta: `SketchUp/instance_132/Captain_s_Chair_1/group_19/ID21637` | CONFIRMADA | Render aislado muestra respaldo y asiento en un mismo objeto<br>CONSERVAR |
| Carcasa posterior e inferior del capitán | `ID21647`<br>Ruta: `SketchUp/instance_132/Captain_s_Chair_1/group_19/ID21647` | CONFIRMADA | Render aislado de la carcasa<br>CONSERVAR |
| Estructura conjunta y ambos reposabrazos del capitán | `ID21655`<br>Ruta: `SketchUp/instance_132/Captain_s_Chair_1/group_19/ID21655` | CONFIRMADA | Render aislado muestra ambos brazos unidos por estructura<br>CONSERVAR |
| Base/pedestal del capitán | `ID21628`<br>Ruta: `SketchUp/instance_132/Captain_s_Chair_1/ID21628` | PROBABLE | Miembro inferior del grupo; caja z=0.324..0.817 y pedestal visible en conjunto<br>CONSERVAR |
| Consola central doble: conjunto de puestos delanteros | `Conn`<br>Ruta: `SketchUp/group_0/instance_125/Conn` | CONFIRMADA | Nombre de origen + render aislado de consola doble de pedestal común<br>POSIBLEMENTE AJUSTAR |
| Cuerpo/tablero común de consola central (candidatos) | `ID20932, ID20991`<br>Ruta: `SketchUp/group_0/instance_125/Conn/ID20932` | PROBABLE | Descendientes de Conn con extensión transversal común<br>POSIBLEMENTE AJUSTAR |
| Silla delantera lado X negativo | `instance_131, Group_31-002.001`<br>Ruta: `SketchUp/instance_131` | CONFIRMADA | Render aislado + posición junto a consola central<br>CONSERVAR |
| Silla delantera lado X positivo | `instance_130, Group_31-002`<br>Ruta: `SketchUp/group_0/instance_130` | PROBABLE | Jerarquía y patrón de mallas equivalente a silla renderizada; posición simétrica<br>CONSERVAR |
| Sillas de estaciones frontales laterales | `instance_137, instance_138`<br>Ruta: `SketchUp/instance_137` | PROBABLE | Patrón de 72 mallas y posición junto a Console_2<br>CONSERVAR |
| Consola frontal lateral X negativo | `Console_2`<br>Ruta: `SketchUp/instance_135/Console_2` | CONFIRMADA | Nombre nativo y render aislado de consola curva<br>POSIBLEMENTE AJUSTAR |
| Consola frontal lateral X positivo | `Console_2.001`<br>Ruta: `SketchUp/instance_136/Console_2.001` | PROBABLE | Jerarquía y datos compartidos con Console_2; posición reflejada<br>POSIBLEMENTE AJUSTAR |
| Arquitectura de mitad X negativa: suelo y paredes integrados | `ID13059`<br>Ruta: `SketchUp/group_0/instance_9/Component_19/ID13059` | CONFIRMADA | Render aislado muestra suelo, pared periférica, huecos y marco posterior<br>POSIBLEMENTE AJUSTAR |
| Arquitectura de mitad X positiva: suelo y paredes integrados | `ID19639`<br>Ruta: `SketchUp/group_0/instance_124/Component_19-001/ID19639` | PROBABLE | Caja simétrica y jerarquía de la otra mitad<br>POSIBLEMENTE AJUSTAR |
| Borde/contorno elevado de mitad X negativa | `ID14178`<br>Ruta: `SketchUp/group_0/instance_9/Component_19/ID14178` | CONFIRMADA | Render aislado de borde<br>CONSERVAR |
| Borde/contorno elevado de mitad X positiva | `ID20751`<br>Ruta: `SketchUp/group_0/instance_124/Component_19-001/ID20751` | PROBABLE | Posición simétrica al contorno renderizado<br>CONSERVAR |
| Paneles del pavimento con HONEYCOMB_GLOW_2 | `ID13545, ID13565, ID13585, ID13605, ID13625 … (34 objetos; lista completa en CSV/JSON)`<br>Ruta: `SketchUp/group_0/instance_9/Component_19/ID13545` | PROBABLE | Superficies horizontales bajas; material ID221; nodo de textura HONEYCOMB; una muestra aislada<br>POSIBLEMENTE AJUSTAR |
| Paneles GLASS_FLOOR de pavimento | `ID16806, ID16814, ID16822, ID16830, ID16838 … (34 objetos; lista completa en CSV/JSON)`<br>Ruta: `SketchUp/group_0/instance_124/Component_19-001/group_8-001/ID16806` | PROBABLE | Material original DAE GLASS_FLOOR enlazado a ID6958; z por cotas<br>POSIBLEMENTE AJUSTAR |
| Superficies de plataforma posterior de mando (candidatos) | `ID13285, ID13295, ID19865, ID19875`<br>Ruta: `SketchUp/group_0/instance_9/Component_19/ID13285` | PROBABLE | Superficies horizontales alrededor del capitán a z≈0.43<br>CONSERVAR |
| Superficie principal de visualización frontal | `ID1471`<br>Ruta: `SketchUp/group_0/instance_8/ID1471` | CONFIRMADA | Render aislado curvo, posición Y negativa y material con VIEWSCREEN_GLOW<br>POSIBLEMENTE AJUSTAR |
| Display vertical lateral X negativo | `Window_Display`<br>Ruta: `SketchUp/instance_133/Window_Display` | CONFIRMADA | Render aislado de panel vertical con marco superior/inferior<br>POSIBLEMENTE AJUSTAR |
| Display vertical lateral X positivo | `Window_Display.001`<br>Ruta: `SketchUp/instance_134/Window_Display.001` | PROBABLE | Datos compartidos y posición simétrica a Window_Display<br>POSIBLEMENTE AJUSTAR |
| Soporte inclinado perforado | `ID1836`<br>Ruta: `SketchUp/group_0/instance_9/Component_19/group_2/instance_10/Component_101/group_3/instance_16/Group_2-001/instance_12-001/Component_114-001/ID1836` | CONFIRMADA | Render aislado de estructura inclinada<br>CONSERVAR |
| Otras partes/variantes de soportes inclinados | `ID1651, ID14508, ID14693, ID1908, ID14765`<br>Ruta: `SketchUp/group_0/instance_9/Component_19/group_2/instance_10/Component_101/group_3/instance_11/Group_2/instance_12/Component_114/ID1651` | PROBABLE | Geometrías/cajas y familias DAE de soporte; correspondencia simétrica<br>CONSERVAR |
| Techo anular y estructuras superiores | `group_1`<br>Ruta: `SketchUp/group_0/group_1` | CONFIRMADA | Vista completa muestra cubierta; ocultar grupo revela interior<br>POSIBLEMENTE AJUSTAR |
| Superficies superiores texturizadas HONEYCOMB | `ID220, ID475`<br>Ruta: `SketchUp/group_0/group_1/ID220` | PROBABLE | Material ID221 y cotas z≈3.59 / 3.88<br>POSIBLEMENTE AJUSTAR |
| Marco triangular posterior X negativo | `ID13907`<br>Ruta: `SketchUp/group_0/instance_9/Component_19/ID13907` | CONFIRMADA | Render aislado; plano Y≈6.5 detrás del capitán<br>POSIBLEMENTE SUSTITUIR |
| Panel triangular posterior X negativo | `ID13917`<br>Ruta: `SketchUp/group_0/instance_9/Component_19/ID13917` | CONFIRMADA | Render aislado; panel plano interior del marco<br>POSIBLEMENTE SUSTITUIR |
| Otros miembros del cerramiento posterior central | `ID20485, ID20495, ID13927, ID13937, ID13952 … (8 objetos; lista completa en CSV/JSON)`<br>Ruta: `SketchUp/group_0/instance_124/Component_19-001/ID20485` | PROBABLE | Simetría/ubicación Y≈6.49..6.53 y relación con paneles renderizados<br>POSIBLEMENTE SUSTITUIR |
| Banda curva de monitores posteriores | `ID11576.001`<br>Ruta: `SketchUp/group_0/instance_9/Component_19/instance_122/Component_30.001/ID11576.001` | CONFIRMADA | Render aislado de banda y nodo NewTrekLCARS<br>POSIBLEMENTE AJUSTAR |
| Otras bandas de monitores laterales/posteriores | `ID18193.001, ID11576, ID18193, ID11750, ID11750.001 … (7 objetos; lista completa en CSV/JSON)`<br>Ruta: `SketchUp/group_0/instance_124/Component_19-001/instance_122-001/Component_30-001.001/ID18193.001` | PROBABLE | Nodo NewTrekLCARS, geometría y posición de la familia de consolas<br>POSIBLEMENTE AJUSTAR |
| MESH vacío, hoja de jerarquía (fuente solo líneas) | `ID11084, ID11084.001, ID11084.002, ID11084.003, ID11140 … (912 objetos; lista completa en CSV/JSON)`<br>Ruta: `SketchUp/group_0/instance_9/Component_19/instance_60/Component_30/instance_113/Group_31/group_12/group_13/ID11084` | CONFIRMADA | bpy: cero vértices/caras, cero hijos; ID fuente DAE contiene solo líneas<br>CANDIDATO A ELIMINAR |
| MESH vacío con hijos: nodo de transformación | `ID17799, ID17799.001, ID17799.002, ID17799.003, ID17799.004 … (24 objetos; lista completa en CSV/JSON)`<br>Ruta: `SketchUp/group_0/instance_124/Component_19-001/instance_60-001/Component_30-001/instance_74-001/ID17799` | CONFIRMADA | bpy: cero vértices pero hijos existentes; no equivale a elemento prescindible<br>CONSERVAR |
| Mission Ops: extensión rectangular posterior | `THEURGY-Z-020`: SIN OBJETO | CONFIRMADA | Requisito del usuario y diseño maestro; no hay malla fuente correspondiente<br>CREAR NUEVO |
| Mesa holográfica posterior Mission Ops | `THEURGY-MESA-MISSION-OPS`: SIN OBJETO | CONFIRMADA | Nueva construcción, distinta del pavimento holográfico frontal<br>CREAR NUEVO |
| Puertas y accesos operativos | `FUNC-PUERTAS`: SIN OBJETO | PENDIENTE DE VERIFICACIÓN VISUAL | Hay huecos visibles; hojas/pivotes/independencia sin identificar<br>POSIBLEMENTE AJUSTAR |
| Iluminación física/funcional del puente | `FUNC-ILUMINACION`: SIN OBJETO | PENDIENTE DE VERIFICACIÓN VISUAL | Material WHITE_GLOW y otros nombres originales no acreditan emisión funcional; no hay LIGHT en colección model.dae<br>POSIBLEMENTE AJUSTAR |
| Asignación exacta CONN/OPS dentro de consola doble | `FUNC-CONN-OPS`: SIN OBJETO | PENDIENTE DE VERIFICACIÓN VISUAL | Conjunto Conn confirmado; puestos y superficies mecánicas no asignados separadamente<br>POSIBLEMENTE AJUSTAR |
| Selección exhaustiva del cerramiento posterior en X | `FUNC-POSTERIOR-X`: SIN OBJETO | PENDIENTE DE VERIFICACIÓN VISUAL | Paneles identificados parcialmente; falta confirmar pertenencia del marco estructural a mallas integradas<br>POSIBLEMENTE SUSTITUIR |

Detalles individuales, padres/hijos, matrices, materiales, UV y cajas: `enterprise_bpy_v2/AUDITORIA_ENTERPRISE_DATOS.json`. El CSV enriquecido permite seguir verificaciones sin renombrar objetos.
