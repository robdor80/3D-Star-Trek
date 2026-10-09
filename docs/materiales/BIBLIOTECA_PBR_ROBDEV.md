# RobDev Material Library — Biblioteca PBR para Star Trek (propuesta v0.1)

**Fecha:** 2026-10-09  
**Ámbito:** USS Theurgy (puente, Mission Ops, pasillos y futuras estancias), con reutilización posterior en otras naves e instalaciones del videojuego Star Trek.  
**Motor final:** Unreal Engine 5. **Herramienta geométrica:** Blender, con automatización mediante Codex/`bpy`.  
**Estado:** **diseño de biblioteca**, no texturas descargadas, no materiales UE5 creados, no pruebas de rendimiento realizadas.

## 1. Principio

Crear una **biblioteca PBR propia y reutilizable**, independiente de cada estancia. No limitarla a un único puente ni comprar obligatoriamente un paquete etiquetado «Star Trek». Las superficies físicas (cuero, aluminio, polímero, pintura, cristal, telas, metal, pavimento) se modelan con materiales generales de calidad; la identidad visual Trek (LCARS, insignias, indicadores, hologramas, alarmas) se añade como otra capa, con gráficos propios o con recursos para los que tengamos derechos.

**Separar:** recursos originales/licencias → texturas normalizadas → materiales maestros UE5 → instancias por nave/estancia → actores interactivos UE5.

## 2. Biblioteca propuesta, por familias

| Familia | ID base propuesto | Aplicación futura |
| --- | --- | --- |
| Cuero y tapicería | `Leather_Black_Fine`, `Fabric_Dark` | Sillón capitán, asientos de estaciones, camarotes |
| Metales | `Metal_Graphite`, `Metal_Brushed_Aluminum`, `Metal_Dark_Titanium` | Estructuras, consolas, barandillas, puertas |
| Polímeros y paneles | `Polymer_Matte_Charcoal`, `Panel_Satin_Gray` | Consolas, revestimientos, muebles, pasillos |
| Suelos | `Floor_Composite_Dark`, `Floor_Grip_Matte` | Puente, Mission Ops, corredores |
| Vidrios | `Glass_Smoked`, `Glass_Display` | Mamparas, displays y superficies de mesa |
| Elementos luminosos | `Light_Strip_White`, `Light_Strip_Cyan` | Arquitectura e indicadores |
| Interfaces funcionales | `Display_LCARS`, `Display_Sensor` | Consolas que mostrarán UI dinámica en UE5 |
| Hologramas | `Holo_Cyan` | Mesa de Mission Ops y proyecciones |
| Señalética y decals | `Decal_Door_ID`, `Decal_Fleet_Sign` | Numeración de accesos, señalización e iconos |

Los IDs son **propuestas iniciales**, no nombres de objetos de la malla importada ni assets UE5 existentes.

## 3. Estrategia de materiales UE5

Se diseñarán unos pocos **materiales maestros** parametrizados y numerosas **instancias**, evitando duplicar shaders complejos:

- `M_RD_Surface`: superficies opacas (base color, roughness, metallic, normal, tintes y escala UV cuando convenga).
- `M_RD_Emissive`: superficies emisivas y bandas de iluminación; intensidad/color parametrizables.
- `M_RD_Display`: pantallas; textura/render target/UI dinámica según sistema funcional.
- `M_RD_Glass`: cristal; definir modo de representación adecuado al coste y efecto buscados en UE5.
- `M_RD_Hologram`: hologramas con transparencia/animación cuando se valide el coste en el motor.
- `M_RD_Decal`: marcas y señalética, con formato apropiado al pipeline UE5.

Ejemplos de **instancias**: `MI_Theurgy_Leather_Captain`, `MI_Theurgy_Metal_Console`, `MI_Theurgy_Floor_Main`, `MI_Theurgy_Light_Cyan`. Otras naves podrán reutilizar `M_RD_*` con instancias nuevas. Los maestros se ajustarán según la versión concreta de UE5 y la plataforma objetivo.

**Nota:** los nodos procedurales de Blender no se transfieren de forma equivalente de forma automática a UE5. Se exportarán mapas cuando proceda y se crearán los materiales del juego en UE5.

## 4. Normalización PBR y texturas

- Canal base: **Base Color (sRGB)**. Roughness, Metallic, AO, Height y mapas de datos: importar **sin sRGB** cuando proceda; mapas normales con configuración específica de normales de UE5.
- Aprovechar texturas Color, Roughness, Normal, Metallic, AO y Emissive según las necesite cada material; **no todos necesitan todos los mapas**.
- Considerar **empaquetado de canales ORM** (AO / Roughness / Metallic) cuando sea apropiado; conservar manifiesto que especifique en qué canal está cada dato.
- Documentar **unidad de escala del patrón** (anchura física del material si se conoce) y coherencia de densidad de texel entre piezas y estancias; evitar que la veta del cuero o del metal cambie de tamaño de una habitación a otra.
- Comenzar con resoluciones **1K o 2K según tamaño aparente y distancia a cámara**, dejando 4K para casos concretos que demuestren beneficiarse de ello. Texturas pequeñas para detalles modestos; **no imponer 2K a todo**.
- Controlar tiling, costuras visibles, colorimetría, UV, normales y material slots antes de dar un asset por acabado.
- Usar compresión, mipmaps y streaming adecuados en UE5 y comprobar consumo real de memoria/VRAM.

## 5. Estancias futuras: regla de modularidad

Después del puente Theurgy podrán añadirse pasillos, turboascensores, salas de reuniones, oficinas, camarotes y demás espacios **a través de puertas funcionales del escenario**, sin reconstruir de nuevo su identidad visual.

Para ello:

1. Definir **escala física común** del proyecto, pivotes, orientación y convenciones de puertas/marcos (en UE5 medir con personaje real). No fijar dimensiones arbitrarias por intuición.
2. Mantener **kits geométricos independientes** de los kits de materiales: módulo de pared, suelo, techo, puerta, panel, luz y señal.
3. Hacer que los materiales se puedan compartir entre zonas mediante instancias y parámetros. Diferenciar colores/iluminación por departamento o tipo de estancia sin duplicar todas las texturas.
4. Preparar conexiones transitables reales y continuas: colisiones, NavMesh, animación de puertas y uso por NPC.
5. Mantener materiales de interfaz funcional separados de superficies decorativas para que la lógica de juego pueda actualizar pantallas sin rehacer sus mallas.
6. Cada sala nueva pasará pruebas de iluminación y materiales **dentro de UE5** antes de considerarse final.

## 6. Procedencia, licencias y almacenamiento

**Bibliotecas de partida a evaluar:**

- Poly Haven: https://polyhaven.com/textures — biblioteca CC0 según condiciones de cada recurso; ejemplo visto: Leather Red 02 (se puede tintar hacia cuero negro).
- ambientCG: https://ambientcg.com — biblioteca CC0; distinguir descargas de mapas PBR de archivos `.sbsar` que requieren herramientas compatibles.
- TextureCan: https://www.texturecan.com — comprobar licencia concreta de cada recurso antes de incorporarlo.

Crear una ficha de procedencia por recurso, con campos:

`asset_id` · `nombre` · `url_fuente` · `autor` · `licencia` · `fecha_obtencion` · `version_origen` · `transformaciones` · `canales` · `resolucion` · `dimensiones_patron` · `usos` · `ubicacion_maestro` · `ubicacion_producto`.

- La licencia de una textura externa **no se deduce** del formato ni de su disponibilidad de descarga.
- Evitar usar materiales/texturas extraídos de modelos de terceros con derechos restringidos.
- Conservar fuentes originales (maestros) separadas de versiones optimizadas/derivadas para el juego.
- Git ordinario (`3D-Models`) almacenará inventarios, especificaciones, scripts, manifiestos y referencias. Los binarios de gran tamaño se almacenarán en un sistema definido explícitamente (p. ej. repositorio separado con Git LFS, archivo externo o gestión de Unreal), sin incorporarlos por defecto.
- Para recursos CC0, mantener registro de fuente y autor aunque no sea obligatoria la atribución; facilita trazabilidad y mantenimiento.
- La iconografía e interfaces de **Star Trek** pueden tener derechos de terceros aun si los materiales físicos utilizados son CC0; mantener separadas sus licencias y no asumir libertad de distribución comercial.

## 7. Pipeline con Blender + Codex + UE5

1. **Identificación** del objeto en Blender, de la zona UV y de los materiales heredados del Enterprise; comprobar si un material está compartido.
2. **Selección/prototipo** del material físico base, aplicando una instancia o versión de prueba; conservar la geometría intacta y guardar antes/después.
3. **Texturizado/horneado** si corresponde, con mapas compatibles y escalas correctas; Codex puede automatizar `bpy`, convertir imágenes y generar manifiestos.
4. **Creación de maestro/instancia en UE5**, enlazando mapas y parámetros con el comportamiento buscado.
5. **Validación visual y técnica en UE5** con personaje y luces reales del escenario; revisar costuras, tono, rendimiento, transparencia y emissive.
6. **Publicación del recurso aprobado** en la biblioteca, con versión, procedencia, ajustes y usos. Una variante nueva no reemplaza silenciosamente un material en uso.

## 8. Prueba piloto propuesta

**Piloto:** cuero negro del respaldo del sillón del capitán (primera pieza de prueba). Seleccionar textura CC0 de cuero, estudiar UV y separación del respaldo, crear material de prueba, aplicarlo en copia y evaluarlo en UE5 con iluminación del puente. **No es necesario descargar ahora 77 MB de textura 4K ni escoger proveedor definitivo.**

**Segundo piloto:** metal grafito de una consola, con variante para iluminación blanca/azul.

**Tercer piloto:** suelo del puente, que debe funcionar bien en visión cercana y lejana y mantener una densidad de detalle coherente con la ampliación Mission Ops.

## 9. Estado y dependencia con otros documentos

- Geometría/referencias: [Diseño maestro Theurgy](../uss-theurgy/DISENO_MAESTRO.md).
- Reglas de exportación/jugabilidad: [Contrato UE5](../uss-theurgy/UE5_ESCENARIO_JUGABLE.md).
- **Fase actual:** arquitectura y criterios. Aún no hay biblioteca PBR de producción, instancias en UE5 ni resultados validados.
- **Prioridad inmediata:** identificar geometría del modelo y calibrar escala. Preparar UV/material slots desde el inicio. La fase intensiva de materiales vendrá una vez conseguida una versión recorrible en UE5.
