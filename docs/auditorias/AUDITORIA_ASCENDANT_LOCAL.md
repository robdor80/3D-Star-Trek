# Auditoría técnica local del puente USS Ascendant

**Fecha:** 2026-10-10 · **Equipo:** MSI Windows · **Rama:** `audit/ascendant-vs-enterprise`  
**Alcance:** exclusivamente `assets/otros/bridges/USS Ascendant bridge`. Sin comparación de modelos con Enterprise, sin cambio de base oficial ni de canon Theurgy.  
**Herramienta comprobada:** Blender **5.2.2 LTS**, build `d13f752e3b9c`, 2026-09-15; Python `bpy` en procesos background independientes de las sesiones gráficas.

## 1. Resumen ejecutivo

La carpeta contiene **21 archivos, 240.533.569 bytes**: un GLB, un DAE, un ZIP y 18 imágenes JPEG externas. Son **dos representaciones de un puente**, no dos modelos independientes. El ZIP reproduce exactamente el DAE y sus nueve JPG, ya extraídos. El GLB contiene además nueve imágenes embebidas.

El **DAE es la entrada recomendada para editar por conjuntos en Blender**: conserva la jerarquía y geometría compartida. Importa 14.177 objetos, 12.191 MESH y 3.413 bloques de malla únicos; la escena contiene 2.467.116 triángulos al contar todas las apariciones. El GLB importa 88 objetos, 83 MESH y 2.466.519 triángulos, agrupados en grandes mallas con numerosas islas. Es más compacto organizativamente, pero conserva peor la separación funcional original.

Los dos formatos corresponden espacialmente al mismo puente a escala normalizada, pero **no son idénticos en geometría, jerarquía ni materiales**. El DAE declara pulgadas y su importador convierte a metros. El GLB entra como una escena métrica aproximadamente **39,3701 veces mayor**; necesita interpretar sus coordenadas con factor 0,0254 para coincidir con el DAE. Esta auditoría aplica ese factor únicamente a los cálculos; no escala ni guarda transformaciones nuevas sobre la geometría importada.

Las dimensiones según la unidad declarada son **21,354 × 16,301 × 4,560 m**, incluida toda la arquitectura, no solamente espacio pisable. Hay conjuntos seleccionables compatibles por posición, tamaño y repetición con una silla central, diez sillas auxiliares, dos estaciones centrales y la cubierta. Su independencia jerárquica está confirmada; **su identificación funcional sigue siendo probable hasta revisión humana local**.

La cápsula de ensayo encuentra espacios libres, con altura suficiente en varios puntos, pero la prueba es preliminar. No demuestra circulación completa, accesos operativos, navegación NPC ni jugabilidad UE5. Los materiales son básicos: nueve texturas de color, sin mapas PBR de datos, sin emisión activa y con una discrepancia importante de transparencia del suelo.

Se generaron ocho capturas Workbench locales. **No se enviaron renders, modelos ni texturas a servicios externos; no hubo inspección visual por IA.** No se modificó ningún archivo de `assets/`, ninguna escena protegida ni la configuración de Blender. No se realizó commit ni push.

## 2. Evidencia, seguridad y criterios de certeza

Al inicio Git estaba limpio; HEAD `8d1e0f2`, rama obligatoria ya activa. No fue necesario cambiarla. Se leyeron `AGENTS.md`, `README.md`, `.gitignore`, el encargo adjunto y los documentos de diseño/contrato UE5/PBR para respetar las normas vigentes. Los datos geométricos se obtuvieron únicamente de Ascendant. De las escenas protegidas se calcularon hashes, sin cargar su geometría.

Las importaciones usan `--disable-autoexec --background --factory-startup --python-exit-code 1`. Los scripts verifican los 21 SHA-256 fuente antes y después. Las copias nuevas se guardan en `blender/analisis/ascendant_v1/`; nunca en `assets/` ni en la escena maestra. Los diagnósticos posteriores abren esas copias y no las vuelven a guardar. Binarios, capturas y archivos temporales siguen excluidos por `.gitignore`.

**Confirmado:** lectura XML/GLB, metadatos JPEG, hashes, registros `bpy`, índices, coordenadas y pruebas numéricas reproducibles. **Probable:** asignación funcional apoyada en forma medida, posición, repetición y materiales. **Pendiente:** identificación humana de piezas, calidad visual, funcionamiento mecánico, escala arquitectónica real y pruebas en UE5. Una denominación como `GLOW` o `GLASS_FLOOR` no prueba por sí sola una función.

Fuentes de datos locales:

- [Inventario físico y procedencia](ascendant_fuentes_v1/FUENTES_ASCENDANT.json), [CSV de los 21 archivos](ascendant_fuentes_v1/ARCHIVOS_ASCENDANT.csv).
- [Importación GLB](ascendant_bpy_v1/GLB_BLENDER.json), [importación DAE](ascendant_bpy_v1/DAE_BLENDER.json): todos los objetos, padres, matrices, mallas, materiales, imágenes y estadísticas; sin volcar vértices ni caras completos.
- [Contraste de formatos](ascendant_bpy_v1/CONTRASTE_FORMATOS_ASCENDANT.json), [conciliación y conjuntos](ascendant_bpy_v1/CONCILIACION_Y_MODULOS.json).
- [Ensayo de circulación](ascendant_bpy_v1/TRANSITABILIDAD_ASCENDANT.json), [verificación final](ascendant_bpy_v1/VERIFICACION_FINAL.json).

## 3. Inventario físico completo

Raíz relativa de esta sección: `assets/otros/bridges/USS Ascendant bridge/`. Se recorrió el disco, incluidos los recursos ignorados por Git. No hay `.blend`, FBX, USDZ, BIN suelto, animaciones ni documento de licencia independiente en esta carpeta.

```text
USS Ascendant bridge/
├── uss_ascendant_bridge.glb
└── uss-ascendant-bridge/
    ├── source/
    │   ├── USS+ASCENDANT+BRIDGE+FINAL.zip
    │   └── USS+ASCENDANT+BRIDGE+FINAL/
    │       ├── model.dae
    │       └── model/                  [9 JPG; tabla siguiente]
    └── textures/                      [9 JPEG; mismos nombres base]
```

| Archivo relativo | Bytes | Función comprobada |
| --- | ---: | --- |
| `uss_ascendant_bridge.glb` | 110.147.416 | Escena glTF binaria con geometría, materiales y nueve JPEG embebidos |
| `uss-ascendant-bridge/source/USS+ASCENDANT+BRIDGE+FINAL.zip` | 20.805.427 | Archivo con diez miembros: DAE y nueve JPG |
| `uss-ascendant-bridge/source/USS+ASCENDANT+BRIDGE+FINAL/model.dae` | 95.037.334 | COLLADA 1.4.1, jerarquía SketchUp y referencias a nueve JPG |

En la tabla siguiente, **JPG** está en `uss-ascendant-bridge/source/USS+ASCENDANT+BRIDGE+FINAL/model/` y **JPEG** en `uss-ascendant-bridge/textures/`. Cada fila representa dos archivos físicos; dimensiones obtenidas localmente por metadatos, no por inspección visual.

| Nombre base (más `.jpg` / `.jpeg`) | Resolución de ambos | Bytes JPG | Bytes JPEG |
| --- | --- | ---: | ---: |
| `_0e3a929217289.560caa6605fe9` | 1024 × 623 | 244.400 | 244.296 |
| `_58cd499217289.560ca8b44d983` | 1024 × 646 | 234.545 | 234.441 |
| `Blinds_Roman_Hobbled_Blue` | 128 × 256 | 4.097 | 4.935 |
| `GRATE_GLOW` | 1227 × 590 | 192.060 | 191.956 |
| `HONEYCOMB_GLOW_2` | 1643 × 1459 | 2.419.513 | 2.419.409 |
| `Honeycomb_Grate` | 1425 × 1420 | 1.316.493 | 1.316.389 |
| `iso_web_yellow2` | 390 × 806 | 34.913 | 34.913 |
| `NewTrekLCARS` | 2349 × 2099 | 2.726.355 | 2.726.251 |
| `VIEWSCREEN_GLOW` | 1073 × 208 | 99.265 | 99.161 |

Los diez miembros del ZIP tienen los mismos SHA-256 que los diez archivos extraídos correspondientes. Se leyeron los miembros dentro del ZIP, sin extraerlos de nuevo. Entre los archivos sueltos hay un único par idéntico byte a byte: `iso_web_yellow2.jpg/.jpeg`. **Los nueve pares JPG/JPEG tienen píxeles RGB idénticos**, calculados localmente; las diferencias restantes son de contenedor/metadatos. Las nueve imágenes embebidas del GLB difieren de las externas tanto en bytes como en píxeles decodificados.

Este recurso permanece en la **biblioteca auxiliar independiente `assets/otros/`**. Su auditoría no lo incorpora al puente oficial.

## 4. Procedencia y condiciones declaradas

El GLB declara título **USS Ascendant bridge**, autor **Cpt.Kirk**, generador **Sketchfab 17.15.0** según el campo almacenado y licencia **CC BY 4.0**. El valor literal del generador se conserva en el JSON fuente. La [API pública de Sketchfab](https://api.sketchfab.com/v3/models/5c882f022ccd45c285f76321af00da8f), consultada el 2026-10-10 mediante GET de metadatos, confirma autor `CaptainJamesKirk`, licencia CC Attribution con enlace CC BY 4.0 y descarga disponible. Fuente del modelo: [ficha Sketchfab](https://sketchfab.com/3d-models/uss-ascendant-bridge-5c882f022ccd45c285f76321af00da8f).

La API registra publicación `2026-06-06T11:22:50.334633` y las etiquetas `startrek`, `starships`, `startrek-starships`. El DAE registra SketchUp 14.0.1 y creación/modificación `2020-01-10T08:40:42Z`. Esas fechas pertenecen a registros distintos y no prueban cuándo se diseñó originalmente la nave. La descripción del publicador relaciona Ascendant con Vengeance: se registra como afirmación de la fuente, sin certificar canon ni procedencia cinematográfica.

**No aparece NoAI en los metadatos consultados ni en los textos locales inspeccionados.** Esto no equivale a certificar todos los términos históricos, permisos de cada textura o derechos de la franquicia. La ficha HTML devolvió 403; la evidencia disponible es el GLB local y la respuesta pública de la API, sin eludir ese bloqueo.

Según el [resumen oficial CC BY 4.0](https://creativecommons.org/licenses/by/4.0/), la reutilización/adaptación exige atribución, enlace a la licencia e indicación de cambios. No añadir restricciones incompatibles al material licenciado. Antes de distribuir, documentar la cadena de derechos de texturas y otros elementos; la licencia declarada no certifica por sí sola todos los permisos necesarios.

Atribución provisional para uso local: **“USS Ascendant bridge — Cpt.Kirk / CaptainJamesKirk, Sketchfab, CC BY 4.0; importaciones y capturas técnicas locales de diagnóstico.”** Conservar enlaces de fuente y licencia. No se distribuyeron modelos, imágenes ni texturas.

## 5. Importadores y cantidades exactas

GLB: `bpy.ops.import_scene.gltf`, importación de normales, imágenes empaquetadas y `merge_vertices=False`. DAE: extensión **Collada Support 1.2.2**, ya instalada en el perfil Blender 5.2, operador `bpy.ops.import_scene.collada`, `transformation='PARENT'`. Se registró únicamente dentro del proceso de auditoría, usando sus dependencias existentes; no se instaló nada ni se guardaron preferencias.

Blender 5.2 no ofrece aquí el antiguo importador nativo `wm.collada_import`; la importación DAE se comprobó realmente con la extensión. COLLADA **no es glTF**. Un inventariador que solo entienda glTF no sustituye el análisis XML/Collada de esta entrada.

| Medida en Blender | GLB | DAE |
| --- | ---: | ---: |
| Objetos totales | 88 | 14.177 |
| MESH | 83 | 12.191 |
| EMPTY | 5 | 1.985 |
| CAMERA / LIGHT | 0 / 0 | 1 / 0 |
| Bloques de malla únicos | 83 | 3.413 |
| Vértices únicos, incluidos datos sin caras | 3.285.840 | 1.309.590 |
| Vértices contando apariciones de objetos | 3.285.840 | 3.570.430 |
| Caras / triángulos únicos | 2.466.519 | 925.840 |
| Triángulos contando apariciones | 2.466.519 | 2.467.116 |
| Aristas contando apariciones | 5.690.115 | 4.944.218 |
| Bloques de malla compartidos por varios objetos | 0 | 1.810 |
| Objetos que usan malla compartida | 0 | 10.588 |
| Bloques de malla vacíos / objetos con malla vacía | 0 / 0 | 480 / 1.012 |
| Bloques con solo líneas y sin caras | 29 | 0 |
| Bloques con UV / objetos MESH con UV | 9 / 9 | 152 / 714 |
| Bloques sin UV, incluidos vacíos/líneas | 74 | 3.261 |
| Materiales / utilizados por caras | 34 / 21 | 34 / 21 |
| Materiales compartidos entre objetos con caras | 6 | 20 |
| Imágenes cargadas / empaquetadas | 9 / 9 | 9 / 9 |
| Objetos con modificadores / restricciones | 0 / 0 | 0 / 0 |
| Determinante mundial negativo, todos son MESH | 0 | 6.209 |
| Objetos con escala local distinta de identidad | 0 | 588 |

“Únicos” significa bloques de datos una sola vez, no vértices soldados por posición ni geometría evaluada tras optimización. Todas las caras importadas son triángulos. En el DAE la repetición es por varios objetos que enlazan el mismo datablock; no son instancias de colección (`instance_type` distinto de `NONE`). Los EMPTY no son mallas defectuosas: estructuran la jerarquía.

El GLB fuente tiene 1 escena, 88 nodos, 83 meshes, 34 materiales, 9 imágenes, 9 texturas, 229 accessors, 0 animaciones, 0 skins y 0 cámaras. Sus primitivas son **54 TRIANGLES y 29 LINES**. El DAE tiene 3.413 definiciones geométricas y 176 nodos de biblioteca; las instancias de la escena producen muchos más objetos que esas definiciones.

## 6. Diferencias GLB–DAE y conciliación

| Estado | GLB | DAE |
| --- | ---: | ---: |
| Triángulos fuente únicos | 2.466.617 | 925.932 |
| Triángulos fuente expandidos según apariciones DAE | 2.466.617 | 2.467.208 |
| Triángulos tras importar | 2.466.519 | 2.467.116 |
| Descartados automáticamente al importar | 98 | 92 |
| Líneas fuente únicas | 837.173 segmentos GLB | 477.218 segmentos DAE |

El total expandido fuente DAE **2.467.208** coincide con `faceCount` de la API; su `vertexCount` no usa la misma definición que nuestros vértices `bpy` y no se intercambian esas cifras.

En el GLB se comprobaron **98 tripletas de índices duplicadas**, ignorando winding; coinciden con las 98 caras que Blender no conserva. En el DAE:

- `ID11772`, `ID11957`, `ID21920`, `ID22105`: 12 triángulos con índices de vértice repetidos en cada malla; el importador rechaza 48 en total.
- `ID1585`, `ID7076`: seis tripletas duplicadas en cada una. `ID1675`, `ID7166`: 16 en cada una. La validación elimina 44 duplicadas adicionales.

Son efectos de importación sobre copias, no reparaciones aplicadas a archivos fuente. El GLB fuente ya tiene **591 triángulos menos** que el DAE expandido; tras las distintas validaciones la diferencia es **597**. No se ha localizado funcionalmente cada diferencia entre las superficies fuente de ambos formatos.

**Las líneas no son equivalentes a superficies.** La extensión Collada no conserva las primitivas `lines` del DAE: sus 480 definiciones exclusivamente lineales resultan en mallas vacías. El GLB sí conserva 29 mallas de líneas. No concluir que el DAE original carece de esas líneas ni que sus objetos vacíos deban borrarse. Para trabajo arquitectónico pueden ser detalles de dibujo, pero esa función requiere revisión local.

Normalizando solamente los cálculos GLB con 0,0254, las cajas coinciden con diferencias máximas de coordenadas del orden de **micrómetros**. Área triangular expandida, incluyendo solapamientos: GLB **3.375,550539 m²**, DAE **3.375,795102 m²**; no es superficie útil del puente.

Se contrastaron todas las tripletas espaciales, con cuantización de **0,1 mm**, ignorando normales, winding y materiales: **2.255.105 coincidencias** de multiconjunto; 211.414 claves GLB y 212.011 DAE no coincidentes. El redondeo cerca de límites de celda puede cambiar una clave completa aunque la superficie casi coincida. **No interpretar esas claves como caras desaparecidas ni como porcentaje demostrado de pérdida geométrica.** Caja coincidente y área semejante tampoco prueban identidad total. Conclusión: mismo conjunto espacial y texturas semánticas correspondientes, con diferencias verificadas; equivalencia exacta no demostrada.

## 7. Jerarquía y modularidad real

El GLB tiene raíz `Sketchfab_model`, grupo `Collada visual scene group` y 83 mallas llamadas `Material2/3/4/5` con sufijos. **81 de las 83 mallas tienen múltiples componentes**, incluso después de considerar coincidencias exactas de coordenadas como conexión virtual. Sus límites abarcan muchas piezas; el nombre material no identifica una silla o consola completa.

El DAE tiene raíz `SketchUp` y una colección `model.dae` con todos los objetos; no hay colecciones funcionales preparadas. Esquema de subárboles principales, omitiendo nodos intermedios secundarios:

```text
SketchUp
└── group_0
    ├── group_1                  conjunto central (1.744 MESH)
    │   ├── group_2              subgrupo central estrecho
    │   ├── instance_9           conjunto izquierdo (774 MESH)
    │   └── instance_80          conjunto derecho (774 MESH)
    ├── group_11                 cubierta/corona candidata (221 MESH)
    ├── instance_193 → Group_17  silla central candidata (141 MESH)
    ├── instance_89 → ID11615    superficie VIEWSCREEN (1 MESH)
    ├── instance_90 → Component_19      mitad izquierda (5.040 MESH)
    └── instance_199 → Component_19-001 mitad derecha (5.040 MESH)
```

Las dos mitades contienen mobiliario y arquitectura: **no son simplemente “pared izquierda/derecha”**. Los nombres `Group_20` y `group_20` son diferentes; usar nombres exactos e IDs del JSON, no coincidencias aproximadas. Los IDs `ASC-DAE-*`/`ASC-GLB-*` de los informes identifican esta importación y no un canon funcional universal.

| Parte solicitada | Evidencia DAE y separación comprobada | Certeza funcional / límite |
| --- | --- | --- |
| Silla del capitán | `instance_193`: 141 MESH, 137 bloques, 72.280 triángulos; caja 0,984 × 0,873 × 1,327 m, centro (−0,005; 3,913; 1,094) | **Probable** silla central de mando; subárbol independiente confirmado; función “capitán” pendiente |
| Otras sillas | Diez subárboles de 72 MESH / 30.120 triángulos cada uno: dos `instance_75*`, cuatro `instance_185*`, cuatro `instance_187*`; tamaño y geometría repetidos | **Probables** sillas; dos centrales y ocho perimetrales; no contar como identificación visual definitiva |
| Consolas centrales | `instance_9` y `instance_80`: 774 MESH / 726 bloques / 152.112 triángulos cada conjunto; cajas 2,031 × 1,648 × 1,421 m, incluyen candidatos a asiento | **Probables** estaciones; mover el conjunto mueve sus hijos; no afirmar que los 774 objetos son solo una consola |
| Subpiezas centrales | `instance_11` y `instance_11-001`: 12 MESH y 2.586 triángulos cada uno; material Honeycomb y caja 1,44 × 0,79 × 1,02 m | Conjuntos independientes confirmados; cuerpo de consola **probable** |
| Consolas perimetrales | Numerosos objetos con ID1065 (LCARS), integrados bajo grupos de las dos mitades; 618 objetos con caras usan ese material en toda la escena | Superficies independientes confirmadas; estación completa y límites funcionales **pendientes** |
| Pantalla principal | `instance_89/ID11615`: una malla, 160 triángulos, solo ID11616/VIEWSCREEN; caja 17,592 × 3,535 × 2,540 m | Pantalla extendida/curva **probable** por geometría y posición; soporte separado no confirmado |
| Paneles y pantallas auxiliares | 714 objetos MESH tienen UV; LCARS aparece en 618 objetos, con atlas compartido | Independencia de superficies confirmada; cada botón/UI funcional **no** está implementado |
| Suelos | `group_16`, `group_16-001`: 18 MESH / 2.018 triángulos cada uno, ID15235; 17 paneles con uso real de ese material por mitad | Paneles horizontales a niveles medidos: suelo **probable**; estructura y rellenos están en otros objetos |
| Paredes | Objetos separados en mitades de 5.040 MESH, sin colección de paredes y sin etiqueta funcional fiable | Editabilidad de subobjetos confirmada; selección completa de paredes **pendiente** |
| Columnas y soportes | `Component_27*`: cuatro conjuntos de 125 MESH / 7.788 triángulos, altura 2,42 m; distribución perimetral | Función soporte/estructura **posible**, no confirmada por nombre; comparte todos sus 125 bloques fuera del subárbol |
| Techo | `group_11`: 221 MESH / 209 bloques / 15.080 triángulos; rango Z 2,85–3,880 m; geometría sobre toda la planta | Cubierta **probable con evidencia fuerte**; subárbol independiente confirmado, sin mallas compartidas fuera |
| Puertas y accesos | Sin actores, animaciones, restricciones o nombres semánticos que prueben hojas/pasos operativos | **Pendiente** identificación y medición de huecos; una textura o panel no prueba una puerta |
| Barandillas | Hay abundantes objetos pequeños e instancias; no se asignó un conjunto inequívoco mediante análisis numérico | **Pendiente**, sin inferir a partir de un nombre genérico |
| Iluminación arquitectónica | ID444/WHITE_GLOW compartido por 4.386 objetos con caras; HONEYCOMB_GLOW_2 usado en techo y planos inferiores | Superficies candidatas confirmadas; iluminación real **no implementada**, cero LIGHT y emisión cero |

No se movió, renombró, separó ni fusionó ninguna pieza. Un subárbol seleccionable permite transformar sus objetos en una futura copia; **no implica edición exclusiva de sus datos**. La silla central comparte 76 bloques fuera de su subárbol; las sillas auxiliares comparten 61–72 de sus 72 bloques. Editar vértices o un material común podría afectar a otras apariciones. Para cambios exclusivos habrá que decidir qué datablocks copiar, conservando instancias donde convenga. Esta auditoría no realizó esas copias ni cambios.

El DAE ofrece separación mucho mejor para seleccionar conjuntos originales, pero su fragmentación es alta. Una estación contiene cientos de objetos; no constituye un kit de piezas de juego organizado automáticamente.

## 8. Materiales, texturas y PBR

Ambos cargan los 34 materiales, pero solo 21 aparecen realmente en caras. Los otros 13 son materiales asociados a bordes/líneas o slots sin caras; no se califican como corrupción. GLB usa nombres descriptivos de material; DAE mantiene IDs como `ID1065`. La correspondencia ID ↔ nombre fuente está en el inventario.

| Material fuente / DAE | JPG original | Resolución original | Imagen GLB / resolución |
| --- | --- | --- | --- |
| NewTrekLCARS / ID1065 | NewTrekLCARS.jpg | 2349 × 2099 | 0 / 2048 × 2048 |
| Honeycomb_Grate / ID253 | Honeycomb_Grate.jpg | 1425 × 1420 | 1 / 1024 × 1024 |
| _58cd499… / ID6702 | _58cd499217289.560ca8b44d983.jpg | 1024 × 646 | 2 / 1024 × 512 |
| HONEYCOMB_GLOW_2 / ID10365 | HONEYCOMB_GLOW_2.jpg | 1643 × 1459 | 3 / 1024 × 1024 |
| VIEWSCREEN_GLOW / ID11616 | VIEWSCREEN_GLOW.jpg | 1073 × 208 | 4 / 1024 × 128 |
| iso_web_yellow2 / ID15387 | iso_web_yellow2.jpg | 390 × 806 | 5 / 256 × 512 |
| GRATE_GLOW / ID21019 | GRATE_GLOW.jpg | 1227 × 590 | 6 / 1024 × 512 |
| Blinds_Roman_Hobbled_Blue / ID14724 | Blinds_Roman_Hobbled_Blue.jpg | 128 × 256 | 7 / 128 × 256 |
| _0e3a929… / ID21387 | _0e3a929217289.560caa6605fe9.jpg | 1024 × 623 | 8 / 1024 × 512 |

La correspondencia GLB se comprueba por `baseColorTexture.index`, no por ver imágenes. El GLB contiene versiones con resoluciones diferentes en ocho casos y píxeles diferentes en los nueve; no conserva exactamente los JPG originales. El DAE importado empaqueta los nueve JPG con **SHA-256 idénticos a los originales**, preservando su resolución.

Los nueve enlaces de imágenes del DAE fuente resuelven correctamente. La extensión carga los JPG en un directorio temporal propio, los empaqueta y conserva rutas `//textures/*.jpg`. Esas rutas relativas no tienen copia externa junto a nuestros `.blend`; **el archivo empaquetado sí está disponible** y no hay dependencia requerida ausente. Si se desempaquetan en el futuro, habrá que definir el destino explícitamente fuera de `assets/`. No se desempaquetaron ni copiaron texturas durante esta tarea.

Hay 152 bloques DAE y nueve GLB con una capa `UVMap`; **ninguna malla que utiliza una textura de imagen carece de UV**. Las otras superficies usan colores sólidos o son líneas/vacíos; no tener UV no demuestra por sí solo un fallo de apariencia. No hay segunda capa de lightmap preparada, ni validación de solapamiento o densidad de texel.

Diferencias materiales comprobadas:

- GLB: Principled BSDF, metallic **0**, roughness **0,6** en todos los materiales. DAE: fuente Lambert/legacy, convertida por la extensión a Principled, metallic **0**, roughness **1**, Specular IOR Level **0**.
- En ambos, **Emission Strength = 0** y las imágenes están conectadas a Base Color, no a Emission. `WHITE_GLOW`, `VIEWSCREEN_GLOW` o `HONEYCOMB_GLOW_2` no producen emisión por su nombre.
- **GLASS_FLOOR:** GLB alfa ≈ **0,219608** con modo fuente `BLEND`; DAE importado ID15235 alfa **0**. El XML DAE sí contiene alfa difuso **0,2196078**, `transparent opaque="RGB_ZERO"` con color 0,7803922 y `transparency=1`. La implementación instalada invierte ese factor (`1−1=0`) al tratar `RGB_ZERO`; por tanto la discrepancia está en la interpretación de importación, no en ausencia de datos de transparencia en el DAE original. Ambos materiales importados tienen Transmission Weight **0**, render method `DITHERED` y backface culling. No se corrigió el material.
- No hay mapas normal/roughness/metallic/AO/emission asociados. Los nueve JPEG son RGB de color sRGB. Tener nodos Principled no equivale a poseer una biblioteca PBR físicamente calibrada.
- Firmas idénticas de los parámetros/nodos inspeccionados: DAE un grupo de 13 materiales de borde y el par ID444/ID75; GLB un grupo de 15, incluidos bordes/material_0/WHITE_GLOW. Son **candidatos a revisión**, no permiso para deduplicar: la firma no certifica equivalencia visual de todos los estados posibles.

**Qué formato conserva mejor qué:** DAE conserva texturas originales, jerarquía y enlaces de malla; GLB conserva mejor las líneas y una transparencia de vidrio distinta que debe tomarse como referencia técnica. Ninguno conserva un PBR completo ni materiales finales UE5. Para editar el puente elegir DAE, y mantener GLB como contraste de esos atributos.

## 9. Geometría, normales y transformaciones

| Comprobación sobre bloques únicos importados | GLB | DAE |
| --- | ---: | ---: |
| Vértices con coordenadas no finitas | 0 | 0 |
| Caras de área local exactamente cero | 4 | 836 |
| Aristas con una cara, por índices | 2.306.391 | 914.392 |
| Aristas con más de dos caras, por índices | 64 | 0 |
| Aristas compartidas con winding inconsistente | 492 | 40 |
| Mallas con más de una isla considerando coincidencia exacta virtual | 81 | 2 |

Los millones de bordes por índice reflejan en parte la fragmentación y duplicación de vértices en costuras/caras de SketchUp. **No son automáticamente millones de agujeros físicos.** Las conexiones por coincidencia exacta se calcularon virtualmente, sin soldar; no consideran tolerancias arbitrarias. La comparación de winding detecta caras adyacentes con orientación relativa incompatible, pero no certifica que toda normal apunte al exterior.

En DAE, 6.209 objetos MESH tienen matriz mundial reflejada y abarcan 1.226.908 triángulos expandidos. Es resultado de instancias simétricas del origen. Registrar y verificar cómo la futura exportación trata esas reflexiones, normales y backface culling; no aplicar transformaciones a ciegas. El GLB tiene esas transformaciones incorporadas en otra organización y no conserva los mismos vínculos de instanciación.

No hay modificadores, restricciones, rigs o animaciones funcionales. No se comprobaron exhaustivamente autointersecciones, espesor físico, superficies solapadas, origen correcto de bisagras ni todos los normales personalizados. Son aspectos pendientes, sin reparación durante la auditoría.

La complejidad de 2,47 millones de triángulos no proporciona por sí sola un pronóstico de FPS. El DAE reduce datos únicos mediante instancias, pero 12.191 objetos MESH no deben convertirse automáticamente en el mismo número de actores de juego. Organización, slots, piezas móviles y colisiones deberán decidirse antes de optimizar.

## 10. Escala y ensayo preliminar de circulación

### Unidad declarada frente a escala arquitectónica validada

DAE: `<unit meter="0.0254" name="inch">`, `Z_UP`. La importación Collada convierte las coordenadas a metros; escena `METRIC`, `scale_length=1`, `METERS`. GLB: coordenadas que entran en una escena métrica sin esa conversión física. Su caja sin corregir es aproximadamente **840,697 × 641,753 × 179,539 unidades Blender**; la caja calculada con 0,0254 reproduce el DAE. La escena de análisis GLB se guarda tal como entró, **no normalizada**: no usarla para medir personajes directamente sin interpretar esta diferencia.

Caja DAE en metros:

- X: −10,676847 a 10,676850.
- Y: −8,150266 a 8,150264.
- Z: −0,680000 a 3,880298.

La unidad del archivo es verificable; **la escala arquitectónica real de la nave no tiene una cota independiente de autor contrastada**. Los candidatos a sillas y estaciones tienen tamaños plausibles en metros, pero eso solo da coherencia interna. El factor no se dedujo del tamaño deseado del humano ni se usó para reescalar el puente por estética.

### Método local, cápsula y límites

Se construyó una BVH de los triángulos DAE, excluyendo únicamente área ≤ 1e−12 m² de la estructura de consulta, sin borrar caras. Referencias: humano de **1,80 m**; cápsula radio **0,34 m**, altura total **1,76 m** (diámetro **0,68 m**).

Prueba sobre **2.173 posiciones** a separación de 0,40 m. Suelo candidato: rayo descendente desde Z=0,60 m, normal horizontal y nivel próximo a **−0,02; 0,27; 0,43 m** (tolerancia 0,018 m), apoyado en geometría horizontal y paneles medidos. No se aceptan indiscriminadamente todas las superficies horizontales como suelo.

La cápsula se eleva 0,04 m para separar la prueba de obstáculos del contacto de apoyo. Se consultan 19 muestras de su eje y se exige distancia ≥ radio + media separación (**0,37 m**). Esta cota es conservadora para la separación de la cápsula elevada respecto a los triángulos consultados. No simula gravedad, contacto del pie, movimiento ni escalones de Character. Los enlaces de la cuadrícula se comprueban cada 0,10 m, con diferencia de apoyo máxima 0,18 m entre extremos; no equivalen a barrido continuo.

| Resultado de la cuadrícula | Posiciones |
| --- | ---: |
| Libres bajo el criterio conservador | 813 |
| Obstáculo o margen insuficiente | 484 |
| Soporte no identificado como suelo del ensayo | 416 |
| Sin soporte dentro del alcance del rayo | 460 |

El 37,4% de las posiciones son libres en este ensayo; **no es porcentaje de superficie jugable**, porque incluye exterior, zonas no soportadas y niveles excluidos. El grafo produce siete componentes de 410, 317, 32, 26, 26, 1 y 1 puntos. La desconexión puede proceder de niveles intermedios/criterio de cápsula/rasterización; no prueba que una ruta sea físicamente imposible.

### Puntos medidos y anchuras

Orientación analítica provisional: Y negativo hacia la superficie `VIEWSCREEN`; Y positivo hacia la zona posterior. No certifica orientación náutica.

| Punto objetivo X,Y (m) | Apoyo Z | Altura hasta primera superficie superior | Cápsula elevada en posición objetivo |
| --- | ---: | ---: | --- |
| Frente (0; −3) | −0,020 | 3,480 m | Libre en ensayo |
| Detrás de consola izquierda (−1; 2,4) | 0,270 | 3,160 m | Libre en ensayo |
| Detrás de consola derecha (1; 2,4) | 0,270 | 3,160 m | Libre en ensayo |
| Delante de silla central (0; 3) | 0,430 | 3,030 m | Libre en ensayo |
| Detrás de silla central (0; 5,2) | 0,430 | 3,070 m | Libre en ensayo |
| Posterior central (0; 6) | 0,430 | 2,565 m | Libre en ensayo |
| Laterales (±6; 0) | ≈0,250 | No calculada como suelo aceptado | Soporte excluido; no declarar bloqueo |

Los seis primeros puntos superan 1,80 m de altura en su rayo vertical, pero **un rayo no representa todo el volumen humano**. El ensayo de cápsula es una referencia geométrica distinta, no una certificación de animaciones, visión o sentado.

Secciones X entre primeras superficies, a 0,40 / 0,90 / 1,50 m sobre apoyo:

- Frontal en (0; −2,8): **8,331 / 8,331 / 8,331 m**.
- Tras estaciones centrales, Y=2,4: aproximadamente **7,386 / 7,634 / 8,188 m**.
- Detrás de silla central, Y=5,2: **10,780 / 13,061 / 13,152 m**.
- Posterior, Y=6,0: **7,343 / 11,048 / 12,117 m**.

Son anchuras de secciones concretas a alturas concretas, **no ancho mínimo de un corredor completo** ni espacio libre garantizado en el suelo. El JSON conserva las coordenadas de los puntos de cuadrícula utilizados; no sustituirlos silenciosamente por la posición objetivo. Por ejemplo, el punto de cuadrícula libre más próximo a (0; 3) está en (0; 2,4), a distinto nivel.

La zona frontal y los accesos posteriores a las estaciones centrales resultan en componentes distintos del grafo conservador. Los nodos detrás de silla central, posterior y laterales muestreados en (±6,4; 0) comparten componente. Hay potencial para circulación y acceso a puestos, pero **no hay una ruta completa certificada de entrada a cada estación**.

Se observan por geometría horizontal niveles principales −0,02, 0,27 y 0,43 m; saltos acumulados de **0,29 y 0,16 m**. También existen superficies a 0,12 y ≈0,25 m, excluidas de la selección principal. No afirmar que el salto de 0,29 m sea un único escalón: hay que medir las transiciones, alturas y huellas intermedias. La proximidad a una silla no certifica entrada/salida del asiento ni alcance manual de controles.

Para NPC quedan pendientes colisiones reales, parámetros del agente, continuidad de niveles, puertas y puntos de acceso a los puestos. No se generó NavMesh ni se ejecutó UE5.

## 11. Adaptabilidad arquitectónica y preparación UE5

| Posibilidad | Evaluación exclusivamente Ascendant |
| --- | --- |
| Cambiar sillas | Viable por subárboles candidatos independientes; preservar o copiar datos compartidos según alcance de la futura edición |
| Redistribuir estaciones centrales | Hay dos conjuntos seleccionables, con asientos incluidos; requerirá medir nueva circulación y servicios/estructura que puedan intersectar |
| Sustituir cuerpos/pantallas de consola | Existen subpiezas y superficies UV separadas; confirmar mapa funcional, atlas compartido y límites de estación |
| Retirar/desplazar arquitectura | Hay numerosos subobjetos; las mitades principales abarcan arquitectura y mobiliario, por lo que no sirven como unidad segura de demolición |
| Añadir arquitectura o estancias conectadas | Posible como trabajo nuevo sobre derivados; unidad/origen y junta de suelo/techo/colisión aún por definir |
| Ampliar hacia posterior | Zona a Y positivo detrás de silla candidata disponible para estudio; paneles medidos a Y≈6,49 y arquitectura adicional dentro de la caja global. No se confirmó un hueco, puerta ni salida libre existente |
| Mantener circulación realista | Potencial confirmado en puntos; depende de desniveles, colisiones, accesos y ensayo de rutas tras cualquier cambio |

No se afirma que existan Mission Ops, habitaciones conectadas o una extensión posterior lista para usar. No se propuso sustituir el modelo base oficial. La posibilidad de ampliar requiere identificar qué mallas cierran la zona posterior, qué sostienen la cubierta y cómo conectar sin perjudicar los recorridos.

El contrato local [UE5_ESCENARIO_JUGABLE.md](../uss-theurgy/UE5_ESCENARIO_JUGABLE.md) exige escala verificada, módulos/pivotes, colisiones, NPC, consolas/puertas/asientos interactivos y validación en motor. La [biblioteca PBR](../materiales/BIBLIOTECA_PBR_ROBDEV.md) es una propuesta, no materiales ya implementados en Ascendant.

| Requisito | Estado real de Ascendant auditado |
| --- | --- |
| Unidad y orientación registradas | DAE documentado; GLB necesita resolver factor de escala para cualquier futura escena de juego |
| Jerarquía modular | DAE conserva grupos/instancias; faltan colecciones y nombres funcionales |
| Pivotes operativos | Transformaciones inventariadas; bisagras y anclajes funcionales no verificados |
| Materiales PBR y luces | Base Color disponible; emisión, mapas de datos y materiales finales pendientes; cero LIGHT |
| UV para texturas | Presentes donde se usan imágenes; lightmaps/densidad/solapamientos pendientes |
| Colisiones de juego | No hay mallas con contrato de colisión preparado ni ensayo en motor; BVH analítica no es colisión UE5 |
| Puertas, asientos y consolas funcionales | No hay lógica/animación de interacción implementada |
| Navegación NPC | Sin validación NavMesh ni rutas de agente |
| Exportación y rendimiento | Sin prueba de exportación Ascendant a UE5, draw calls, VRAM o FPS |

La documentación oficial confirma distancia por defecto en [centímetros en UE](https://dev.epicgames.com/documentation/en-us/unreal-engine/units-of-measurement-in-unreal-engine). En un futuro ensayo, 1,76 m corresponden a 176 cm, radio 0,34 m a 34 cm y half-height total de cápsula a 88 cm; verificar esas dimensiones tras importar, sin encadenar escalas arbitrarias.

Para colisiones, distinguir [formas simples y geometría triangular compleja](https://dev.epicgames.com/documentation/en-us/unreal-engine/simple-versus-complex-collision-in-unreal-engine), y seleccionar por pieza/función. La [navegación de Epic](https://dev.epicgames.com/documentation/en-us/unreal-engine/basic-navigation-in-unreal-engine) depende de la geometría de colisión: el presente grafo numérico no sustituye ese ensayo. Estas páginas consultadas muestran documentación UE 5.8; la versión de UE5 del proyecto no se verificó ni se presupone instalada en esta auditoría.

## 12. Capturas locales y límite de inspección visual

Ubicación: `output/capturas_revision/ascendant_v1/`. **Ocho PNG, 960 × 720**, Workbench, antialiasing 8; sin renders cinematográficos ni modificación de materiales. [Galería local](../../output/capturas_revision/ascendant_v1/GALERIA_LOCAL.html) y [manifiesto](../../output/capturas_revision/ascendant_v1/MANIFIESTO_CAPTURAS.json).

| Archivo | Diagnóstico previsto |
| --- | --- |
| `01_general_exterior.png` | Perspectiva con cubierta completa |
| `02_cenital_sin_cubierta.png` | Planta; group_11 ocultado temporalmente |
| `03_frontal.png` | Vista desde lado Y negativo, cubierta oculta |
| `04_posterior.png` | Vista desde lado Y positivo, cubierta oculta |
| `05_conjunto_central_aislado.png` | Solo subárbol group_1 |
| `06_silla_central_candidata.png` | Solo subárbol instance_193 |
| `07_zona_posterior.png` | Encuadre posterior, cubierta oculta |
| `08_pieza_perimetral_aislada.png` | Solo subárbol instance_185 |

Se añadió una cámara temporal y se alteró únicamente visibilidad de render en memoria para aislar conjuntos. No se guardaron esos cambios. Las capturas muestran materiales mediante colores Workbench, **no certifican el aspecto de las texturas ni el resultado PBR**. PNG y hashes se verificaron localmente; los contenidos no se enviaron a IA. La lectura humana de estas vistas —silla exacta, soporte, puerta, barandilla, consola— queda explícitamente pendiente, sin afirmar inspección visual realizada por Codex.

## 13. Riesgos, diferencias con una escena de juego y prioridades

1. **Escala GLB inconsistente con DAE declarado.** Resolver en una futura copia documentada antes de exportar o medir personajes. La copia GLB actual es evidencia de importación, no escena de escala corregida.
2. **Material de vidrio diferente, emisión inexistente.** Revisar visualmente localmente la transparencia y definir materiales físicos/interfaz/emisión por separado. No atribuir calidad luminosa a nombres de textura.
3. **Jerarquía fragmentada y datos compartidos.** Catalogar piezas y diseñar colecciones/actores sin convertir cada fragmento en un módulo. Antes de editar, comprobar usuarios de malla y material.
4. **Líneas DAE no conservadas y caras descartadas.** Preservar fuentes y el GLB de contraste; decidir si las líneas tienen una función necesaria. Los vacíos actuales no autorizan eliminación.
5. **Geometría degenerada, winding y simetrías.** Localizar los casos medidos en una copia y comprobar normales/culling al exportar. No reparar automáticamente solo por conteos globales.
6. **Rutas, accesos y desniveles pendientes.** Medir escalones/huellas y posiciones de entrada/salida de estaciones. Completar cápsula y rutas en escena de prueba, con referencias humanas provisionales.
7. **UE5 aún sin implementar.** Exportación piloto con una estación, silla y tramo de suelo; comprobar escala, pivotes, colisiones, NavMesh, interacción y rendimiento antes de extender el pipeline.
8. **Derechos y procedencia.** Conservar atribución/licencia y resolver recursos de terceros antes de cualquier distribución. No inferir autorización de franquicia o texturas únicamente del anuncio.

**Evaluación:** geometría detallada y aprovechable como fuente; modularidad jerárquica fuerte en DAE, organización funcional débil, materiales de color disponibles pero PBR incompleto, automatización `bpy` comprobada, preparación jugable todavía insuficiente. Hay potencial de optimización por instancias existentes y planificación de módulos, pero no se midió rendimiento ni se optimizó. La adaptabilidad arquitectónica es plausible con selección cuidadosa de piezas; no está resuelta por un único objeto “puente”. No se emitió clasificación competitiva frente a otro modelo.

## 14. Próximo paso técnico concreto

**Revisar localmente en Blender la copia DAE y las ocho capturas para confirmar el mapa funcional de los subárboles candidatos**, empezando por `instance_193`, `instance_75*`, `instance_185*`, `instance_187*`, `instance_9/80`, `group_11`, `group_16*` y la zona posterior. Registrar para cada pieza ID, función confirmada, usuarios de malla/material, pivote y entrada/salida requerida. Completar medidas de accesos y niveles intermedios; todavía sin intervención geométrica.

Después de esa identificación, el trabajo recomendado es una copia versionada de prototipo Ascendant para organizar módulos, resolver transparencia/escala y preparar una exportación UE5 pequeña con colisiones y cápsula. Esa fase no se ejecutó aquí.

**Formato recomendado para continuar en Blender: DAE**, mediante la extensión existente, porque conserva grupos, instancias y JPG originales. Usar `blender/analisis/ascendant_v1/ascendant_dae_analisis.blend` como evidencia local de la importación, conservándola intacta y creando otra versión para editar. Mantener GLB como contraste de líneas/materiales; no considerarlos intercambiables sin la conciliación documentada.

## 15. Reproducción y entregables

Scripts nuevos en `scripts/blender_python/`:

- `inventariar_fuentes_ascendant.py`: archivos, ZIP, XML/GLB, imágenes por metadatos/hashes y procedencia pública.
- `auditar_ascendant_blender.py`: importaciones, `bpy`, instancias, topología, materiales, copias y contraste de coordenadas. Reutiliza funciones matemáticas/inventario genéricas existentes; no carga otro puente.
- `comprobar_ascendant_importacion.py`: conciliación de descartes por índices, UV y subárboles seleccionables; `--salida` permite un destino nuevo.
- `medir_ascendant_local.py`: BVH, posiciones de cápsula, rayos y grafo preliminar; no guarda la escena.
- `capturar_ascendant_local.py`: ocho renders Workbench, cámara y visibilidad temporales; no guarda la escena.
- `verificar_ascendant_auditoria.py`: hashes finales, inventario de archivos/carpetas sin cambios, cabeceras PNG, sintaxis, JSON y exclusiones Git.

Los destinos se protegen contra sobrescritura; para repetir usar carpetas nuevas. Comandos de importación, desde la raíz del repositorio, PowerShell:

```powershell
& 'C:\Program Files\Blender Foundation\Blender 5.2\blender.exe' --disable-autoexec --background --factory-startup --python-exit-code 1 --python 'scripts/blender_python/auditar_ascendant_blender.py' -- --fuentes 'docs/auditorias/ascendant_fuentes_v1/FUENTES_ASCENDANT.json' --salida 'docs/auditorias/ascendant_bpy_v2' --escenas 'blender/analisis/ascendant_v2'
& 'C:\Program Files\Blender Foundation\Blender 5.2\blender.exe' --disable-autoexec --background --factory-startup --python-exit-code 1 --python 'scripts/blender_python/medir_ascendant_local.py' -- --escena 'blender/analisis/ascendant_v1/ascendant_dae_analisis.blend' --salida 'temp/ascendant_transito_nuevo.json'
& 'C:\Program Files\Blender Foundation\Blender 5.2\blender.exe' --disable-autoexec --background --factory-startup --python-exit-code 1 --python 'scripts/blender_python/capturar_ascendant_local.py' -- --escena 'blender/analisis/ascendant_v1/ascendant_dae_analisis.blend' --salida 'output/capturas_revision/ascendant_v2'
```

Copias locales, excluidas de Git: `ascendant_glb_analisis.blend` y `ascendant_dae_analisis.blend`. Los informes incluyen hashes y estadísticas, **no copias de binarios, imágenes o texturas**. Los archivos nuevos permanecen sin commit/push para revisión del usuario.
