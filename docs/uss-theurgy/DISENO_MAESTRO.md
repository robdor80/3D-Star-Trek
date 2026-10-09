# USS Theurgy — Diseño maestro del puente (v0.4)

**Proyecto:** 3D-Models · **Nave objetivo:** USS Theurgy NX-79854 · **Lugar:** Puente principal, cubierta 01  
**Fecha inicial:** 2026-10-09 · **Estado:** Referencia visual + nomenclatura funcional preliminar (sin modificaciones 3D)

> **REQUISITO CANÓNICO UE5:** este modelo no es una maqueta: será un **escenario 3D jugable**, recorrible, con colisiones, puertas, sillas, consolas y mesa holográfica preparadas para interacciones y NPC. Todo el modelado y la exportación deben cumplir el [contrato técnico Blender → UE5](./UE5_ESCENARIO_JUGABLE.md). No cerrar piezas basándose únicamente en un render de Blender.\n\n## 1. Objetivo y premisa revisada

Reproducir y convertir en espacio 3D editable/jugable el puente de la **USS Theurgy**, utilizando como base el archivo de Sketchfab titulado **U.S.S. Enterprise A New Bridge**, que se descargó y analizó previamente.

**Observación crítica:** las capturas de la malla original muestran coincidencias en el **núcleo circular**: patrón angular del pavimento, consolas y soportes inclinados. **NO incluye la ampliación posterior rectangular de la Theurgy**: el usuario lo ha confirmado expresamente. No confundir pequeñas plataformas o consolas elevadas del modelo Enterprise con dicha ampliación. Hay que revisar qué piezas del núcleo son realmente reutilizables.

El objetivo **NO** es rediseñar el núcleo circular desde cero si se puede aprovechar. Sin embargo, la **ampliación posterior rectangular es obra nueva obligatoria** y deberá modelarse e integrarse con el núcleo en Blender. No se debe presentar como una pieza ya existente del glTF.

## 2. Referencias visuales y fiabilidad

El usuario aportó tres referencias el 2026-10-09:

1. **Plano anotado del puente Theurgy (vista en perspectiva superior frontal):** incluye los nombres de puestos, accesos y zonas. Fuente principal para asignar **funciones y posiciones**.
2. **Render desde la parte delantera, mirando hacia el centro y el fondo:** aporta materiales, estilo de iluminación, volumen de techo anular, pantallas, barandillas y niveles. Fuente para **acabados e integración tridimensional**.
3. **Repetición del plano anotado:** refuerza legibilidad de las etiquetas.

La conversación anterior incluye también capturas del modelo en el visor de Sketchfab (alzado superior y perspectivas laterales). Estas referencias están en la conversación; **no se han subido las imágenes al repositorio**.

> La nomenclatura de un puesto en el plano NO identifica automáticamente una malla concreta del modelo Sketchfab. Los mapeos de mallas deberán verificarse visualmente en Blender.

## 3. Orientación del plano anotado

En el **plano de referencia**:

- **Parte inferior:** frente del puente, con la marca **VIEW SCREEN** y la zona de **HOLOGRAPHIC DISPLAY AREA**.
- **Parte superior:** fondo del puente, con puestos de apoyo, puestos de seguridad y conexiones de acceso.
- Las posiciones izquierda/derecha enumeradas a continuación se refieren **a la imagen**, no todavía a babor/estribor (validar orientación náutica del modelo).
- La silla central **CO CHAIR** queda detrás de los puestos CONN y OPS según el eje desde la pantalla frontal.

## 4. Inventario funcional de zonas del plano

| ID funcional provisional | Etiqueta visible en referencia | Ubicación aproximada en plano | Trabajo futuro |
| --- | --- | --- | --- |
| THEURGY-Z-001 | VIEW SCREEN | Borde inferior / proa visual | Identificar superficie o estructura de visualización |
| THEURGY-Z-002 | HOLOGRAPHIC DISPLAY AREA | Suelo central delantero, patrón geométrico | Verificar sistema de material/suelo; decidir efecto holográfico |
| THEURGY-Z-003 | CONN | Frente de isla central, lado izquierdo de imagen | Identificar consola y asiento(s) |
| THEURGY-Z-004 | OPS | Frente de isla central, lado derecho de imagen | Identificar consola y asiento(s) |
| THEURGY-Z-005 | CO CHAIR | Centro, detrás de CONN/OPS | Identificar asiento de mando y piezas del respaldo |
| THEURGY-Z-006 | TACTICAL | Centro-fondo, lado izquierdo de imagen | Verificar estación |
| THEURGY-Z-007 | ENGINEERING | Centro-fondo, lado derecho de imagen | Verificar estación |
| THEURGY-Z-008 | MISSION OPS | Zona media posterior | Delimitar qué estación/paneles conforman la zona |
| THEURGY-Z-009 | SCIENCE | Perímetro lateral izquierdo | Verificar consolas y asientos |
| THEURGY-Z-010 | INTELLIGENCE & COMMUNICATION | Perímetro lateral derecho | Verificar consolas y asientos |
| THEURGY-Z-011 | SUPPORT STAFF | Fondo superior central | Verificar estaciones, pantallas y zona de apoyo |
| THEURGY-Z-012 | SEC POST (varios) | Fondo y laterales superiores | Contar puestos reales tras inspección visual |
| THEURGY-Z-013 | TURBOLIFT (ambos lados) | Laterales de la zona media-posterior | Identificar puertas, vestíbulos y espacio útil |
| THEURGY-Z-014 | CAPTAIN'S READY ROOM | Acceso indicado en el fondo izquierdo | Confirmar si la puerta/sala existe en el mesh |
| THEURGY-Z-015 | SEC CHECKPOINT & ACCESS CONTROL | Acceso indicado en el fondo derecho | Confirmar volumen/puerta y puesto de control |
| THEURGY-Z-016 | Estructuras inclinadas/soportes | Entre el área frontal y estaciones centrales | Separar visualmente de paneles y geometría de suelo |
| THEURGY-Z-017 | Anillo luminoso del techo | Render de interior, zona central superior | Comprobar si está ausente del modelo descargado |
| THEURGY-Z-018 | Banda de iluminación superior | Render, perímetro alto del puente | Comprobar presencia y materiales emisivos |
| THEURGY-Z-019 | Consolas y pantallas posteriores | Render, pared/panel posterior | Comprobar mallas y materiales individuales |
| THEURGY-Z-020 | AMPLIACIÓN POSTERIOR RECTANGULAR | Inmediatamente detrás de la silla del capitán, conectada físicamente al núcleo circular | **CREAR DESDE CERO**; zona operativa nueva con numerosos puestos y mesa holográfica |

**Importante:** las zonas son entidades FUNCIONALES para el juego; no son aún objetos físicos ni identificadores glTF. Una zona puede contener varias mallas, y una malla puede atravesar distintas zonas.

## 4A. Decisión de autor confirmada — ampliación posterior rectangular

**CANON FIJO DEL OBJETIVO:** el puente de la USS Theurgy **NO es exclusivamente circular**. Tiene una **ampliación rectangular en su parte posterior, inmediatamente detrás de la silla del capitán**. No se trata de una sala desconectada: **forma parte integral del puente**, prolonga físicamente su espacio útil y rompe deliberadamente el perímetro circular.

- **En el modelo Enterprise descargado esta ampliación no existe.**
- Por tanto se clasificará como **CREAR NUEVO DESDE CERO**, no MODIFICAR ni RECICLAR.
- Contendrá **múltiples estaciones de trabajo** y **una mesa holográfica**; la distribución exacta, número de puestos y dimensiones se resolverán con las referencias y aprobación del usuario.
- Resolver una **conexión continua y transitable** entre círculo y rectángulo; no superponer una caja sin adaptar suelo, niveles, paredes, acabados y circulación.
- La ampliación se diseñará como **conjunto modular de mallas independientes** (suelo, contorno/estructura, muros, puestos, mesa holográfica, iluminación y cualquier elemento de techo que se confirme), apto para ajustes posteriores.
- **No eliminar ni deformar el núcleo original para simular que la ampliación ya existe.** Construir sobre una copia de trabajo con operaciones reversibles.
- Separar la **mesa holográfica posterior** de la **HOLOGRAPHIC DISPLAY AREA del suelo delantero** (THEURGY-Z-002): son elementos funcionales distintos.
- Pueden existir estructuras elevadas en el núcleo Enterprise; no equivalen automáticamente a esta ampliación.

**Secuencia obligatoria de modelado:** (1) establecer vista ortográfica/escala y punto real de unión al núcleo; (2) dibujar huella rectangular en planta; (3) decidir dimensiones/cota según referencias; (4) construir suelo y conexión; (5) laterales, cierre y soportes; (6) estaciones; (7) mesa holográfica; (8) materiales e iluminación; (9) comprobar accesibilidad, circulación y encaje visual con el resto del puente. El modelado 3D está **pendiente**, no se ha iniciado.


## 4B. Contraste de capturas: Enterprise (origen) vs. Theurgy (objetivo)

**Evidencia visual adicional, 2026-10-09:** capturas del modelo Sketchfab oficial **USS Theurgy Main Bridge (Cut-Away View)** de **Auctor Lucan**, comparadas con capturas del **U.S.S. Enterprise A New Bridge** de **Cpt.Kirk**.

**Referencias del autor:**

- Sketchfab — Theurgy Cut-Away: https://sketchfab.com/3d-models/uss-theurgy-main-bridge-cut-away-view-531b845d47da49a3840f402ab371c49e
- Sketchfab — Theurgy Main Bridge: https://sketchfab.com/3d-models/uss-theurgy-main-bridge-7caf2057deab4383ab4d43ca7f10490e
- Galería y explicación de Auctor Lucan: https://auctorlucan.artstation.com/projects/weNzw
- Modelo de partida Enterprise: https://sketchfab.com/3d-models/uss-enterprise-a-new-bridge-a98a3da7570f433684f067c01298ad05

**Confirmaciones:**

1. **La silla central posterior es la del capitán. Se conserva en su lugar y con su protagonismo visual.** Nunca incluirla en el grupo de demolición.
2. En **Enterprise**, el elemento que estorba al nuevo diseño es el **cerramiento trasero de aspecto azul, con estructura en X**, por detrás de la silla; debe estudiarse la separación de mallas para sustituirlo por el espacio Theurgy.
3. En **Theurgy**, **detrás de la silla del capitán** se reconoce una **gran mesa holográfica horizontal azul**, flanqueada por estaciones y respaldada por una **bancada curva de monitores**. **La mesa azul de Theurgy SE CONSTRUYE y SE CONSERVA en el diseño final; no confundirla con el fondo azul del Enterprise que se retira.**
4. Según Auctor Lucan, la ampliación es **Mission Ops Center**, destinada a coordinar operaciones y unidades de cazas; incluye mesa táctica holográfica. Verificar el contorno exacto desde planta antes de construir su huella.
5. La secuencia funcional objetivo queda: **CONN/OPS → silla del capitán → área integrada de Mission Ops con mesa holográfica y puestos/pantallas posteriores**. La circulación real debe calcularse, no bloquearla con geometría nueva.

**Derechos y límites de las referencias Theurgy:** las fichas de Auctor Lucan identifican el modelo como **NoAI** y lo describen como obra propia con condiciones restrictivas, entre otras el uso no comercial con atribución. Las capturas y enlaces sirven de **referencia visual y documental**; NO incorporar/importar el modelo 3D del autor, ni sus texturas, ni pasarlo a herramientas de IA/Codex, ni distribuirlo o publicarlo como recurso del proyecto sin obtener permiso explícito. No consta un botón de descarga oficial para ese modelo. El ZIP Enterprise de Cpt.Kirk es otro recurso con licencia distinta.

## 5. Identidad visual observada

- Base grafito/gris oscuro y paneles grises; superficies principales sobrias.
- Suelo con **geometría angular y líneas claras**, con grandes polígonos oscuros en la zona holográfica frontal.
- Pantallas y acentos azul-cian.
- Tiras de iluminación blanca en pilares, paramentos, barandillas y perímetro superior.
- Render de interior: **techo anular concéntrico** con luminarias y elementos azulados.
- Isla de mando central con consolas CONN/OPS y un asiento de mando detrás de ellas.
- Diferentes cotas/plataformas, no asumir que todo está a un solo nivel.
- Debe diferenciarse la **estructura física** del puente de las **interfaces funcionales** que se diseñarán para el RPG.

Estos rasgos son **referencias de acabado**, no especificaciones de RGB, dimensiones ni geometría exacta.

## 6. Hipótesis: modelo Sketchfab vs. diseño Theurgy

| Elemento observado | Coincidencia visual preliminar | Acción |
| --- | --- | --- |
| Perímetro circular principal | Alta | Comparar planta con cámara ortográfica |
| Suelo delantero con trama geométrica | Alta | Superponer capturas, comparar bordes y proporciones |
| Dos grandes soportes inclinados | Alta | Localizar mallas y validar simetrías |
| Pequeñas plataformas del núcleo circular | Aparente | Revisar reutilización; **no confundir con ampliación rectangular** |
| Extensión posterior rectangular Theurgy | **Ausente del modelo Enterprise — confirmado por el usuario** | **MODELAR DESDE CERO** con múltiples puestos y mesa holográfica |
| Consolas perimetrales laterales | Aparente | Contar módulos y ubicaciones |
| Estaciones CONN/OPS y silla del CO | Aparente | Identificar piezas y verificar distribución |
| Techo anular y iluminación superior | Desconocida | Comprobar si existen en glTF o son solo del render |
| Puertas y zonas fuera del área visible | Desconocida | No inventar: comprobar geometría y referencias |

**Regla de decisión:** si una pieza del **núcleo circular** ya coincide geométricamente, conservarla. La ampliación posterior rectangular es la **excepción explícita**: debe crearse de cero.

## 7. Flujo técnico cuando volvamos al MSI

1. Vincular la app ChatGPT del MSI con Codex Remote en el Realme (cuando esté disponible).
2. Sincronizar `robdor80/3D-Models` y conservar el ZIP glTF de referencia en almacenamiento local, sin subirlo automáticamente.
3. Importar el glTF a **una copia de trabajo de Blender**; registrar versión de Blender y parámetros de importación.
4. Ejecutar `tools/inventario_gltf.py` y conservar artefactos de salida del modelo original.
5. Hacer capturas **ortográficas superior, frontal y laterales** del modelo actual. Compararlas con las referencias aportadas; no cambiar nada todavía.
6. Enlazar cada zona THEURGY-Z-### con uno o más IDs del glTF (KELVIN-N-####, nombre provisional legado), y documentar certeza y captura.
7. Identificar cada objeto real como **CONSERVAR / AJUSTAR / SUSTITUIR / ELIMINAR / CREAR**, justificando la operación; no aplicar cambios sin revisión.
8. Probar cambios de material, traslado y edición por piezas en copias de trabajo, usando `bpy` y scripts versionados. Registrar pruebas y capturas.
9. Diseñar la huella, unión y dimensiones de THEURGY-Z-020 con validación del usuario; construirla de cero **en módulos independientes**; dejar la mesa holográfica y los puestos para después de validar la arquitectura.

## 8. Reglas de conservación / versionado

- El original Sketchfab queda **inmutable**.
- No borrar ni fusionar mallas de forma irreversible sin una copia recuperable.
- Mantener la referencia de los autores/licencias del modelo y de las imágenes al distribuir el resultado; revisar permisos antes de publicar assets derivados.
- Separar **IDs técnicos** (mallas/nodos del glTF) de **IDs funcionales** (zonas del puente).
- No inferir medidas físicas ni inventar estaciones no visibles en los documentos.
- Los nombres heredados `kelvin` en rutas y IDs de herramientas son temporales y **no acreditan que la geometría provenga del puente Kelvin**.

## 9. Próximo entregable

**MAPA DE CORRESPONDENCIA**: tabla zona funcional -> mallas reales -> captura de identificación -> estado de modificación. Para THEURGY-Z-020 la referencia será **SIN MALLA / NUEVA CONSTRUCCIÓN**, porque no existe en el modelo origen. Primer hito verificable en el MSI, antes de cualquier edición estructural.
