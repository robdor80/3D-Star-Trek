# Auditoría inicial del inventario local — 3D Star Trek

Fecha: **9 de octubre de 2026**, Europe/Madrid. Entorno: MSI Windows. Repositorio: `C:/Users/andro/Documents/GitHub/3D Star Trek`.

## 1. Resumen ejecutivo

El canon vigente es un **puente USS Theurgy jugable en UE5**, utilizando **U.S.S. Enterprise A New Bridge** como base geométrica y creando posteriormente Mission Ops. El nombre heredado `enterprise_kelvin` no acredita origen Kelvin. `assets/otros/` constituye una biblioteca auxiliar independiente.

La base principal disponible es **Collada 1.4.1**, no glTF. El DAE coincide por SHA-256 con el original empaquetado; sus **20 referencias de textura** están disponibles. Declara **pulgadas, 0,0254 metros por unidad**, y **Z_UP**. La caja matemática global con instancias mide **21,353696 × 16,300531 × 4,560299 m**, según esa declaración. Falta validar escala funcional y circulación con personaje UE5.

Blender instalado: **5.2.2 LTS**, Windows, compilado el 2026-09-15, hash `d13f752e3b9c`. **No tiene registrado el importador Collada**; sí dispone de glTF, USD y FBX. El ZIP glTF del puente descrito en los documentos no está en el repositorio. El USDZ local es candidato por sus nombres de textura, pero su identidad y estructura interna todavía no están confirmadas.

No hay escena maestra `.blend`, scripts de modelado ni proyecto UE5 implementado aquí. No se modificó geometría ni se importaron modelos, instalaron herramientas o extrajeron archivos a disco. Las referencias Theurgy se trataron exclusivamente por metadatos, sin mostrarlas ni analizarlas visualmente mediante IA.

Los recuentos completos, que incluyen incorporaciones concurrentes durante la auditoría, figuran en el apartado 12. No confundir archivos/variantes con modelos distintos.

## 2. Método y límites de evidencia

- Lectura completa de `AGENTS.md`, `README.md`, `.gitignore`, `.gitattributes`, `docs/puente-kelvin/PLAN.md`, `docs/uss-theurgy/DISENO_MAESTRO.md`, `docs/uss-theurgy/UE5_ESCENARIO_JUGABLE.md`, `docs/materiales/BIBLIOTECA_PBR_ROBDEV.md` y `tools/inventario_gltf.py`.
- Recorrido local con `rg --files --hidden --no-ignore` y Python `os.walk`, sin limitarse a archivos versionados. Comprobación posterior de nuevas incorporaciones.
- Python 3.10 instalado, biblioteca estándar: XML, JSON GLB, directorios ZIP/USDZ, cabeceras PNG/JPEG y SHA-256. No se ejecutó código de los activos.
- ZIP leídos por streaming; ZIP anidados leídos en memoria, sin extracción a disco. Lecturas completas de miembros ZIP comprueban CRC mediante `zipfile`. USDZ: solo directorio y cabecera USDC, sin validar íntegramente escena ni texturas.
- DAE: lectura de POSITION enlazados desde vertices, matrices por filas y vectores columna, expansión recursiva de `instance_node/library_nodes`. Caja global sobre posiciones transformadas. No se validaron superficies transitables, costuras UV, normales, topología manifold ni clasificación funcional.
- GLB: cabecera y JSON, longitud declarada frente a tamaño físico. No se validaron todos los accesores/rangos BIN ni se renderizó. Los triángulos GLB suman primitivas TRIANGLES por definición de malla, sin multiplicar instancias de nodo.
- `.git/` se contabilizó de forma agregada: 61 archivos y 60.499 bytes después de crear la rama. No se publican configuración privada, hooks ni contenidos internos. No se consultó GitHub ni el remoto.
- Fuera del repositorio solo se examinó la instalación local de Blender. No se auditó una instalación UE5 externa.
- Imágenes Theurgy: nombres, bytes, cabeceras PNG y hashes; sin visionado, OCR, carga visual a IA ni consultas a sus páginas originales.
- Durante el recorrido aparecieron el corredor modular, Danube y NPC. Se incorporaron a las tablas. Es una instantánea de disco, no un bloqueo de futuras aportaciones.

El anexo `INVENTARIO_LOCAL_DATOS.json` contiene evidencia textual de rutas, tamaños, hashes, estructuras y miembros ZIP. No contiene imágenes ni binarios.

## 3. Git y conservación

Estado inicial: `main...origin/main`, sin cambios mostrados por `git status --short --branch`; solo existía la rama local `main`. Se creó y activó **`audit/inventario-inicial-3d`**. No se descartó ni sobrescribió trabajo anterior. No se ejecutaron add, commit, push, reset, clean ni operaciones remotas.

Los binarios locales están ignorados por `.gitignore`, incluidos todos los recursos de `assets/otros/`. Los `.gitkeep` previstos están versionados. `.gitattributes` solo configura normalización de texto, no LFS. Los futuros `.blend`, FBX, GLB o recursos UE5 fuera de rutas ignoradas no quedan excluidos por una regla general: definir almacenamiento y comprobar licencias antes de futuras incorporaciones. No se modificó `.gitignore`.

Las únicas escrituras de contenido son los dos informes de auditoría. La creación de rama modifica metadatos Git. Se conservaron originales y documentos previos; ver comprobación SHA-256 de cierre en apartado 12.

## 4. Canon y diferencias entre documentos y disco

| Asunto | Documentación | Hecho local / criterio vigente |
| --- | --- | --- |
| Objetivo | AGENTS menciona Enterprise Kelvin | Prima la instrucción actual y diseño maestro: Theurgy; base Enterprise A New Bridge, sin procedencia Kelvin acreditada |
| Entrada principal | PLAN describe `u.s.s._enterprise_a_new_bridge.zip` glTF/BIN | No existe aquí; sí `ENT-A1_dae.zip` y DAE extraído |
| Recuentos antiguos | 104 nodos, 99 mallas, 55 materiales, 21 imágenes, 2.138.083 triángulos | Históricos del glTF ausente; no aplicarlos al DAE actual ni a GLB de otras naves |
| Escala | Anexo A propone pulgadas como hipótesis | DAE declara pulgadas explícitamente; falta comprobar escala útil e importación |
| Capturas | Diseño maestro indica capturas anteriores fuera del repositorio | Diez PNG locales presentes; no se demuestra identidad con capturas históricas solo por nombre |
| Mission Ops | Zona 008 preliminar y ampliación 020 detallada | Nueva extensión posterior integrada; mesa holográfica y puestos; no plataforma ya existente |
| Pruebas anteriores | PLAN comunica pruebas de sillón/suelo | No hay escenas/scripts aquí para reproducirlas |
| PBR | Biblioteca expresamente propuesta | No existen materiales maestros/instancias UE5 ni biblioteca PBR de producción |
| Entorno | Referencias a `3D-Models`, Realme y sincronización futura | Tarea actual solo MSI, repositorio `3D Star Trek` |
| Formato Markdown | DISENO_MAESTRO contiene `\n\n` literal antes del apartado 1 | Defecto observado, no reparado para limitar escrituras a auditoría |

## 5. Base Enterprise A New Bridge

Ruta DAE: `assets/enterprise_kelvin/modelo_original/uss-enterprise-a-new-bridge/source/ENT-A1_dae/model.dae`.

Tamaño: **84.248.309 bytes**. SHA-256: `447d9cfd90e326875b28ed5345f59d8e8633b712618319c5ec0806c001c5453e`. Exportador: **SketchUp 23.1.340**; fechas internas creado/modificado: **2024-03-29T14:03:21Z**. No hay autor ni licencia explícitos en el asset XML.

Collada contiene **2.526 definiciones de geometría**, **18 nodos en visual_scene**, **399 nodos en library_nodes**, **265 elementos instance_node**, **55 materiales**, **55 efectos**, **20 imágenes**. Las definiciones suman **713.534 triángulos y 381.894 líneas**. Al expandir instancias de escena: **10.721 instancias de geometría**, **2.138.314 triángulos**, **3.122.804 entradas POSITION transformadas**; las definiciones contienen **1.014.603 entradas POSITION**. No son vértices únicos soldados. Nodos, instancias, geometrías y objetos jugables son conceptos distintos.

Efectos heredados `profile_COMMON`: **39 lambert y 16 constant**, sin equivalencia automática a PBR Unreal. Existe el material `GLASS_FLOOR`, sin asociación visual validada. Nombres genéricos de grupos/instancias; falta mapa semántico de sillas, consolas y arquitectura. Algunas matrices contienen reflexión y escala no uniforme; habrá que comprobar normales y transformaciones durante la futura importación.

| Caja global | Pulgadas fuente | Metros según DAE |
| --- | ---: | ---: |
| X horizontal | 840,696700 | 21,353696 |
| Y horizontal | 641,753200 | 16,300531 |
| Z vertical | 179,539316 | 4,560299 |

Mínimo fuente aproximado: (-420,3483; -320,8766; -26,77165); máximo: (420,3484; 320,8766; 152,767666). Incluye toda la geometría instanciada, no solo espacio transitable. Coincide numéricamente con dimensiones históricas glTF tras intercambiar ejes vertical/profundidad, pero difieren los recuentos: no acredita igualdad completa de exportaciones. No aplicar nuevamente 0,0254 si el importador ya convierte unidades.

**ZIP fuente:** `ENT-A1_dae.zip`, 20.411.908 bytes; 21 miembros, `model.dae` y 20 texturas (19 JPG + 1 PNG), 90.581.423 bytes descomprimidos. Todos coinciden por SHA-256 con archivos locales existentes. No se extrajo ni reemplazó nada.

**Texturas:** las 20 URI del DAE resuelven en `source/ENT-A1_dae/model/`. Carpeta hermana `textures/`: 22 archivos (20 JPEG + 2 PNG), incluidos `internal_ground_ao_texture.jpeg` y `material_28.inline_conv_generated.png`, adicionales respecto a las 20 referencias DAE. `texturas_originales/` solo tiene `.gitkeep`.

Seis parejas idénticas por SHA-256 entre JPG fuente y JPEG: `iso_web_yellow2`, `material_3`, `material_43`, `material_48`, `material_54`, `material_7`. Otros nombres similares y resoluciones iguales difieren en bytes: no se afirma igualdad de píxeles ni se deduplica. Resoluciones entre 21×21 y 2349×2099; una textura pequeña no demuestra por sí sola un defecto. Las tablas completas incluyen resolución.

**Otros archivos en la ruta heredada:** los GLB se identifican por metadatos internos como Enterprise NCC 1701 D y Star Trek TNG Galaxy Class Model. Son otros recursos, no Enterprise A New Bridge; ver autores/licencias en el inventario GLB.

**USDZ:** `U.S.S.usdz`, 76.463.978 bytes; contiene `scene.usdc` de 72.140.817 bytes, cabecera `PXR-USDC`, y 20 imágenes de base color. Nombres HONEYCOMB_GLOW_2, VIEWSCREEN_GLOW y NewTrekLCARS concuerdan con el puente: asociación probable, **identidad no confirmada**. No se leyó jerarquía USD, escala ni autoría. No afirmar que representa otra nave o que es exactamente el DAE.

**Procedencia/licencia:** PLAN atribuye Enterprise a Cpt.Kirk y CC BY 4.0 a partir del glTF/capturas históricos. Los archivos locales DAE/ZIP no incluyen ficha explícita de licencia. Recuperar evidencia vinculada al archivo antes de distribuir derivados; conservar atribución. La licencia declarada no acredita automáticamente derechos sobre Star Trek o gráficos ajenos.

## 6. USS Theurgy: metadatos y diseño previsto

Hay diez PNG en `imagenes_puente/`; nombres, bytes y resolución están en el apartado 12. `planos/` solo tiene `.gitkeep`. Ninguna imagen se examinó visualmente en esta sesión; las funciones descritas a continuación proceden de los documentos, no de reconocimiento del contenido de las PNG.

Las **20 zonas funcionales previstas** son: pantalla principal; área holográfica frontal; CONN; OPS; silla del capitán; Táctica; Ingeniería; Mission Ops; Ciencia; Inteligencia/Comunicaciones; Support Staff; puestos de seguridad; turboascensores; acceso a Captain's Ready Room; checkpoint/control de acceso; soportes inclinados; techo anular; bandas luminosas; consolas/pantallas posteriores; ampliación rectangular. Son zonas de diseño, no veinte objetos existentes verificados.

Mission Ops es una prolongación posterior integrada detrás del capitán, de nueva construcción: múltiples estaciones, mesa holográfica horizontal, bancada de monitores y arquitectura modular. Conservar silla del capitán; estudiar separación del cerramiento posterior Enterprise antes de sustituirlo. La mesa posterior y el área holográfica frontal son distintas. Cantidad de puestos, cotas, dimensiones, huella y conexión siguen pendientes. La ausencia de esa ampliación en Enterprise es una decisión/evidencia histórica registrada, no una comprobación visual nueva de esta auditoría.

**Restricciones documentadas:** DISENO_MAESTRO atribuye a Auctor Lucan condiciones NoAI, uso no comercial y atribución; prohíbe incorporar modelo/texturas a Codex o distribuirlos sin permiso explícito. Aquí no consta autorización para análisis visual por IA, reproducción/adaptación, comercialización o publicación de derivados. La posesión de capturas no prueba permiso. Resolver alcance con el titular y guardar autorización/atribución. No se consultaron páginas Theurgy ni se remitieron imágenes a servicios externos. Se registran condiciones de los documentos, no verificación web actual ni dictamen jurídico.

## 7. Biblioteca auxiliar: assets/otros

- **Low Poly Corridor - [Star Trek]:** dos GLB del mismo título/fuente, Robin Butler, CC-BY-NC-4.0 declarada. Original: specularGlossiness; variante PBR_Compat: IOR/specular. Ambos 21 nodos, 10 mallas, 9 materiales, 19.886 triángulos por definiciones, cero imágenes. No son duplicados binarios. ZIP con `source/Cooridoor test.blend`, 1.335.372 bytes, cabecera `BLENDER-v279` (2.79); no abierto.
- **hangar:** GLB Star Trek Hangar, Cpt.Kirk, CC-BY-4.0 declarada. También ZIP del corredor modular: contiene `source/Star Trek Corridor.blend`, 3.371.956 bytes, cabecera Blender 2.79. Es otro corredor, no el hangar. Autor/licencia/escala del ZIP no acreditados por directorio, sin licencia interna listada.
- **replicator:** Henry Star Trek TNG Replicator, MML0385, CC-BY-4.0 declarada. Sus 202 definiciones de malla no equivalen a componentes interactivos.
- **Danube simulador:** GLB y ZIP convertido glTF/BIN/cinco PNG/licencia, Crusty Bread, CC-BY-4.0 declarada. ZIP original: cuatro PNG y ZIP anidado con `runabout cockpit 6.obj`, 4.343.027 bytes; sin MTL listado. Licencia interna del convertido coincide con GLB. Son variantes de la misma familia auxiliar.
- **NPC/7 de 9:** Seven of Nine, Stan, CC-BY-NC-4.0 declarada; GLB con **una skin y una animación**. ZIP fuente contiene FBX y texturas; ZIP convertido glTF/BIN/texturas/licencia. No se comprobaron rig, pesos, animación ni compatibilidad del esqueleto con UE5.
- **NPC/Piccard:** Patrick Stewart (Star Trek), David Wigforss, CC-BY-4.0 declarada; GLB sin skins/animaciones. ZIP original incluye dos niveles ZIP adicionales; en el nivel interior hay `mesh.fbx`, 4.328.024 bytes, y dos JPG. No se infiere comportamiento NPC ni rig por el nombre de carpeta.

No se mezclaron estos recursos con el puente. Las licencias son declaraciones locales, no verificación de facultades del publicador. Corredor y Seven of Nine tienen restricción NC; aclarar permisos para uso comercial. No convertir recursos de terceros en biblioteca PBR propia sin procedencia y permisos.

## 8. Blender, formatos y herramienta de inventario

Prueba ligera: `blender.exe --version` y arranques `--background --factory-startup --python-expr`, sin activos, render o guardado de preferencias. Verificación mediante `get_rna_type()`: `WM_OT_collada_import` no existe; `IMPORT_SCENE_OT_gltf`, `WM_OT_usd_import` y `IMPORT_SCENE_OT_fbx` están registrados. Se descartó una comprobación preliminar con `hasattr(bpy.ops, ...)`, que no demuestra registro de operadores.

| Formato local | Adecuación Blender / límite |
| --- | --- |
| DAE | Fuente original con unidades; no importador integrado en 5.2.2 |
| GLB/glTF | Importador registrado; GLB del puente exacto ausente, variantes auxiliares disponibles |
| USDZ/USDC | Importador registrado; candidato local de puente con identidad/escala/estructura pendientes |
| BLEND 2.79 empaquetado | Posible apertura de copia posterior; compatibilidad de escena/shaders no ensayada |
| OBJ empaquetado | Alternativa Danube; vinculación de materiales pendiente, sin MTL listado |
| FBX empaquetado | Fuentes NPC; importador registrado, rig/materiales no ensayados |

Collada integrado fue retirado desde Blender 5.0 según [notas oficiales Pipeline & I/O](https://developer.blender.org/docs/release_notes/5.0/pipeline_io/). Puede evaluarse Blender 4.5 LTS, última serie con Collada integrado según [anuncio oficial de desarrollo](https://devtalk.blender.org/t/moving-collada-i-o-to-legacy-status/34621/79), o complemento/conversor local mantenido, previa autorización para instalar. No se ejecutó ninguna alternativa. Preferir comprobar USDZ o recuperar GLB/glTF exacto con procedencia documentada; no sustituirlo por Enterprise D/Galaxy.

El [manual USD](https://docs.blender.org/manual/en/4.4/files/import_export/usd.html) documenta opciones de copia/empaquetado de texturas USDZ; cualquier prueba futura debe dirigir derivados fuera de assets. El [manual glTF](https://docs.blender.org/manual/en/5.1/addons/import_export/scene_gltf2.html) documenta GLB/glTF. El código glTF instalado incluye tratamiento de specularGlossiness, IOR y specular: `PBR_Compat` no demuestra que el corredor original sea imposible de importar. Falta ensayo de equivalencia.

**`tools/inventario_gltf.py`:** solo `.gltf` JSON o ZIP con exactamente un `.gltf`. No admite DAE, GLB, USDZ, BLEND ni ZIP anidados. ENT-A1_dae.zip tiene cero glTF y fallaría. Puede utilizarse para ZIP convertidos auxiliares; los IDs KELVIN heredados no acreditan identidad. Solo lee JSON; no posiciones BIN, transformaciones globales ni escala. Su salida sobrescribe archivos existentes. No se ejecutó ni modificó; requiere lector Collada o adaptación a GLB cuando se disponga del puente correcto.

## 9. Preparación comprobada para UE5

| Área | Requisito documental | Implementación local comprobada |
| --- | --- | --- |
| Escala | Métrico, cm UE5 y Character de prueba | Pulgadas declaradas y caja calculada; sin ensayo Blender/UE5 |
| Ejes/origen/pivotes | Orientación y pivotes funcionales | Z_UP y matrices; sin pivotes funcionales identificados |
| Jerarquía | Arquitectura, consolas, sillas, puertas, luces separados | Instancias genéricas; sin colecciones Blender/mapa semántico |
| UV/normales | Costuras, normales y lightmaps según iluminación | No validados visualmente ni en motor |
| Texturas/PBR | Maestros/instancias, pantalla dinámica, emisivos | Texturas accesibles, shaders DAE heredados; PBR propia solo propuesta |
| Colisiones/circulación | Suelo estable, pasos, cápsula y NavMesh | Sin colisiones UE5 ni prueba de navegación |
| Interactividad | Puerta, asiento, consola, mesa; lógica Blueprint/C++ | Sin implementación de juego ni anclajes funcionales del puente |
| Mission Ops | Nueva arquitectura y unión continua | Diseño documental, ninguna nueva geometría |
| Rendimiento | Perfilado y decisiones LOD/Nanite/luces | Recuentos fuente, sin FPS/VRAM/perfilado |
| Proyecto UE5 | Mapa de ensayo y Character | Ningún .uproject, .uasset o .umap en repositorio |
| Reproducibilidad | Scripts bpy y versiones de escena | scripts/blender_python solo .gitkeep; herramienta glTF y documentos |

La biblioteca física propuesta (cuero/tela, metales, polímeros, suelo, vidrio, luces, interfaces, hologramas, decals), maestros `M_RD_*` y pilotos de sillón/consola/suelo no están implementados reproduciblemente aquí. No hay evidencia para declarar el puente listo para UE5.

## 10. Incidencias y recomendaciones priorizadas

1. **P0 — Vía de importación:** DAE sin importador en Blender actual y glTF histórico ausente. Confirmar identidad del USDZ y ensayar copia; si no sirve, recuperar GLB/glTF exacto o autorizar una vía DAE compatible.
2. **P0 — Procedencia/permisos:** ficha Enterprise vinculada al binario; mantener NoAI Theurgy; resolver alcance de adaptación/distribución/comercialización, licencias NC y corredor modular. No publicar originales/derivados por defecto.
3. **P1 — Escala:** documentar pulgadas→metros→cm sin doble conversión; validar con silla/puertas/personaje. La caja global no fija anchos libres ni cápsula.
4. **P1 — Correspondencia:** zona funcional↔geometría/material↔pieza mecánica, preservando instancias. No reutilizar los IDs de 99 mallas del glTF ausente ni equiparar geometrías DAE a objetos jugables.
5. **P1 — Documentos:** actualizar entrada real, rutas MSI, texturas, PNG locales y unidad fuente en tarea posterior, conservando evidencias históricas claramente identificadas.
6. **P2 — Prototipo UE5:** versión/cápsula/hardware, suelo y colisiones, circulación y una pieza interactiva antes de Mission Ops. Definir unión y escala antes de crear extensión.
7. **P2 — Materiales:** revisión UV/material slots y PBR propia con manifiestos de procedencia. Biblioteca auxiliar separada. No deduplicar/reorganizar assets en esta tarea.
8. **P2 — Almacenamiento:** política de escenas/copias/exportaciones/binarios; comprobar exclusiones antes de futuros commits. No LFS configurado aquí.

## 11. Próximo trabajo técnico concreto

**Confirmar la identidad y estructura del `U.S.S.usdz` con un lector USD local disponible y preparar una prueba aislada de importación en Blender 5.2.2**, conservando originales y guardando derivados en `blender/`, pruebas en `output/`. Comparar unidades, caja, materiales e instancias con el DAE auditado; registrar parámetros y correspondencias. Si no se confirma la misma base, recuperar la exportación GLB/glTF exacta de Enterprise A New Bridge con licencia, o solicitar autorización para una vía DAE local compatible.

No empezar Mission Ops ni editar mallas antes de resolver importación, escala y mapa de piezas. Este siguiente trabajo no se ejecuta en la auditoría.

## 12. Inventario, árbol y evidencia de cierre

Cierre de inventario: `2026-10-09T23:15:58.976153+02:00`. **99 archivos previos a los dos informes**, **81 en assets**, de ellos 5 marcadores .gitkeep y **76 recursos**, **677,054,742 bytes**. **13 archivos de modelo sueltos**: 11 GLB, un DAE y un USDZ. **11 ZIP externos**. **52 imágenes sueltas**, 42 texturas Enterprise y diez referencias Theurgy. Modelos dentro de paquetes (incluidos anidados): `{'.usdc': 1, '.dae': 1, '.blend': 3, '.obj': 2, '.gltf': 3, '.fbx': 2}`; USDC es la escena interna del USDZ ya contado, DAE empaquetado es duplicado comprobado. Estas representaciones no equivalen a diseños distintos. Imágenes dentro de archivos: **418 apariciones**, incluidos duplicados; imágenes embebidas GLB: **227 entradas**, sin afirmar unicidad.

### Verificación de integridad y cambios concurrentes
Se releyeron **81 archivos de assets**. Resultado: contenido cambiado `[]`, rutas nuevas pendientes `[]`, ausencias desde inventario final `[]`.
Durante la auditoría las tres rutas del corredor Low Poly dejaron de existir en su ubicación inicial y aparecieron bajo hangar. Los hashes coinciden; se registran como reubicaciones externas observadas. Codex no ejecutó operaciones de movimiento, borrado o modificación en assets. Las tablas siguientes muestran las rutas actuales.
- `assets/otros/Low Poly Corridor - [Star Trek]/low-poly-corridor-star-trek.zip` → `assets/otros/hangar/Low Poly Corridor - [Star Trek]/low-poly-corridor-star-trek.zip`; mismo SHA-256.
- `assets/otros/Low Poly Corridor - [Star Trek]/low_poly_corridor_-_star_trek.glb` → `assets/otros/hangar/Low Poly Corridor - [Star Trek]/low_poly_corridor_-_star_trek.glb`; mismo SHA-256.
- `assets/otros/Low Poly Corridor - [Star Trek]/low_poly_corridor_-_star_trek_PBR_Compat_6997a32b7a8d44a8a250f9332cb2f180.glb` → `assets/otros/hangar/Low Poly Corridor - [Star Trek]/low_poly_corridor_-_star_trek_PBR_Compat_6997a32b7a8d44a8a250f9332cb2f180.glb`; mismo SHA-256.

### Incorporaciones finales a la biblioteca auxiliar

- **Enterprise Corridor**, `assets/otros/hangar/`: GLB de Massimiliano Castiglione, CC-BY-4.0 declarada. ZIP con BLEND y una textura AO. La cabecera del BLEND empaquetado no empieza por BLENDER; archivo comprimido, versión no identificada en esta auditoría. No se presume Blender 2.79 ni se abre.
- **Argo II Type Rover [Star Trek] ZEO**, `assets/otros/vehicles/rover/`: GLB y ZIP convertido glTF/BIN/texturas; ZIP original incluye OBJ/MTL y numerosas texturas en ZIP anidado. Autor ZEO CMF; licencia interna **CC-BY-NC-ND-4.0**. Registrar restricción de derivados además de uso no comercial; no asumir permiso para adaptar al juego. Recurso independiente del puente.

### Referencias Theurgy (solo metadatos)

| Archivo | Bytes | Resolución ancho×alto |
| --- | ---: | --- |
| 45 grados.png | 345,715 | 996×676 |
| Anexo 2.png | 2,036,967 | 2256×1074 |
| Anexo.png | 1,773,938 | 2248×1078 |
| Back view.png | 1,035,652 | 2089×1015 |
| Consola CONN y vuelo.png | 1,257,285 | 1903×807 |
| Consola lateral 2.png | 2,289,563 | 2238×1083 |
| Consola lateral.png | 997,912 | 2223×1084 |
| Silla capitan.png | 1,449,180 | 2266×1081 |
| frontal.png | 406,971 | 835×666 |
| zenital.png | 483,104 | 937×952 |

### Modelos GLB: datos internos

Triángulos por definiciones de malla; no por escena expandida. Autores/licencias son declaraciones locales.

| Ruta | Título / autor / licencia declarada | Nodos | Mallas | Materiales | Imágenes | Triángulos | Skins / animaciones |
| --- | --- | ---: | ---: | ---: | ---: | ---: | --- |
| `assets/enterprise_kelvin/modelo_original/enterprise_ncc_1701_d.glb` | Enterprise NCC 1701 D / morenostefanuto (https://sketchfab.com/morenostefanuto) / SKETCHFAB Standard (https://sketchfab.com/licenses) | 120 | 118 | 44 | 39 | 603,324 | 0 / 0 |
| `assets/enterprise_kelvin/modelo_original/star_trek_tng_galaxy_class_model.glb` | Star Trek TNG Galaxy Class Model / Crusty Bread (https://sketchfab.com/CrustyBread) / CC-BY-4.0 (http://creativecommons.org/licenses/by/4.0/) | 5 | 3 | 1 | 3 | 48,341 | 0 / 0 |
| `assets/otros/hangar/star_trek_hangar.glb` | Star Trek Hangar / Cpt.Kirk (https://sketchfab.com/CommanderCodyfromCoruscant) / CC-BY-4.0 (http://creativecommons.org/licenses/by/4.0/) | 63 | 58 | 57 | 33 | 68,208 | 0 / 0 |
| `assets/otros/replicator/henry_star_trek_tng_replicator.glb` | Henry Star Trek TNG Replicator / MML0385 (https://sketchfab.com/MML0385) / CC-BY-4.0 (http://creativecommons.org/licenses/by/4.0/) | 215 | 202 | 13 | 2 | 10,214 | 0 / 0 |
| `assets/otros/Danube simulador/star_trek_ds9_danube_runabout_rio_grande_cockpit.glb` | Star Trek DS9 Danube Runabout Rio Grande Cockpit / Crusty Bread (https://sketchfab.com/CrustyBread) / CC-BY-4.0 (http://creativecommons.org/licenses/by/4.0/) | 20 | 18 | 16 | 5 | 36,801 | 0 / 0 |
| `assets/otros/NPC/7 de 9/seven_of_nine.glb` | Seven of Nine / Stan (https://sketchfab.com/Stas_SayHallo) / CC-BY-NC-4.0 (http://creativecommons.org/licenses/by-nc/4.0/) | 119 | 6 | 6 | 13 | 27,134 | 1 / 1 |
| `assets/otros/NPC/Piccard/patrick_stewart_star_trek.glb` | Patrick Stewart (Star Trek) / David Wigforss (https://sketchfab.com/dwigfor) / CC-BY-4.0 (http://creativecommons.org/licenses/by/4.0/) | 5 | 1 | 1 | 2 | 15,087 | 0 / 0 |
| `assets/otros/hangar/enterprise_corridor.glb` | Enterprise Corridor / Massimiliano Castiglione (https://sketchfab.com/Maxider) / CC-BY-4.0 (http://creativecommons.org/licenses/by/4.0/) | 23 | 15 | 7 | 0 | 61,288 | 0 / 0 |
| `assets/otros/hangar/Low Poly Corridor - [Star Trek]/low_poly_corridor_-_star_trek.glb` | Low Poly Corridor - [Star Trek] / Robin Butler (https://sketchfab.com/StarTrekGuy) / CC-BY-NC-4.0 (http://creativecommons.org/licenses/by-nc/4.0/) | 21 | 10 | 9 | 0 | 19,886 | 0 / 0 |
| `assets/otros/hangar/Low Poly Corridor - [Star Trek]/low_poly_corridor_-_star_trek_PBR_Compat_6997a32b7a8d44a8a250f9332cb2f180.glb` | Low Poly Corridor - [Star Trek] / Robin Butler (https://sketchfab.com/StarTrekGuy) / CC-BY-NC-4.0 (http://creativecommons.org/licenses/by-nc/4.0/) | 21 | 10 | 9 | 0 | 19,886 | 0 / 0 |
| `assets/otros/vehicles/rover/argo_ii_type_rover_star_trek_zeo.glb` | Argo II Type Rover [Star Trek] ZEO / ZEO CMF (https://sketchfab.com/ZEOCMF) / CC-BY-NC-ND-4.0 (http://creativecommons.org/licenses/by-nc-nd/4.0/) | 91 | 89 | 80 | 130 | 1,144,701 | 0 / 0 |
Todos los GLB tienen firma glTF 2.0 y tamaño declarado igual al físico. No declaran imágenes externas. Animación/skin solo se observan en Seven of Nine; no se validó su comportamiento.

### Árbol de carpetas

Las carpetas blender/principal, componentes, backups, scripts/blender_python, output/*, temp, texturas_originales, imagenes_referencia y planos contienen solo marcadores, sin maestros ni pruebas. docs/auditorias contiene los entregables de esta tarea.

```text
.
  .git/ [metadatos privados; conteo agregado]
  assets/
    enterprise_kelvin/
      imagenes_referencia/
      modelo_original/
        uss-enterprise-a-new-bridge/
          source/
            ENT-A1_dae/
              model/
          textures/
      texturas_originales/
    otros/
      Danube simulador/
      NPC/
        7 de 9/
        Piccard/
      hangar/
        Low Poly Corridor - [Star Trek]/
      replicator/
      vehicles/
        rover/
    uss_theurgy/
      imagenes_puente/
      planos/
  blender/
    backups/
    componentes/
    principal/
  docs/
    auditorias/
    materiales/
    puente-kelvin/
    uss-theurgy/
  output/
    capturas_revision/
    exportaciones/
    renders/
  scripts/
    blender_python/
  temp/
  tools/
```

### Inventario físico completo

Rutas relativas al repositorio. Función probable basada en ruta/formato, no en inspección visual. Los informes creados se listan al final.

| Ruta | Formato | Bytes | Ignorado Git | Función probable / resolución |
| --- | --- | ---: | --- | --- |
| `.gitattributes` | (sin extension) | 66 | No | Configuración o documentación |
| `.gitignore` | (sin extension) | 968 | No | Configuración o documentación |
| `AGENTS.md` | .md | 1,815 | No | Configuración o documentación |
| `README.md` | .md | 16 | No | Configuración o documentación |
| `assets/enterprise_kelvin/imagenes_referencia/.gitkeep` | (sin extension) | 0 | No | Marcador de carpeta |
| `assets/enterprise_kelvin/modelo_original/.gitkeep` | (sin extension) | 0 | No | Marcador de carpeta |
| `assets/enterprise_kelvin/modelo_original/U.S.S.usdz` | .usdz | 76,463,978 | Sí | Candidato de base; identidad pendiente |
| `assets/enterprise_kelvin/modelo_original/enterprise_ncc_1701_d.glb` | .glb | 29,047,960 | Sí | Otra nave, identificada por metadatos |
| `assets/enterprise_kelvin/modelo_original/star_trek_tng_galaxy_class_model.glb` | .glb | 9,470,884 | Sí | Otra nave, identificada por metadatos |
| `assets/enterprise_kelvin/modelo_original/uss-enterprise-a-new-bridge/source/ENT-A1_dae.zip` | .zip | 20,411,908 | Sí | Fuente geométrica principal |
| `assets/enterprise_kelvin/modelo_original/uss-enterprise-a-new-bridge/source/ENT-A1_dae/model.dae` | .dae | 84,248,309 | Sí | Fuente geométrica principal |
| `assets/enterprise_kelvin/modelo_original/uss-enterprise-a-new-bridge/source/ENT-A1_dae/model/Aluminum.jpg` | .jpg | 12,471 | Sí | Textura Enterprise; 530×530 |
| `assets/enterprise_kelvin/modelo_original/uss-enterprise-a-new-bridge/source/ENT-A1_dae/model/Blinds_Roman_Hobbled_Blue.jpg` | .jpg | 4,097 | Sí | Textura Enterprise; 128×256 |
| `assets/enterprise_kelvin/modelo_original/uss-enterprise-a-new-bridge/source/ENT-A1_dae/model/GRATE_GLOW.jpg` | .jpg | 192,060 | Sí | Textura Enterprise; 1227×590 |
| `assets/enterprise_kelvin/modelo_original/uss-enterprise-a-new-bridge/source/ENT-A1_dae/model/HONEYCOMB_GLOW_2.jpg` | .jpg | 2,419,513 | Sí | Textura Enterprise; 1643×1459 |
| `assets/enterprise_kelvin/modelo_original/uss-enterprise-a-new-bridge/source/ENT-A1_dae/model/NewTrekLCARS.jpg` | .jpg | 2,726,355 | Sí | Textura Enterprise; 2349×2099 |
| `assets/enterprise_kelvin/modelo_original/uss-enterprise-a-new-bridge/source/ENT-A1_dae/model/VIEWSCREEN_GLOW.jpg` | .jpg | 99,265 | Sí | Textura Enterprise; 1073×208 |
| `assets/enterprise_kelvin/modelo_original/uss-enterprise-a-new-bridge/source/ENT-A1_dae/model/_58cd499217289.560ca8b44d983.jpg` | .jpg | 234,545 | Sí | Textura Enterprise; 1024×646 |
| `assets/enterprise_kelvin/modelo_original/uss-enterprise-a-new-bridge/source/ENT-A1_dae/model/__.jpg` | .jpg | 21,835 | Sí | Textura Enterprise; 600×600 |
| `assets/enterprise_kelvin/modelo_original/uss-enterprise-a-new-bridge/source/ENT-A1_dae/model/iso_web_yellow2.jpg` | .jpg | 34,913 | Sí | Textura Enterprise; 390×806 |
| `assets/enterprise_kelvin/modelo_original/uss-enterprise-a-new-bridge/source/ENT-A1_dae/model/material_28.png` | .png | 229,353 | Sí | Textura Enterprise; 568×995 |
| `assets/enterprise_kelvin/modelo_original/uss-enterprise-a-new-bridge/source/ENT-A1_dae/model/material_3.jpg` | .jpg | 16,783 | Sí | Textura Enterprise; 167×86 |
| `assets/enterprise_kelvin/modelo_original/uss-enterprise-a-new-bridge/source/ENT-A1_dae/model/material_3_0.jpg` | .jpg | 13,468 | Sí | Textura Enterprise; 167×86 |
| `assets/enterprise_kelvin/modelo_original/uss-enterprise-a-new-bridge/source/ENT-A1_dae/model/material_3_1.jpg` | .jpg | 13,434 | Sí | Textura Enterprise; 167×86 |
| `assets/enterprise_kelvin/modelo_original/uss-enterprise-a-new-bridge/source/ENT-A1_dae/model/material_4.jpg` | .jpg | 894 | Sí | Textura Enterprise; 21×21 |
| `assets/enterprise_kelvin/modelo_original/uss-enterprise-a-new-bridge/source/ENT-A1_dae/model/material_43.jpg` | .jpg | 115,341 | Sí | Textura Enterprise; 313×397 |
| `assets/enterprise_kelvin/modelo_original/uss-enterprise-a-new-bridge/source/ENT-A1_dae/model/material_44.jpg` | .jpg | 34,315 | Sí | Textura Enterprise; 167×197 |
| `assets/enterprise_kelvin/modelo_original/uss-enterprise-a-new-bridge/source/ENT-A1_dae/model/material_46.jpg` | .jpg | 43,357 | Sí | Textura Enterprise; 309×200 |
| `assets/enterprise_kelvin/modelo_original/uss-enterprise-a-new-bridge/source/ENT-A1_dae/model/material_48.jpg` | .jpg | 6,886 | Sí | Textura Enterprise; 148×220 |
| `assets/enterprise_kelvin/modelo_original/uss-enterprise-a-new-bridge/source/ENT-A1_dae/model/material_54.jpg` | .jpg | 9,336 | Sí | Textura Enterprise; 104×75 |
| `assets/enterprise_kelvin/modelo_original/uss-enterprise-a-new-bridge/source/ENT-A1_dae/model/material_7.jpg` | .jpg | 104,893 | Sí | Textura Enterprise; 300×438 |
| `assets/enterprise_kelvin/modelo_original/uss-enterprise-a-new-bridge/textures/Aluminum.jpeg` | .jpeg | 16,836 | Sí | Textura Enterprise; 530×530 |
| `assets/enterprise_kelvin/modelo_original/uss-enterprise-a-new-bridge/textures/Blinds_Roman_Hobbled_Blue.jpeg` | .jpeg | 4,935 | Sí | Textura Enterprise; 128×256 |
| `assets/enterprise_kelvin/modelo_original/uss-enterprise-a-new-bridge/textures/GRATE_GLOW.jpeg` | .jpeg | 191,956 | Sí | Textura Enterprise; 1227×590 |
| `assets/enterprise_kelvin/modelo_original/uss-enterprise-a-new-bridge/textures/HONEYCOMB_GLOW_2.jpeg` | .jpeg | 2,419,409 | Sí | Textura Enterprise; 1643×1459 |
| `assets/enterprise_kelvin/modelo_original/uss-enterprise-a-new-bridge/textures/NewTrekLCARS.jpeg` | .jpeg | 2,726,251 | Sí | Textura Enterprise; 2349×2099 |
| `assets/enterprise_kelvin/modelo_original/uss-enterprise-a-new-bridge/textures/VIEWSCREEN_GLOW.jpeg` | .jpeg | 99,161 | Sí | Textura Enterprise; 1073×208 |
| `assets/enterprise_kelvin/modelo_original/uss-enterprise-a-new-bridge/textures/_58cd499217289.560ca8b44d983.jpeg` | .jpeg | 234,441 | Sí | Textura Enterprise; 1024×646 |
| `assets/enterprise_kelvin/modelo_original/uss-enterprise-a-new-bridge/textures/__.jpeg` | .jpeg | 21,811 | Sí | Textura Enterprise; 600×600 |
| `assets/enterprise_kelvin/modelo_original/uss-enterprise-a-new-bridge/textures/internal_ground_ao_texture.jpeg` | .jpeg | 17,506 | Sí | Textura Enterprise; 512×512 |
| `assets/enterprise_kelvin/modelo_original/uss-enterprise-a-new-bridge/textures/iso_web_yellow2.jpeg` | .jpeg | 34,913 | Sí | Textura Enterprise; 390×806 |
| `assets/enterprise_kelvin/modelo_original/uss-enterprise-a-new-bridge/textures/material_28.inline_conv_generated.png` | .png | 41,436 | Sí | Textura Enterprise; 568×995 |
| `assets/enterprise_kelvin/modelo_original/uss-enterprise-a-new-bridge/textures/material_28.png` | .png | 229,029 | Sí | Textura Enterprise; 568×995 |
| `assets/enterprise_kelvin/modelo_original/uss-enterprise-a-new-bridge/textures/material_3.jpeg` | .jpeg | 16,783 | Sí | Textura Enterprise; 167×86 |
| `assets/enterprise_kelvin/modelo_original/uss-enterprise-a-new-bridge/textures/material_3_0.jpeg` | .jpeg | 13,444 | Sí | Textura Enterprise; 167×86 |
| `assets/enterprise_kelvin/modelo_original/uss-enterprise-a-new-bridge/textures/material_3_1.jpeg` | .jpeg | 13,410 | Sí | Textura Enterprise; 167×86 |
| `assets/enterprise_kelvin/modelo_original/uss-enterprise-a-new-bridge/textures/material_4.jpeg` | .jpeg | 870 | Sí | Textura Enterprise; 21×21 |
| `assets/enterprise_kelvin/modelo_original/uss-enterprise-a-new-bridge/textures/material_43.jpeg` | .jpeg | 115,341 | Sí | Textura Enterprise; 313×397 |
| `assets/enterprise_kelvin/modelo_original/uss-enterprise-a-new-bridge/textures/material_44.jpeg` | .jpeg | 34,291 | Sí | Textura Enterprise; 167×197 |
| `assets/enterprise_kelvin/modelo_original/uss-enterprise-a-new-bridge/textures/material_46.jpeg` | .jpeg | 43,333 | Sí | Textura Enterprise; 309×200 |
| `assets/enterprise_kelvin/modelo_original/uss-enterprise-a-new-bridge/textures/material_48.jpeg` | .jpeg | 6,886 | Sí | Textura Enterprise; 148×220 |
| `assets/enterprise_kelvin/modelo_original/uss-enterprise-a-new-bridge/textures/material_54.jpeg` | .jpeg | 9,336 | Sí | Textura Enterprise; 104×75 |
| `assets/enterprise_kelvin/modelo_original/uss-enterprise-a-new-bridge/textures/material_7.jpeg` | .jpeg | 104,893 | Sí | Textura Enterprise; 300×438 |
| `assets/enterprise_kelvin/texturas_originales/.gitkeep` | (sin extension) | 0 | No | Marcador de carpeta |
| `assets/otros/Danube simulador/star-trek-ds9-danube-runabout-rio-grande-cockpit.zip` | .zip | 29,627,139 | Sí | Biblioteca auxiliar independiente |
| `assets/otros/Danube simulador/star_trek_ds9_danube_runabout_rio_grande_cockpit.glb` | .glb | 18,045,284 | Sí | Biblioteca auxiliar independiente |
| `assets/otros/Danube simulador/star_trek_ds9_danube_runabout_rio_grande_cockpit.zip` | .zip | 16,705,517 | Sí | Biblioteca auxiliar independiente |
| `assets/otros/NPC/7 de 9/seven-of-nine.zip` | .zip | 33,813,623 | Sí | Biblioteca auxiliar independiente |
| `assets/otros/NPC/7 de 9/seven_of_nine.glb` | .glb | 36,617,688 | Sí | Biblioteca auxiliar independiente |
| `assets/otros/NPC/7 de 9/seven_of_nine.zip` | .zip | 35,518,427 | Sí | Biblioteca auxiliar independiente |
| `assets/otros/NPC/Piccard/patrick-stewart-star-trek.zip` | .zip | 18,886,500 | Sí | Biblioteca auxiliar independiente |
| `assets/otros/NPC/Piccard/patrick_stewart_star_trek.glb` | .glb | 7,758,024 | Sí | Biblioteca auxiliar independiente |
| `assets/otros/hangar/Low Poly Corridor - [Star Trek]/low-poly-corridor-star-trek.zip` | .zip | 1,335,524 | Sí | Biblioteca auxiliar independiente |
| `assets/otros/hangar/Low Poly Corridor - [Star Trek]/low_poly_corridor_-_star_trek.glb` | .glb | 1,073,456 | Sí | Biblioteca auxiliar independiente |
| `assets/otros/hangar/Low Poly Corridor - [Star Trek]/low_poly_corridor_-_star_trek_PBR_Compat_6997a32b7a8d44a8a250f9332cb2f180.glb` | .glb | 1,073,832 | Sí | Biblioteca auxiliar independiente |
| `assets/otros/hangar/enterprise-corridor.zip` | .zip | 1,050,962 | Sí | Biblioteca auxiliar independiente |
| `assets/otros/hangar/enterprise_corridor.glb` | .glb | 2,134,976 | Sí | Biblioteca auxiliar independiente |
| `assets/otros/hangar/modular-star-trek-corridor.zip` | .zip | 3,372,116 | Sí | Biblioteca auxiliar independiente |
| `assets/otros/hangar/star_trek_hangar.glb` | .glb | 4,682,108 | Sí | Biblioteca auxiliar independiente |
| `assets/otros/replicator/henry_star_trek_tng_replicator.glb` | .glb | 658,856 | Sí | Biblioteca auxiliar independiente |
| `assets/otros/vehicles/rover/argo-ii-type-rover-star-trek-zeo.zip` | .zip | 71,403,650 | Sí | Biblioteca auxiliar independiente |
| `assets/otros/vehicles/rover/argo_ii_type_rover_star_trek_zeo.glb` | .glb | 92,734,984 | Sí | Biblioteca auxiliar independiente |
| `assets/otros/vehicles/rover/argo_ii_type_rover_star_trek_zeo.zip` | .zip | 56,113,365 | Sí | Biblioteca auxiliar independiente |
| `assets/uss_theurgy/imagenes_puente/.gitkeep` | (sin extension) | 0 | No | Marcador de carpeta |
| `assets/uss_theurgy/imagenes_puente/45 grados.png` | .png | 345,715 | Sí | Referencia restringida; solo metadatos; 996×676 |
| `assets/uss_theurgy/imagenes_puente/Anexo 2.png` | .png | 2,036,967 | Sí | Referencia restringida; solo metadatos; 2256×1074 |
| `assets/uss_theurgy/imagenes_puente/Anexo.png` | .png | 1,773,938 | Sí | Referencia restringida; solo metadatos; 2248×1078 |
| `assets/uss_theurgy/imagenes_puente/Back view.png` | .png | 1,035,652 | Sí | Referencia restringida; solo metadatos; 2089×1015 |
| `assets/uss_theurgy/imagenes_puente/Consola CONN y vuelo.png` | .png | 1,257,285 | Sí | Referencia restringida; solo metadatos; 1903×807 |
| `assets/uss_theurgy/imagenes_puente/Consola lateral 2.png` | .png | 2,289,563 | Sí | Referencia restringida; solo metadatos; 2238×1083 |
| `assets/uss_theurgy/imagenes_puente/Consola lateral.png` | .png | 997,912 | Sí | Referencia restringida; solo metadatos; 2223×1084 |
| `assets/uss_theurgy/imagenes_puente/Silla capitan.png` | .png | 1,449,180 | Sí | Referencia restringida; solo metadatos; 2266×1081 |
| `assets/uss_theurgy/imagenes_puente/frontal.png` | .png | 406,971 | Sí | Referencia restringida; solo metadatos; 835×666 |
| `assets/uss_theurgy/imagenes_puente/zenital.png` | .png | 483,104 | Sí | Referencia restringida; solo metadatos; 937×952 |
| `assets/uss_theurgy/planos/.gitkeep` | (sin extension) | 0 | No | Marcador de carpeta |
| `blender/backups/.gitkeep` | (sin extension) | 0 | No | Marcador de carpeta |
| `blender/componentes/.gitkeep` | (sin extension) | 0 | No | Marcador de carpeta |
| `blender/principal/.gitkeep` | (sin extension) | 0 | No | Marcador de carpeta |
| `docs/.gitkeep` | (sin extension) | 0 | No | Marcador de carpeta |
| `docs/materiales/BIBLIOTECA_PBR_ROBDEV.md` | .md | 10,027 | No | Configuración o documentación |
| `docs/puente-kelvin/PLAN.md` | .md | 3,666 | No | Configuración o documentación |
| `docs/uss-theurgy/DISENO_MAESTRO.md` | .md | 15,514 | No | Configuración o documentación |
| `docs/uss-theurgy/UE5_ESCENARIO_JUGABLE.md` | .md | 15,297 | No | Configuración o documentación |
| `output/capturas_revision/.gitkeep` | (sin extension) | 0 | No | Marcador de carpeta |
| `output/exportaciones/.gitkeep` | (sin extension) | 0 | No | Marcador de carpeta |
| `output/renders/.gitkeep` | (sin extension) | 0 | No | Marcador de carpeta |
| `scripts/blender_python/.gitkeep` | (sin extension) | 0 | No | Marcador de carpeta |
| `temp/.gitkeep` | (sin extension) | 0 | No | Marcador de carpeta |
| `tools/inventario_gltf.py` | .py | 6,739 | No | Herramienta glTF |

### Directorios internos de ZIP/USDZ

Miembros no extraídos. Tamaños descomprimidos; los paquetes anidados se indican con ↳. Miembros del ZIP DAE coinciden por SHA-256 con disco.

#### `assets/enterprise_kelvin/modelo_original/U.S.S.usdz`

| Miembro | Bytes | Observación |
| --- | ---: | --- |
| `scene.usdc` | 72,140,817 |  |
| `0/HONEYCOMB_GLOW_2_baseColor.jpg` | 1,197,366 |  |
| `0/VIEWSCREEN_GLOW_baseColor.jpg` | 54,114 |  |
| `0/Aluminum_baseColor.jpg` | 79,992 |  |
| `0/iso_web_yellow2_baseColor.jpg` | 50,819 |  |
| `0/GRATE_GLOW_baseColor.jpg` | 163,079 |  |
| `0/NewTrekLCARS_baseColor.jpg` | 2,136,005 |  |
| `0/Blinds_Roman_Hobbled_Blue_baseColor.jpg` | 9,616 |  |
| `0/58cd499217289.560ca8b44d983_baseColor.jpg` | 188,410 |  |
| `0/material_35_baseColor.jpg` | 84,466 |  |
| `0/material_4_baseColor.jpg` | 397 |  |
| `0/material_44_baseColor.jpg` | 16,677 |  |
| `0/material_46_baseColor.jpg` | 25,465 |  |
| `0/material_7_baseColor.jpg` | 56,001 |  |
| `0/material_48_baseColor.jpg` | 10,261 |  |
| `0/material_3_baseColor.jpg` | 8,560 |  |
| `0/material_3_0_baseColor.jpg` | 7,549 |  |
| `0/material_54_baseColor.jpg` | 4,396 |  |
| `0/material_3_1_baseColor.jpg` | 7,472 |  |
| `0/material_28_baseColor.png` | 161,924 | ; 512×512 |
| `0/material_43_baseColor.jpg` | 56,510 |  |

#### `assets/enterprise_kelvin/modelo_original/uss-enterprise-a-new-bridge/source/ENT-A1_dae.zip`

| Miembro | Bytes | Observación |
| --- | ---: | --- |
| `model/Aluminum.jpg` | 12,471 | SHA-256 coincide con disco |
| `model/Blinds_Roman_Hobbled_Blue.jpg` | 4,097 | SHA-256 coincide con disco |
| `model/GRATE_GLOW.jpg` | 192,060 | SHA-256 coincide con disco |
| `model/HONEYCOMB_GLOW_2.jpg` | 2,419,513 | SHA-256 coincide con disco |
| `model/iso_web_yellow2.jpg` | 34,913 | SHA-256 coincide con disco |
| `model/material_28.png` | 229,353 | SHA-256 coincide con disco; 568×995 |
| `model/material_3.jpg` | 16,783 | SHA-256 coincide con disco |
| `model/material_3_0.jpg` | 13,468 | SHA-256 coincide con disco |
| `model/material_3_1.jpg` | 13,434 | SHA-256 coincide con disco |
| `model/material_4.jpg` | 894 | SHA-256 coincide con disco |
| `model/material_43.jpg` | 115,341 | SHA-256 coincide con disco |
| `model/material_44.jpg` | 34,315 | SHA-256 coincide con disco |
| `model/material_46.jpg` | 43,357 | SHA-256 coincide con disco |
| `model/material_48.jpg` | 6,886 | SHA-256 coincide con disco |
| `model/material_54.jpg` | 9,336 | SHA-256 coincide con disco |
| `model/material_7.jpg` | 104,893 | SHA-256 coincide con disco |
| `model/NewTrekLCARS.jpg` | 2,726,355 | SHA-256 coincide con disco |
| `model/VIEWSCREEN_GLOW.jpg` | 99,265 | SHA-256 coincide con disco |
| `model/_58cd499217289.560ca8b44d983.jpg` | 234,545 | SHA-256 coincide con disco |
| `model/__.jpg` | 21,835 | SHA-256 coincide con disco |
| `model.dae` | 84,248,309 | SHA-256 coincide con disco |

#### `assets/otros/hangar/modular-star-trek-corridor.zip`

| Miembro | Bytes | Observación |
| --- | ---: | --- |
| `source/Star Trek Corridor.blend` | 3,371,956 | ; Blender 2.79 |

#### `assets/otros/Danube simulador/star-trek-ds9-danube-runabout-rio-grande-cockpit.zip`

| Miembro | Bytes | Observación |
| --- | ---: | --- |
| `source/runabout cockpit 6.zip` | 4,343,185 |  |
| ↳ `runabout cockpit 6.obj` | 4,343,027 |  |
| `textures/runabout_cockpit_textures_4.png` | 6,233,950 | ; 2048×2048 |
| `textures/runabout_cockpit_lights_2.png` | 2,441,210 | ; 2048×2048 |
| `textures/runabout_cockpit_textures_4_DISP.png` | 4,649,851 | ; 2048×2048 |
| `textures/runabout_cockpit_textures_4_NORM.png` | 11,958,147 | ; 2048×2048 |

#### `assets/otros/Danube simulador/star_trek_ds9_danube_runabout_rio_grande_cockpit.zip`

| Miembro | Bytes | Observación |
| --- | ---: | --- |
| `license.txt` | 826 |  |
| `scene.bin` | 2,342,184 |  |
| `scene.gltf` | 37,291 |  |
| `textures/` | 0 |  |
| `textures/Grey_baseColor.png` | 6,151,276 | ; 2048×2048 |
| `textures/Grey_emissive.png` | 2,423,764 | ; 2048×2048 |
| `textures/Grey_specularf0.png` | 1,514,611 | ; 2048×2048 |
| `textures/Material.001_normal.png` | 4,349,357 | ; 2048×2048 |
| `textures/Trek_Black_metallicRoughness.png` | 1,243,103 | ; 2048×2048 |

#### `assets/otros/NPC/7 de 9/seven-of-nine.zip`

| Miembro | Bytes | Observación |
| --- | ---: | --- |
| `source/7of9_sketchfab.fbx` | 2,714,284 |  |
| `textures/7of9Body_normal.png` | 5,255,333 | ; 2048×2048 |
| `textures/7of9Hair_normal.png` | 4,604,339 | ; 2048×2048 |
| `textures/7of9Body_albedo.jpeg` | 2,189,380 |  |
| `textures/eye_albedo.jpeg` | 327,523 |  |
| `textures/7of9Body_metallic.jpeg` | 175,852 |  |
| `textures/7of9Head_roughness.jpeg` | 1,696,795 |  |
| `textures/7of9Body_AO.jpeg` | 1,504,073 |  |
| `textures/7of9Hair_opacity.jpeg` | 226,761 |  |
| `textures/7of9Eyelashes_normal.png` | 113,794 | ; 512×512 |
| `textures/7of9Head_albedo.jpeg` | 861,699 |  |
| `textures/7of9Head_AO.jpeg` | 906,163 |  |
| `textures/7of9Hair_AO.jpeg` | 1,583,698 |  |
| `textures/7of9Hair_albedo.jpeg` | 2,956,143 |  |
| `textures/Mough_albedo.jpeg` | 305,464 |  |
| `textures/7of9Body_roughness.jpeg` | 2,349,808 |  |
| `textures/7of9Eyelashes_opacity.jpeg` | 74,380 |  |
| `textures/7of9Head_normal.png` | 4,623,247 | ; 2048×2048 |
| `textures/7of9Hair_roughness.jpeg` | 1,342,329 |  |

#### `assets/otros/NPC/7 de 9/seven_of_nine.zip`

| Miembro | Bytes | Observación |
| --- | ---: | --- |
| `license.txt` | 678 |  |
| `scene.bin` | 1,778,572 |  |
| `scene.gltf` | 137,605 |  |
| `textures/` | 0 |  |
| `textures/7of9Body_baseColor.jpeg` | 1,366,559 |  |
| `textures/7of9Body_metallicRoughness.png` | 5,356,434 | ; 2048×2048 |
| `textures/7of9Body_normal.png` | 4,851,306 | ; 2048×2048 |
| `textures/7of9Eyelashes_baseColor.png` | 54,513 | ; 512×512 |
| `textures/7of9Eyelashes_normal.png` | 105,911 | ; 512×512 |
| `textures/7of9Hair_baseColor.png` | 5,485,934 | ; 2048×2048 |
| `textures/7of9Hair_metallicRoughness.png` | 4,143,632 | ; 2048×2048 |
| `textures/7of9Hair_normal.png` | 4,384,410 | ; 2048×2048 |
| `textures/7of9Head_baseColor.jpeg` | 523,995 |  |
| `textures/7of9Head_metallicRoughness.png` | 3,811,507 | ; 2048×2048 |
| `textures/7of9Head_normal.png` | 4,325,641 | ; 2048×2048 |
| `textures/Mough_baseColor.jpeg` | 168,990 |  |
| `textures/material_baseColor.jpeg` | 181,431 |  |

#### `assets/otros/NPC/Piccard/patrick-stewart-star-trek.zip`

| Miembro | Bytes | Observación |
| --- | ---: | --- |
| `source/model.zip` | 14,097,339 |  |
| ↳ `source/model.zip` | 9,308,178 |  |
| ↳ ↳ `MAT_PatrickStewart_StarTrek_normal.jpg` | 2,760,722 |  |
| ↳ ↳ `MAT_PatrickStewart_StarTrek_basecolor.jpg` | 2,219,008 |  |
| ↳ ↳ `mesh.fbx` | 4,328,024 |  |
| ↳ `textures/MAT_PatrickStewart_StarTrek_basecolor.jpeg` | 2,143,779 |  |
| ↳ `textures/MAT_PatrickStewart_StarTrek_normal.jpeg` | 2,644,902 |  |
| `textures/MAT_PatrickStewart_StarTrek_basecolor.jpeg` | 2,143,779 |  |
| `textures/MAT_PatrickStewart_StarTrek_normal.jpeg` | 2,644,902 |  |

#### `assets/otros/hangar/enterprise-corridor.zip`

| Miembro | Bytes | Observación |
| --- | ---: | --- |
| `source/Sketchfab_2022_10_07_12_02_44.blend` | 1,037,123 | ; cabecera comprimida; versión no identificada |
| `textures/internal_ground_ao_texture.jpeg` | 13,501 |  |

#### `assets/otros/hangar/Low Poly Corridor - [Star Trek]/low-poly-corridor-star-trek.zip`

| Miembro | Bytes | Observación |
| --- | ---: | --- |
| `source/Cooridoor test.blend` | 1,335,372 | ; Blender 2.79 |

#### `assets/otros/vehicles/rover/argo-ii-type-rover-star-trek-zeo.zip`

| Miembro | Bytes | Observación |
| --- | ---: | --- |
| `source/Argo_II_objFiles.zip` | 46,220,464 |  |
| ↳ `Argo_II.png` | 221,362 |  |
| ↳ `material_10_ca.png` | 9,979 |  |
| ↳ `material_10_ng.png` | 79,538 |  |
| ↳ `material_11_ca.png` | 97,432 |  |
| ↳ `material_12_ca.png` | 45,069 |  |
| ↳ `material_12_ng.png` | 77,434 |  |
| ↳ `material_13_ca.png` | 46,839 |  |
| ↳ `material_14_ca.png` | 78,647 |  |
| ↳ `material_15_ca.png` | 37,626 |  |
| ↳ `material_16_ca.png` | 550,966 |  |
| ↳ `material_16_ng.png` | 1,685,330 |  |
| ↳ `material_17_ca.png` | 373,460 |  |
| ↳ `material_18_ca.png` | 588,658 |  |
| ↳ `material_18_ng.png` | 6,527 |  |
| ↳ `material_19_ca.png` | 373,839 |  |
| ↳ `material_19_ng.png` | 251,516 |  |
| ↳ `material_1_ca.png` | 87,501 |  |
| ↳ `material_1_ng.png` | 146,912 |  |
| ↳ `material_20_ca.png` | 1,084,820 |  |
| ↳ `material_21_ca.png` | 294,075 |  |
| ↳ `material_21_ng.png` | 275,468 |  |
| ↳ `material_22_ca.png` | 210,288 |  |
| ↳ `material_23_ca.png` | 204,249 |  |
| ↳ `material_24_ca.png` | 570,894 |  |
| ↳ `material_25_ca.png` | 634,231 |  |
| ↳ `material_26_ca.png` | 570,894 |  |
| ↳ `material_27_ca.png` | 1,449,337 |  |
| ↳ `material_27_ng.png` | 1,110,470 |  |
| ↳ `material_28_ca.png` | 92,431 |  |
| ↳ `material_28_ng.png` | 110,312 |  |
| ↳ `material_29_ca.png` | 294,075 |  |
| ↳ `material_2_ca.png` | 34,159 |  |
| ↳ `material_2_ng.png` | 4,993 |  |
| ↳ `material_30_ca.png` | 182,407 |  |
| ↳ `material_30_ng.png` | 387,869 |  |
| ↳ `material_31_ca.png` | 210,291 |  |
| ↳ `material_32_ca.png` | 267,487 |  |
| ↳ `material_32_ng.png` | 387,869 |  |
| ↳ `material_33_ca.png` | 210,961 |  |
| ↳ `material_34_ca.png` | 194,215 |  |
| ↳ `material_34_ng.png` | 267,617 |  |
| ↳ `material_36_ca.png` | 373,460 |  |
| ↳ `material_37_ca.png` | 240,235 |  |
| ↳ `material_37_ng.png` | 51,625 |  |
| ↳ `material_38_ca.png` | 373,839 |  |
| ↳ `material_39_ca.png` | 588,658 |  |
| ↳ `material_3_ca.png` | 114,809 |  |
| ↳ `material_3_ng.png` | 155,929 |  |
| ↳ `material_40_ca.png` | 1,084,820 |  |
| ↳ `material_41_ca.png` | 74,167 |  |
| ↳ `material_41_ng.png` | 266,746 |  |
| ↳ `material_42_ca.png` | 158,052 |  |
| ↳ `material_42_ng.png` | 345,737 |  |
| ↳ `material_43_ca.png` | 69,925 |  |
| ↳ `material_43_ng.png` | 144,301 |  |
| ↳ `material_44_ca.png` | 148,960 |  |
| ↳ `material_44_ng.png` | 335,638 |  |
| ↳ `material_45_ca.png` | 47,286 |  |
| ↳ `material_45_ng.png` | 36,188 |  |
| ↳ `material_46_ca.png` | 84,532 |  |
| ↳ `material_46_ng.png` | 144,301 |  |
| ↳ `material_47_ca.png` | 224,645 |  |
| ↳ `material_47_ng.png` | 99 |  |
| ↳ `material_48_ca.png` | 117 |  |
| ↳ `material_48_ng.png` | 99 |  |
| ↳ `material_49_ca.png` | 92,427 |  |
| ↳ `material_4_ca.png` | 148,090 |  |
| ↳ `material_4_ng.png` | 75,652 |  |
| ↳ `material_50_ca.png` | 41,603 |  |
| ↳ `material_50_ng.png` | 70,428 |  |
| ↳ `material_51_ca.png` | 1,449,337 |  |
| ↳ `material_52_ca.png` | 579,986 |  |
| ↳ `material_53_ca.png` | 570,894 |  |
| ↳ `material_55_ca.png` | 92,427 |  |
| ↳ `material_56_ca.png` | 12,546 |  |
| ↳ `material_56_ng.png` | 10,914 |  |
| ↳ `material_57_ca.png` | 74,167 |  |
| ↳ `material_58_ca.png` | 92,431 |  |
| ↳ `material_59_ca.png` | 182,409 |  |
| ↳ `material_5_ca.png` | 33,454 |  |
| ↳ `material_5_ng.png` | 19,087 |  |
| ↳ `material_60_ca.png` | 215,720 |  |
| ↳ `material_61_ca.png` | 194,222 |  |
| ↳ `material_62_ca.png` | 148,959 |  |
| ↳ `material_63_ca.png` | 102,144 |  |
| ↳ `material_65_ca.png` | 184,921 |  |
| ↳ `material_65_ng.png` | 94,779 |  |
| ↳ `material_66_ca.png` | 117 |  |
| ↳ `material_67_ca.png` | 21,137 |  |
| ↳ `material_68_ca.png` | 109,725 |  |
| ↳ `material_69_ca.png` | 47,289 |  |
| ↳ `material_6_ca.png` | 82,378 |  |
| ↳ `material_6_ng.png` | 151,423 |  |
| ↳ `material_70_ca.png` | 210,288 |  |
| ↳ `material_71_ca.png` | 203,173 |  |
| ↳ `material_72_ca.png` | 28,909 |  |
| ↳ `material_73_ca.png` | 30,249 |  |
| ↳ `material_74_ca.png` | 134,610 |  |
| ↳ `material_75_ca.png` | 1,239,118 |  |
| ↳ `material_75_ng.png` | 1,548,309 |  |
| ↳ `material_76_ca.png` | 373,460 |  |
| ↳ `material_77_ca.png` | 1,084,820 |  |
| ↳ `material_78_ca.png` | 373,839 |  |
| ↳ `material_79_ca.png` | 588,658 |  |
| ↳ `material_7_ca.png` | 126,530 |  |
| ↳ `material_80_ca.png` | 294,075 |  |
| ↳ `material_8_ca.png` | 73,591 |  |
| ↳ `material_9_ca.png` | 80,455 |  |
| ↳ `Argo_II.obj` | 73,254,275 |  |
| ↳ `Argo_II.mtl` | 16,125 |  |
| `textures/material_22_ca.png` | 210,231 | ; 512×512 |
| `textures/material_79_ca.png` | 412,871 | ; 1024×1024 |
| `textures/material_20_ca.png` | 969,097 | ; 1024×1024 |
| `textures/material_69_ca.png` | 47,268 | ; 512×512 |
| `textures/material_41_ng.png` | 266,677 | ; 512×512 |
| `textures/material_51_ca.png` | 1,294,816 | ; 1024×1024 |
| `textures/material_65_ca.png` | 174,223 | ; 512×512 |
| `textures/material_16_ng.png` | 1,685,009 | ; 1024×1024 |
| `textures/material_5_ca.png` | 16,458 | ; 256×256 |
| `textures/material_46_ng.png` | 144,256 | ; 512×512 |
| `textures/material_48_ng.png` | 95 | ; 4×4 |
| `textures/material_66_ca.png` | 76 | ; 4×4 |
| `textures/material_56_ng.png` | 7,093 | ; 256×256 |
| `textures/material_50_ca.png` | 23,921 | ; 256×256 |
| `textures/material_19_ca.png` | 310,283 | ; 512×512 |
| `textures/material_71_ca.png` | 203,116 | ; 512×512 |
| `textures/material_63_ca.png` | 102,111 | ; 512×512 |
| `textures/material_78_ca.png` | 310,283 | ; 512×512 |
| `textures/material_59_ca.png` | 182,364 | ; 512×512 |
| `textures/material_53_ca.png` | 541,605 | ; 1024×1024 |
| `textures/material_42_ng.png` | 345,656 | ; 512×512 |
| `textures/material_21_ng.png` | 275,399 | ; 512×512 |
| `textures/material_41_ca.png` | 74,134 | ; 512×512 |
| `textures/material_4_ng.png` | 75,619 | ; 256×256 |
| `textures/material_33_ca.png` | 210,904 | ; 512×512 |
| `textures/material_19_ng.png` | 179,365 | ; 512×512 |
| `textures/material_57_ca.png` | 74,134 | ; 512×512 |
| `textures/material_49_ca.png` | 90,778 | ; 256×512 |
| `textures/material_18_ng.png` | 235 | ; 1024×1024 |
| `textures/material_36_ca.png` | 206,031 | ; 1024×1024 |
| `textures/material_32_ca.png` | 267,418 | ; 512×512 |
| `textures/material_30_ng.png` | 387,788 | ; 512×512 |
| `textures/material_47_ca.png` | 203,881 | ; 1024×1024 |
| `textures/material_15_ca.png` | 16,530 | ; 256×256 |
| `textures/material_5_ng.png` | 19,066 | ; 128×128 |
| `textures/material_18_ca.png` | 412,871 | ; 1024×1024 |
| `textures/material_29_ca.png` | 294,006 | ; 512×512 |
| `textures/material_58_ca.png` | 90,782 | ; 256×512 |
| `textures/material_50_ng.png` | 70,395 | ; 256×256 |
| `textures/material_23_ca.png` | 204,192 | ; 512×512 |
| `textures/material_38_ca.png` | 310,283 | ; 512×512 |
| `textures/material_65_ng.png` | 94,746 | ; 512×512 |
| `textures/material_28_ng.png` | 110,279 | ; 256×512 |
| `textures/material_75_ng.png` | 1,548,012 | ; 1024×1024 |
| `textures/material_27_ng.png` | 1,110,257 | ; 1024×1024 |
| `textures/material_6_ng.png` | 151,378 | ; 512×256 |
| `textures/material_61_ca.png` | 194,177 | ; 512×512 |
| `textures/material_26_ca.png` | 541,605 | ; 1024×1024 |
| `textures/material_48_ca.png` | 76 | ; 4×4 |
| `textures/material_27_ca.png` | 1,294,816 | ; 1024×1024 |
| `textures/material_68_ca.png` | 94,423 | ; 512×512 |
| `textures/material_21_ca.png` | 294,006 | ; 512×512 |
| `textures/material_76_ca.png` | 206,031 | ; 1024×1024 |
| `textures/material_34_ng.png` | 267,548 | ; 512×512 |
| `textures/material_42_ca.png` | 158,007 | ; 512×512 |
| `textures/material_7_ca.png` | 58,939 | ; 512×512 |
| `textures/material_52_ca.png` | 237,042 | ; 1024×1024 |
| `textures/material_45_ng.png` | 36,167 | ; 512×512 |
| `textures/material_14_ca.png` | 32,658 | ; 512×256 |
| `textures/material_74_ca.png` | 64,126 | ; 512×512 |
| `textures/material_55_ca.png` | 90,778 | ; 256×512 |
| `textures/material_30_ca.png` | 182,362 | ; 512×512 |
| `textures/material_2_ng.png` | 4,972 | ; 64×64 |
| `textures/material_31_ca.png` | 210,234 | ; 512×512 |
| `textures/material_75_ca.png` | 1,183,423 | ; 1024×1024 |
| `textures/material_70_ca.png` | 210,231 | ; 512×512 |
| `textures/material_77_ca.png` | 969,097 | ; 1024×1024 |
| `textures/material_28_ca.png` | 90,782 | ; 256×512 |
| `textures/material_62_ca.png` | 148,914 | ; 512×512 |
| `textures/material_44_ng.png` | 335,557 | ; 512×512 |
| `textures/material_37_ng.png` | 51,604 | ; 256×256 |
| `textures/material_12_ca.png` | 17,061 | ; 256×256 |
| `textures/material_40_ca.png` | 969,097 | ; 1024×1024 |
| `textures/material_17_ca.png` | 206,031 | ; 1024×1024 |
| `textures/material_37_ca.png` | 237,040 | ; 512×512 |
| `textures/material_34_ca.png` | 194,170 | ; 512×512 |
| `textures/material_12_ng.png` | 77,401 | ; 256×256 |
| `textures/material_67_ca.png` | 21,116 | ; 256×256 |
| `textures/material_60_ca.png` | 215,663 | ; 512×512 |
| `textures/material_46_ca.png` | 84,499 | ; 512×512 |
| `textures/material_32_ng.png` | 387,788 | ; 512×512 |
| `textures/material_24_ca.png` | 541,605 | ; 1024×1024 |
| `textures/material_3_ng.png` | 155,884 | ; 512×256 |
| `textures/material_43_ng.png` | 144,256 | ; 512×512 |
| `textures/material_39_ca.png` | 412,871 | ; 1024×1024 |
| `textures/material_16_ca.png` | 237,087 | ; 1024×1024 |
| `textures/material_56_ca.png` | 8,396 | ; 256×256 |
| `textures/material_43_ca.png` | 69,892 | ; 512×512 |
| `textures/material_44_ca.png` | 148,915 | ; 512×512 |
| `textures/material_80_ca.png` | 294,006 | ; 512×512 |
| `textures/material_13_ca.png` | 17,253 | ; 256×256 |
| `textures/material_45_ca.png` | 47,265 | ; 512×512 |
| `textures/material_47_ng.png` | 95 | ; 4×4 |

#### `assets/otros/vehicles/rover/argo_ii_type_rover_star_trek_zeo.zip`

| Miembro | Bytes | Observación |
| --- | ---: | --- |
| `license.txt` | 804 |  |
| `scene.bin` | 67,996,460 |  |
| `scene.gltf` | 193,864 |  |
| `textures/` | 0 |  |
| `textures/material_10_emissive.png` | 4,626 | ; 128×128 |
| `textures/material_11_emissive.png` | 43,097 | ; 512×256 |
| `textures/material_12_baseColor.png` | 20,309 | ; 256×256 |
| `textures/material_12_normal.png` | 19,060 | ; 256×256 |
| `textures/material_13_baseColor.png` | 20,536 | ; 256×256 |
| `textures/material_14_baseColor.png` | 37,446 | ; 512×256 |
| `textures/material_14_normal.png` | 46,780 | ; 512×256 |
| `textures/material_15_baseColor.png` | 18,688 | ; 256×256 |
| `textures/material_15_normal.png` | 8,911 | ; 128×128 |
| `textures/material_16_baseColor.png` | 274,688 | ; 1024×1024 |
| `textures/material_16_normal.png` | 641,921 | ; 1024×1024 |
| `textures/material_17_baseColor.png` | 288,201 | ; 1024×1024 |
| `textures/material_18_baseColor.png` | 482,895 | ; 1024×1024 |
| `textures/material_18_normal.png` | 222 | ; 1024×1024 |
| `textures/material_19_baseColor.png` | 316,669 | ; 512×512 |
| `textures/material_19_normal.png` | 1,396 | ; 512×512 |
| `textures/material_1_emissive.png` | 39,890 | ; 512×256 |
| `textures/material_20_baseColor.png` | 910,377 | ; 1024×1024 |
| `textures/material_21_baseColor.png` | 289,364 | ; 512×512 |
| `textures/material_21_emissive.png` | 215,880 | ; 512×512 |
| `textures/material_21_normal.png` | 109,372 | ; 512×512 |
| `textures/material_22_baseColor.png` | 215,977 | ; 512×512 |
| `textures/material_22_emissive.png` | 161,451 | ; 512×512 |
| `textures/material_23_baseColor.png` | 207,814 | ; 512×512 |
| `textures/material_23_emissive.png` | 151,789 | ; 512×512 |
| `textures/material_24_baseColor.png` | 489,292 | ; 1024×1024 |
| `textures/material_25_emissive.png` | 275,872 | ; 1024×1024 |
| `textures/material_26_baseColor.png` | 489,292 | ; 1024×1024 |
| `textures/material_27_baseColor.png` | 1,261,734 | ; 1024×1024 |
| `textures/material_27_normal.png` | 223,813 | ; 1024×1024 |
| `textures/material_28_baseColor.png` | 84,774 | ; 256×512 |
| `textures/material_28_normal.png` | 30,491 | ; 256×512 |
| `textures/material_29_baseColor.png` | 289,364 | ; 512×512 |
| `textures/material_29_emissive.png` | 215,880 | ; 512×512 |
| `textures/material_2_emissive.png` | 16,734 | ; 256×256 |
| `textures/material_30_baseColor.png` | 195,203 | ; 512×512 |
| `textures/material_30_emissive.png` | 117,977 | ; 512×512 |
| `textures/material_30_normal.png` | 180,902 | ; 512×512 |
| `textures/material_31_baseColor.png` | 215,978 | ; 512×512 |
| `textures/material_31_emissive.png` | 161,455 | ; 512×512 |
| `textures/material_32_baseColor.png` | 273,130 | ; 512×512 |
| `textures/material_32_emissive.png` | 240,380 | ; 512×512 |
| `textures/material_32_normal.png` | 180,902 | ; 512×512 |
| `textures/material_33_baseColor.png` | 212,554 | ; 512×512 |
| `textures/material_33_emissive.png` | 157,454 | ; 512×512 |
| `textures/material_34_baseColor.png` | 206,195 | ; 512×512 |
| `textures/material_34_emissive.png` | 111,115 | ; 512×512 |
| `textures/material_34_normal.png` | 161,355 | ; 512×512 |
| `textures/material_36_baseColor.png` | 288,201 | ; 1024×1024 |
| `textures/material_37_baseColor.png` | 210,947 | ; 512×512 |
| `textures/material_37_normal.png` | 932 | ; 256×256 |
| `textures/material_38_baseColor.png` | 316,669 | ; 512×512 |
| `textures/material_39_baseColor.png` | 482,895 | ; 1024×1024 |
| `textures/material_3_emissive.png` | 47,360 | ; 512×256 |
| `textures/material_3_normal.png` | 39,489 | ; 512×256 |
| `textures/material_40_baseColor.png` | 910,377 | ; 1024×1024 |
| `textures/material_41_baseColor.png` | 65,492 | ; 512×512 |
| `textures/material_41_normal.png` | 64,567 | ; 512×512 |
| `textures/material_42_baseColor.png` | 155,968 | ; 512×512 |
| `textures/material_42_emissive.png` | 138,873 | ; 512×512 |
| `textures/material_42_normal.png` | 180,653 | ; 512×512 |
| `textures/material_43_baseColor.png` | 75,721 | ; 512×512 |
| `textures/material_43_emissive.png` | 65,703 | ; 512×512 |
| `textures/material_43_normal.png` | 96,750 | ; 512×512 |
| `textures/material_44_baseColor.png` | 143,868 | ; 512×512 |
| `textures/material_44_emissive.png` | 124,495 | ; 512×512 |
| `textures/material_44_normal.png` | 189,587 | ; 512×512 |
| `textures/material_45_baseColor.png` | 48,075 | ; 512×512 |
| `textures/material_45_emissive.png` | 39,401 | ; 512×512 |
| `textures/material_45_normal.png` | 8,923 | ; 512×512 |
| `textures/material_46_baseColor.png` | 87,009 | ; 512×512 |
| `textures/material_46_emissive.png` | 77,033 | ; 512×512 |
| `textures/material_46_normal.png` | 96,750 | ; 512×512 |
| `textures/material_47_baseColor.png` | 195,453 | ; 1024×1024 |
| `textures/material_47_normal.png` | 83 | ; 4×4 |
| `textures/material_48_baseColor.png` | 77 | ; 4×4 |
| `textures/material_48_normal.png` | 83 | ; 4×4 |
| `textures/material_49_baseColor.png` | 84,768 | ; 256×512 |
| `textures/material_4_emissive.png` | 70,716 | ; 512×512 |
| `textures/material_50_baseColor.png` | 32,286 | ; 256×256 |
| `textures/material_50_normal.png` | 16,302 | ; 256×256 |
| `textures/material_51_baseColor.png` | 1,261,734 | ; 1024×1024 |
| `textures/material_52_baseColor.png` | 274,654 | ; 1024×1024 |
| `textures/material_53_baseColor.png` | 489,292 | ; 1024×1024 |
| `textures/material_55_baseColor.png` | 84,768 | ; 256×512 |
| `textures/material_56_baseColor.png` | 9,011 | ; 256×256 |
| `textures/material_56_emissive.png` | 370 | ; 256×256 |
| `textures/material_56_normal.png` | 103 | ; 256×256 |
| `textures/material_57_baseColor.png` | 65,492 | ; 512×512 |
| `textures/material_58_baseColor.png` | 84,774 | ; 256×512 |
| `textures/material_59_baseColor.png` | 195,200 | ; 512×512 |
| `textures/material_59_emissive.png` | 117,977 | ; 512×512 |
| `textures/material_5_baseColor.png` | 18,635 | ; 256×256 |
| `textures/material_60_baseColor.png` | 225,805 | ; 512×512 |
| `textures/material_60_emissive.png` | 197,103 | ; 512×512 |
| `textures/material_61_baseColor.png` | 206,196 | ; 512×512 |
| `textures/material_61_emissive.png` | 111,117 | ; 512×512 |
| `textures/material_62_baseColor.png` | 143,863 | ; 512×512 |
| `textures/material_62_emissive.png` | 124,493 | ; 512×512 |
| `textures/material_63_baseColor.png` | 97,982 | ; 512×512 |
| `textures/material_63_emissive.png` | 84,429 | ; 512×512 |
| `textures/material_65_baseColor.png` | 174,059 | ; 512×512 |
| `textures/material_65_normal.png` | 146 | ; 512×512 |
| `textures/material_66_baseColor.png` | 77 | ; 4×4 |
| `textures/material_67_baseColor.png` | 20,255 | ; 256×256 |
| `textures/material_67_emissive.png` | 8,184 | ; 256×256 |
| `textures/material_68_baseColor.png` | 91,902 | ; 512×512 |
| `textures/material_69_baseColor.png` | 48,071 | ; 512×512 |
| `textures/material_69_emissive.png` | 39,402 | ; 512×512 |
| `textures/material_6_emissive.png` | 38,027 | ; 512×256 |
| `textures/material_70_baseColor.png` | 215,976 | ; 512×512 |
| `textures/material_70_emissive.png` | 161,450 | ; 512×512 |
| `textures/material_71_baseColor.png` | 209,240 | ; 512×512 |
| `textures/material_71_emissive.png` | 151,755 | ; 512×512 |
| `textures/material_72_emissive.png` | 15,250 | ; 256×256 |
| `textures/material_73_emissive.png` | 16,518 | ; 256×256 |
| `textures/material_73_normal.png` | 1,696 | ; 64×64 |
| `textures/material_74_baseColor.png` | 71,473 | ; 512×512 |
| `textures/material_74_normal.png` | 20,949 | ; 256×256 |
| `textures/material_75_baseColor.png` | 1,110,176 | ; 1024×1024 |
| `textures/material_75_normal.png` | 1,111,846 | ; 1024×1024 |
| `textures/material_76_baseColor.png` | 288,201 | ; 1024×1024 |
| `textures/material_77_baseColor.png` | 910,377 | ; 1024×1024 |
| `textures/material_78_baseColor.png` | 316,669 | ; 512×512 |
| `textures/material_79_baseColor.png` | 482,895 | ; 1024×1024 |
| `textures/material_7_baseColor.png` | 66,081 | ; 512×512 |
| `textures/material_80_baseColor.png` | 289,364 | ; 512×512 |
| `textures/material_80_emissive.png` | 215,880 | ; 512×512 |
| `textures/material_8_emissive.png` | 37,493 | ; 512×256 |
| `textures/material_9_emissive.png` | 37,959 | ; 512×256 |

## 13. Entregables y estado final

- `docs/auditorias/INVENTARIO_LOCAL_INICIAL.md`: informe y tablas completas.
- `docs/auditorias/INVENTARIO_LOCAL_DATOS.json`: evidencia textual de metadatos, hashes, estructuras y verificación.

Archivos previos conservados; sin commit ni push. Sigue pendiente la vía validada de importación del puente, escala funcional, correspondencia semántica y ensayo UE5.
