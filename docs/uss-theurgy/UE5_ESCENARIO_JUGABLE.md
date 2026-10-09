# USS Theurgy — Contrato técnico Blender → Unreal Engine 5 (v0.1)

**Proyecto:** 3D-Models  
**Destino obligatorio:** escenario **3D jugable** del puente de la USS Theurgy (UE5), no maqueta ni render estático.  
**Estado:** reglas técnicas de diseño aprobadas en conversación el 2026-10-09. Las dimensiones y ajustes concretos se validarán en Blender y en una escena de prueba UE5.

> **Biblioteca de materiales reutilizable:** ver [RobDev Material Library — PBR Star Trek](../materiales/BIBLIOTECA_PBR_ROBDEV.md). Los materiales físicos y los gráficos de interfaz se mantendrán separados para poder reutilizarlos en futuras estancias y naves.

## 1. Objetivo

Construir un puente recorrible en primera y/o tercera persona, que admita NPC, asientos, puertas, consolas funcionales, efectos holográficos, sistemas de juego y futuras revisiones de materiales y geometría. Se tomará el puente Enterprise como base, conservando el maestro original, y se diseñará una ampliación trasera tipo Mission Ops desde cero, según el diseño maestro. **Se validarán las licencias de todos los recursos antes de usarlos o distribuirlos.**

La prioridad operativa es **funcionalidad y mantenibilidad**, además de fidelidad visual. La aprobación de un render en Blender **no basta** para dar por terminada una pieza del juego.

## 2. Convenciones de escala, orientación y origen

- **Unreal Engine trabaja por defecto con centímetros** (1 Unreal Unit = 1 cm); **Blender suele trabajar en metros**. Definir en una hoja de importación la conversión real y verificar dimensiones de una puerta/asiento/personaje de prueba en UE5. No aplicar factores de escala a ciegas.
- Registrar ejes/orientación de exportación, transformaciones aplicadas, escala real del modelo y punto de origen. Evitar cambios sucesivos de escala que alteren colisiones o animaciones.
- Usar una referencia humana y un **Character** de prueba para confirmar altura libre, visión desde la silla, ancho de pasos, escalones y circulación. No se fijan dimensiones ficticias hasta medir el mesh original.
- Los pivotes de piezas móviles deben permitir la operación: bisagra en puerta, centro de giro en silla, anclaje coherente en consola; origen global consistente para módulos estáticos.

## 3. Arquitectura modular de la escena

Separar y nombrar de forma estable, **cuando técnicamente sea posible**, los elementos que deban interactuar o cambiar de forma independiente:

- `BRG_FLOOR_*`, `BRG_WALL_*`, `BRG_FRAME_*`, `BRG_CEILING_*`: estructura.
- `BRG_DOOR_*`: hoja(s), marco, mecanismo, punto de acceso.
- `BRG_CONSOLE_*`: cuerpo, pantalla, botones/superficies de interacción.
- `BRG_CHAIR_*`: respaldo, asiento, base, puntos de sentarse y levantarse.
- `BRG_HOLO_*`: base física y proyección/volumen holográfico por separado.
- `BRG_LIGHT_*`, `BRG_DECOR_*`: iluminación, accesorios y detalles.

No fusionar puertas, consolas, sillas o elementos animables con grandes mallas de suelo por comodidad. La unión arquitectónica de zonas no exige que sean una única malla: debe evitarse que el jugador vea huecos o sufra bloqueos de colisión.

Usar IDs técnicos del archivo glTF para el inventario de origen y **nombres semánticos** para piezas finales: conservar una tabla de correspondencias. No asumir que las 99 mallas originales equivalen a 99 objetos jugables.

## 4. Colisiones y circulación

- Todo suelo pisable necesita colisión estable; paredes, columnas, barandillas y consolas tendrán colisiones adecuadas, evitando bloquear una zona por detalles decorativos invisibles.
- Definir colisiones simples donde sea viable; recurrir a geometría más detallada solo cuando haga falta y validar coste/compatibilidad en UE5.
- Dejar huecos reales para puertas y accesos a Mission Ops. Una textura de puerta no equivale a un paso transitable.
- Comprobar los escalones, rampas, superficies curvas, zonas elevadas y continuidad de suelo en el empalme **núcleo circular ↔ ampliación rectangular**.
- Preparar navegación de NPC en UE5 mediante `NavMesh` y puntos de acceso/salida a los puestos, comprobando que no atraviesan estaciones ni tropiezan con la mesa holográfica.
- Definir el perfil real de cápsula del personaje antes de fijar definitivamente los anchos de circulación.

## 5. Actores interactivos del futuro juego (UE5)

Las piezas gráficas y las lógicas son capas distintas:

| Elemento | Malla(s) Blender | Comportamiento previsto UE5 |
| --- | --- | --- |
| Consola Sensores / Ciencia / Táctica / Ingeniería / CONN / OPS | Estructura, pantallas, mandos por piezas | Actor o Blueprint de estación: interacción, bloqueo/ocupación, interfaz funcional y datos del juego |
| Sillón capitán y otros | Malla de sillón, anclaje | Sentarse, levantarse y orientarse; puntos de entrada y salida |
| Puerta | Hoja(s), marco, punto de pivote | Abrir/cerrar, estado, permisos de acceso, colisión y navegación |
| Mesa de Mission Ops | Mesa física, volumen/proyección separado | Proyección de mapa/objetivos; interacción; estado dinámico |
| Pantalla principal | Soporte y plano/superficie visible | Material dinámico o interfaz actualizable según la simulación |
| Iluminación de alarma | Mallas/soportes y emisivos | Cambio de estado desde UE5 según alertas, daños o emergencias |

**No implementar la lógica de juego dentro de scripts `bpy`.** Blender prepara geometría, UV, materiales base, pivotes y metadatos; **Blueprints/C++ en UE5** gestionarán controles, simulación, interacción y estados persistentes.

## 6. Materiales, UV y rendimiento

- Mantener materiales organizados por propósito: suelo, metal, cristal, emissive, pantalla, holograma.
- Evitar modificar indiscriminadamente materiales compartidos si cambian objetos ajenos. Para estados dinámicos preferir materiales parametrizados e instancias en UE5.
- Corregir normales, geometría invertida y UV. Si se opta por iluminación horneada, preparar UV de lightmaps sin solapamientos; con Lumen no asumir automáticamente que el horneado es necesario.
- Considerar Nanite para piezas estáticas compatibles y apropiadas, **no** como solución universal para cualquier objeto o efecto; decidir tras importar y perfilar.
- Valorar cantidad de draw calls, triángulos, materiales, luces dinámicas y transparencias; utilizar instancias, LOD o simplificación cuando resulte útil.
- No convertir todas las pequeñas pantallas en texturas gigantes: reservar resolución en función de tamaño en pantalla y distancia de cámara. Registrar atribución/licencias de los assets fuente.

## 7. Pipeline de ida y vuelta

1. **Maestro inmutable**: archivo original Enterprise con licencia, procedencia y ZIP/GLTF/BIN/texturas preservados.
2. **`Blender_Working`**: archivo `.blend` de edición con módulos y colecciones estructuradas; numerar versiones antes de cambios destructivos.
3. **Inventario**: malla del origen ↔ ID técnico ↔ pieza funcional ↔ acción (`CONSERVAR`, `MODIFICAR`, `OCULTAR`, `SUSTITUIR`, `CREAR`).
4. **Exportación de prueba**: empezar con FBX o glTF según importador y comportamiento validado en la versión concreta de UE5. Registrar versión, opciones y nombres; **no presumir que todos los pivotes, materiales o colisiones sobrevivirán automáticamente**.
5. **`UE5_Prototype`**: mapa de ensayo con Character, colisiones, navegación, prueba de asiento, puerta, consola y mesa holográfica.
6. **Control de calidad**: volver a Blender si hay problemas de escala, mallas, iluminación o colisión; no parchear arbitrariamente en los dos programas sin registrar la fuente de verdad.
7. **Repositorio**: subir scripts, documentación, correspondencias, parámetros, capturas y manifiestos. Los modelos grandes y derivados se guardarán en almacenamiento adecuado con política explícita de Git LFS/adjuntos y licencias, **no se añadirán automáticamente al Git convencional**.

## 8. Pruebas de aceptación UE5 por fase

**Hito A — Escenario vacío recorrible**
- El jugador puede andar por todo el suelo del núcleo, sin atravesarlo ni atascarse.
- El empalme a la extensión Mission Ops permite tránsito continuo, sin escalón invisible ni cierre posterior bloqueante.
- Las dimensiones relativas de puestos y jugador resultan coherentes.

**Hito B — Mobiliario**
- Las consolas y sillas siguen siendo piezas editables/movibles cuando proceda.
- Las colisiones no invaden injustificadamente el espacio de circulación.
- Los NPC disponen de rutas y posiciones accesibles.

**Hito C — Interacciones**
- Una consola seleccionada abre el flujo de interacción real.
- La puerta se abre, deja pasar y vuelve a bloquear al cerrarse.
- El sillón del capitán admite interacción de sentarse/levantarse.
- La mesa holográfica muestra un estado actualizable.

**Hito D — Presentación y rendimiento**
- Materiales, iluminación, transparencia y pantallas se ven bien **dentro de UE5**, no solo en Blender.
- Se revisa rendimiento en el hardware de destino y se decide qué optimizaciones hacen falta.

La definición de completado de cada hito exige **evidencia en UE5** (captura, vídeo corto o prueba reproducible). Mientras no haya prueba en el motor, se considerará **pendiente de validación**.

## 9. Condiciones de trabajo con Codex

- Codex debe leer esta especificación y el `DISENO_MAESTRO.md` **antes** de generar/modificar scripts `bpy`.
- Trabajar sobre copias, mediante cambios auditables; preferir ocultar/deshabilitar antes de borrar irreversiblemente.
- Mantener un `CHANGELOG` técnico con cada lote de objetos afectados y capturas.
- Distinguir claramente entre **editar la malla Blender** y **implementar el comportamiento en UE5**.
- No declarar «listo para UE5» basándose únicamente en que la pieza existe en el visor de Blender.

## 10. Cuestiones abiertas

- Versión concreta de Blender y UE5 del proyecto.
- Modelo de locomoción del personaje y dimensiones de su cápsula.
- Escala física real del archivo de origen y sus unidades.
- Descomposición real de las mallas Enterprise y alcance de las piezas reutilizables.
- Resolución/tamaño final de los recursos, elección de iluminación y presupuesto de rendimiento según pruebas.
- Diseño final (medidas, malla, número de puestos) de Mission Ops.

**No inventar estas respuestas: medir y acordar antes de cerrar geometría definitiva.**

## Anexo A — Medición real del glTF Enterprise (2026-10-09)

**Medición efectuada leyendo todos los vértices POSITION del archivo `u.s.s._enterprise_a_new_bridge.zip`**, incluyendo las transformaciones de los nodos en su árbol de escena (raíz Sketchfab con conversión de ejes).

| Eje geométrico | Extensión numérica original |
| --- | ---: |
| Ancho (X) | **840,6967 unidades** |
| Fondo (Z en glTF, profundidad horizontal) | **641,7532 unidades** |
| Alto (Y en glTF, vertical) | **179,5393 unidades** |

Caja envolvente global de todas las mallas; no es el diámetro útil transitable ni garantiza espacio libre interior. Se inspeccionaron **3.157.194 vértices** referenciados por las primitivas de mallas del glTF. El nodo raíz incorpora una rotación de ejes; el modelo no contiene una escala normalizadora que convierta a metros.

**ALERTA — escala física SIN CONFIRMAR:** glTF especifica metros como unidad lineal, pero las cifras numéricas brutas de esta conversión Sketchfab/Collada no son plausibles como metros reales (≈841 m de ancho). No usar el tamaño importado sin calibración. No asumir que los archivos exportados de Sketchfab respetan la intención de escala del autor.

**Hipótesis inicial, NO VERIFICADA: coordenadas en pulgadas originales** (`1 unidad fuente ≈ 0,0254 m`):

| Eje | Tamaño si fueran pulgadas |
| --- | ---: |
| Ancho | ≈ **21,35 m** |
| Fondo | ≈ **16,30 m** |
| Alto | ≈ **4,56 m** |

Si fueran centímetros en vez de pulgadas, serían 8,41 m × 6,42 m × 1,80 m, por lo que el techo/silla probablemente quedarían subdimensionados. Ninguna hipótesis constituye evidencia de la escala del archivo.

### Calibración obligatoria antes del modelado Theurgy

1. Abrir **copia** del modelo en Blender y comprobar la caja de dimensiones globales.
2. Construir una referencia de 1,80 m de altura y comparar visualmente con **silla del capitán, altura de puertas y consolas**, sin asumir de antemano que alguna mide exactamente una cifra.
3. Verificar distancias transitables y alturas respecto al controlador de personaje UE5 y su cápsula. Registrar decisiones y capturas.
4. Ajustar **uniformemente** la escena original (o geometría exportada) hasta obtener proporciones físicas creíbles. No escalar solamente un eje ni deformar mobiliario.
5. Congelar y documentar el factor fuente→metros→centímetros de UE5 antes de crear la ampliación rectangular; **Mission Ops deberá modelarse en esa misma escala**.
6. Hacer una importación temprana a UE5 para comprobar medidas reales con un Character de prueba; no declarar confirmada la escala hasta entonces.

La conversión glTF→Blender→FBX/glTF→UE5 debe documentar todas las escalas y evitar doble factor ×100 o ×0,01.

## Anexo B — Metadatos de Sketchfab confirmados en capturas (2026-10-09)

Fuente: ficha **U.S.S. Enterprise A New Bridge** de **Cpt.Kirk** en Sketchfab, aportada por el usuario en capturas (sección «Model Information» y «All files»).

| Campo Sketchfab | Valor mostrado |
| --- | --- |
| Licencia | CC Attribution |
| Formato de origen | Collada (`.dae`) |
| Tamaño de fichero DAE | 80 MB, en listado «All files» |
| Tamaño de descarga del original | 25 MB, posiblemente descarga comprimida; no equiparar ambos valores |
| Triángulos / vértices | 2,1 M / 1,8 M (cifras redondeadas del visor) |
| Materiales | 55 |
| Texturas | 21 |
| PBR | **No** (según ficha del modelo) |
| Formatos convertidos ofrecidos | glTF, USDZ, GLB |

Se observan resoluciones muy variables en las texturas, por ejemplo `NewTrekLCARS` **2349×2099**, `HONEYCOMB_GLOW_2` **1643×1459**, `VIEWSCREEN_GLOW` **1073×208**, y otras como `material_4` **21×21** o `material_3` **167×86**. La resolución de un archivo no demuestra por sí sola su calidad o defecto: depende de la zona y uso de la textura.

**Consecuencias para UE5:**

- Preparar revisión/adaptación de materiales hacia el flujo PBR de Unreal (Base Color, Roughness, Metallic, Normal cuando corresponda, emisivos de pantallas/luminarias), sin interpretar el campo `PBR: No` como ausencia total de materiales.
- Identificar UV y texturas heredadas; distinguir las pantallas que van a tener interfaz dinámica de las decorativas; no trasladar sin revisión gráficos pequeños a monitores cercanos a la cámara.
- Evaluar colisiones, mallas separables y coste de geometría/materiales tras importar a UE5. Los 2,1 M triángulos no determinan por sí solos el rendimiento.
- **Los megabytes del archivo y los recuentos de vértices no aportan medidas físicas**. La escala sigue pendiente de calibración con persona de referencia y UE5, según el Anexo A.
- Conservar atribución del autor y revisar la licencia antes de publicar derivados.

