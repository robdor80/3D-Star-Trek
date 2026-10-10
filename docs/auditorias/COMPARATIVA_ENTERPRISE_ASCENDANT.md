# Comparativa técnica Enterprise / USS Ascendant

10 de octubre de 2026 · MSI Windows · Blender **5.2.2 LTS**, build `d13f752e3b9c` · Rama `audit/ascendant-vs-enterprise` · HEAD inicial `33ac98e`.

## 1. Resultado y alcance

**Recomendación A: mantener Enterprise como base para desarrollar Theurgy.** La recomendación no cambia la base oficial, el canon ni las escenas. Ascendant comparte casi toda la arquitectura de Enterprise y no resuelve sus principales barreras de circulación, desniveles o conexión posterior. Enterprise ofrece un sillón de capitán y un conjunto CONN considerablemente más simples y con datos de malla exclusivos de sus respectivos conjuntos. Ascendant separa mejor las dos estaciones centrales por padres y deja más distancia detrás de su silla central; estas ventajas no compensan, para la prioridad actual, la complejidad adicional y la ausencia de una mejora acreditada en navegación conectada.

La arquitectura común está **acreditada geométricamente**, más allá de dimensiones o materiales: **2.065.576 ocurrencias de triángulos emparejadas** con cuantización mundial de 0,1 mm, el **96,6005% de Enterprise** y el **83,7243% de Ascendant**. No queda demostrada la secuencia histórica de derivación ni que uno sea la versión posterior del otro.

Ambos superan el mismo ensayo geométrico de cinco tramos planos; ninguno tiene validada una red jugable completa. El prisma de la futura conexión Mission Ops intercepta **6.828 triángulos en cada modelo y los 6.828 coinciden** mediante el mismo criterio espacial. Tener 14 objetos afectados frente a 18 no reduce por sí solo la intervención arquitectónica.

No se modificaron activos, geometría, materiales ni transformaciones guardadas. No se guardaron escenas nuevas, no se instalaron herramientas y no se importó nada en UE5. Se generaron ocho vistas locales para revisión humana; **no fueron inspeccionadas visualmente por IA**. Tampoco se cargaron ni analizaron visualmente las referencias restringidas Theurgy.

## 2. Fuentes, controles y reproducibilidad

Se revisaron `AGENTS.md`, `README.md`, `.gitignore`, el encargo adjunto, `docs/puente-kelvin/PLAN.md`, `docs/uss-theurgy/DISENO_MAESTRO.md`, `docs/uss-theurgy/UE5_ESCENARIO_JUGABLE.md`, `docs/materiales/BIBLIOTECA_PBR_ROBDEV.md`, las auditorías geométricas de Enterprise y Ascendant, `ESCALA_Y_TRANSITABILIDAD_ENTERPRISE.md`, `PREPARACION_MISSION_OPS.md` y sus datos/scripts asociados. Se reutilizaron los inventarios anteriores; solo se repitieron pruebas necesarias para obtener criterios equivalentes y correspondencias nuevas.

Escenas abiertas, exclusivamente para lectura y cambios temporales de presentación en memoria:

| Escena | SHA-256 protegido |
| --- | --- |
| `blender/principal/enterprise_importacion_inicial.blend` | `0a55058552623995200fd5e16ddc327d5a6b2f6c54bbb9754f8340d01c885148` |
| `blender/analisis/ascendant_v1/ascendant_dae_analisis.blend` | `519b7905a663b6ab0a2f621d53af71979dbb91cd79a2c59fdae6af1fcc47a8ea` |
| `blender/principal/theurgy_trabajo_v0_1.blend`, protegida sin abrir | `a47bf96edd671bfbf6f68ccbadf8ee03938fd81e68df18ba3a41e65badefb093` |

Git estaba limpio, en la rama obligatoria. No se crearon ramas, commits ni pushes. [CONTROL_INICIAL.json](comparativa_v1/CONTROL_INICIAL.json) registra 278 archivos físicos de `assets/`, tres escenas protegidas y 33 informes previos. [VERIFICACION_FINAL.json](comparativa_v2/VERIFICACION_FINAL.json) registra el contraste final, comprobaciones de informes y capturas. Los informes anteriores se conservaron.

**Alta sobrevenida en la biblioteca:** durante el control final aparecieron 22 archivos adicionales en `assets/otros/bridges/USS Vengance bridge/`: dos ZIP, un DAE, un GLB y 18 imágenes externas. No fueron creados por los scripts de esta auditoría; no se determina su autor/proceso. Se registran rutas, tamaños, formatos y hashes finales en el control. Son recursos auxiliares independientes, fuera de la comparación de estos dos puentes; no se abrió su geometría ni se analizaron sus imágenes. El total final es 300 archivos de `assets/`. Los 278 iniciales conservan tamaños y SHA; no hubo bajas. No se presenta como idéntico el listado inicial/final cuando hubo esta incorporación.

Evidencias nuevas:

- [Correspondencia global](comparativa_v2/CORRESPONDENCIA_GEOMETRICA.json), [comprobaciones focales](comparativa_v2/CORRESPONDENCIAS_FOCALES.json), [resumen y metadatos fuente](comparativa_v2/RESUMEN_COMPARATIVO.json).
- [Ensayo Enterprise](comparativa_v2/ENTERPRISE_ENSAYO.json), [ensayo Ascendant](comparativa_v2/ASCENDANT_ENSAYO.json).
- [Mapa Enterprise](comparativa_v2/ENTERPRISE_DIFERENCIAS.csv), [mapa Ascendant](comparativa_v2/ASCENDANT_DIFERENCIAS.csv): una fila por objeto con caras, clasificación, caja, materiales y pertenencia a conjuntos; sin vértices ni texturas originales.
- [Conjuntos comparados](comparativa_v2/MODULOS_COMPARADOS.csv), [imágenes comunes por SHA](comparativa_v2/MATERIALES_PREVIOS.json), [procedencia pública](comparativa_v1/PROCEDENCIA_PUBLICA.json).
- Scripts nuevos: `comparar_puentes_dae.py`, `comprobar_correspondencias_focales.py`, `resumir_comparativa_puentes.py`, `capturar_comparativa_puentes.py` y `verificar_comparativa_puentes.py`, en `scripts/blender_python/`. Reutilizan funciones geométricas y topológicas anteriores. Los destinos nuevos y la prohibición de sobrescribir son deliberados; para repetir la comparación principal/capturas hay que elegir carpetas nuevas.

Se ejecutó Blender con `--disable-autoexec --background --factory-startup --python-exit-code 1`. La primera ejecución global se detuvo por una diferencia en la API de imágenes empaquetadas; se corrigió el acceso, y la ejecución completa produjo `comparativa_v2`. `comparativa_v1` conserva únicamente los controles iniciales y la procedencia, no un ensayo completo. No se cambió la configuración permanente de Blender.

## 3. Datos comparables, escala y orientación

Se comparan **dos puentes**, utilizando sus importaciones **DAE/Collada**, no el GLB de Ascendant ni los GLB de otras naves. El DAE no es glTF. La extensión Collada Support 1.2.2 ya instalada permitió las importaciones anteriores; esta fase abre los `.blend` existentes. `tools/inventario_gltf.py` no sirve para interpretar estos DAE.

| Métrica | Enterprise | Ascendant |
| --- | ---: | ---: |
| Objetos importados del puente | 12.451 | 14.177 |
| MESH / EMPTY / CAMERA / LIGHT del puente | 10.721 / 1.729 / 1 / 0 | 12.191 / 1.985 / 1 / 0 |
| Objetos MESH con caras | 9.785 | 11.179 |
| Bloques MESH totales / con caras | 2.526 / 2.138 | 3.413 / 2.933 |
| Bloques MESH compartidos / objetos que los usan | 1.497 / 9.692 | 1.810 / 10.588 |
| Bloques vacíos / apariciones vacías | 388 / 936 | 480 / 1.012 |
| Vértices únicos / expandidos por objeto | 1.011.864 / 3.118.098 | 1.309.590 / 3.570.430 |
| Triángulos únicos / expandidos por objeto | 713.486 / 2.138.266 | 925.840 / 2.467.116 |
| Determinantes mundiales negativos en MESH | 5.363 | 6.209 |
| Objetos con escala local no identidad, inventario previo | 486 | 588 |
| Modificadores / restricciones de objeto registrados | 0 / 0 | 0 / 0 |
| Dimensiones mundiales recalculadas, metros | 21,353697 × 16,300530 × 4,560298 | iguales |

Enterprise tiene además Camera y Light auxiliares fuera de `model.dae`: sus 12.453 objetos totales no son el número de objetos del puente. En Ascendant el inventario importado no contiene esa luz auxiliar.

Ambos XML declaran `inch`, `meter=0.0254`, `Z_UP`. Las escenas están en METRIC, `scale_length=1`, con coordenadas mundiales expresadas en metros. Sus cajas recalculadas coinciden: mínimo `(-10,676847; -8,150266; -0,680000)`, máximo `(10,676850; 8,150264; 3,880298)`. El centro de caja es aproximadamente `(0;0;1,600149)`. X separa las mitades; Y negativo es frente y Y positivo zona posterior, según identificaciones previas. **Bastó alineación identidad**, sin nuevas transformaciones.

Las mitades `Component_19` y `Component_19-001` tienen posiciones/cajas aproximadamente simétricas respecto a X=0, igual número de triángulos y correspondencia con las mitades homólogas del otro modelo. Las estaciones centrales Ascendant muestran cajas casi especulares, centradas en X≈±1,083. Esto acredita disposición bilateral; no se calculó una igualdad espejo exhaustiva de cada triángulo del puente.

Centroide ponderado por área triangular: Enterprise `(0,003992;0,314736;0,919833)` y Ascendant `(0,003051;0,314469;1,133908)`. **No es centro de masa**. El área sumada, 3.057,367634 frente a 3.375,795102 m², incluye duplicados/solapamientos: no es superficie pisable ni superficie arquitectónica única.

La conversión de unidades está comprobada. La escala anatómica y funcional aún requiere personaje real: declarar pulgadas no garantiza que cada asiento o puerta tenga dimensiones adecuadas. El GLB Ascendant presenta el problema documentado de factor ≈39,3701; se excluyó del ensayo homogéneo y no se corrigió durante esta fase.

## 4. Cuánto comparten y qué significa

Método: transformar en memoria los vértices de cada objeto mediante su matriz mundial; triangular según Blender; redondear cada coordenada a una cuadrícula; ordenar los tres vértices de cada triángulo y comparar multiconjuntos ordenados, conservando multiplicidad. Se utilizaron operaciones vectorizadas/intersección de claves, sin comparar cada triángulo con todos los demás.

| Cuantización | Ocurrencias comunes | Enterprise | Ascendant |
| --- | ---: | ---: | ---: |
| 0,1 mm | 2.065.576 | 96,6005% | 83,7243% |
| 0,5 mm | 2.065.580 | 96,6007% | 83,7245% |
| 1,0 mm | 2.065.624 | 96,6028% | 83,7263% |

En la prueba de 0,1 mm hay **1.033.654 claves espaciales distintas comunes**. Una clave igual implica una diferencia máxima de coordenadas euclídea de √3×0,1 mm≈0,1732 mm entre vértices correspondientes. No implica identidad binaria. El criterio ignora winding, normales, UV y materiales; el redondeo junto a límites de celda puede generar falsos negativos. No se acredita equivalencia de superficies retrianguladas mediante esta prueba.

Quedan 72.690 ocurrencias Enterprise y 401.540 Ascendant sin pareja de multiconjunto. En Ascendant, 6.972 de estas últimas son **multiplicidad adicional de claves ya presentes** en Enterprise: solamente 394.568 ocurrencias carecen de cualquier clave correspondiente. Ni unas ni otras equivalen automáticamente a volumen nuevo o a piezas físicas exclusivas.

Clasificación espacial de objetos con caras:

| Clase operativa | Enterprise | Ascendant |
| --- | ---: | ---: |
| Todas sus claves tienen correspondencia | 9.556 | 9.515 |
| Correspondencia parcial | 47 | 47 |
| Ninguna correspondencia triangular mundial acreditada | 182 | 1.617 |

La clase `EQUIVALENTE_TRIANGULOS_CUANTIZADOS` del CSV significa que todas las claves del objeto aparecen en el otro puente; **no** garantiza pareja uno a uno de objetos ni multiplicidad/materiales idénticos. La tercera clase tampoco prueba exclusividad de forma: una silla desplazada puede conservar su forma local y no coincidir mundialmente.

Las dos mitades arquitectónicas conservan ≈99,965% de ocurrencias con claves presentes en el otro modelo. La pantalla principal coincide íntegramente (160 triángulos). También coinciden íntegramente anclas de plataforma, bandas LCARS, borde perimetral, paneles de suelo y soportes inclinados. Ejemplos de correspondencia completa de multiconjunto a 0,1 mm:

| Enterprise → Ascendant | Triángulos por objeto | Identidad funcional |
| --- | ---: | --- |
| `ID1471` → `ID11615` | 160 | Pantalla principal confirmada en auditoría Enterprise |
| `ID13285/13295` → `ID20466/20474` | 126 / 150 | Superficies de plataforma, función probable |
| `ID19865/19875` → `ID25524/25532` | 126 / 150 | Contrapartes de plataforma, función probable |
| `ID14178/20751` → `ID21171/26220` | 224 | Contorno, confirmado/probable según mitad |
| `ID1836` → `ID11957` | 13.806 | Soporte inclinado confirmado previamente |
| `ID1651/1908` → `ID11772/12029` | 13.806 / 4.828 | Otras partes de soportes, función probable |
| `ID11576.001/18193.001` → `ID19075.001/24160.001` | 38 | Bandas posteriores, confirmado/probable |
| `ID13907/13917` → `ID20998/21008` | 976 / 484 | Marco/panel del cierre posterior confirmados previamente |
| `ID16806` → `ID23083` | 232 | Panel GLASS_FLOOR, función probable |

El techo conserva ≈99% de claves con correspondencia, pero suma 8.034 triángulos Enterprise frente a 15.080 Ascendant. Las anclas texturizadas `ID220/475` y `ID10364/10619` tienen el mismo conjunto espacial de claves con doble multiplicidad en Ascendant: no son automáticamente superficies más detalladas.

Una comprobación local de la silla delantera izquierda identifica **23 de sus 25 mallas con caras** con el mismo conjunto de triángulos locales en Ascendant, ignorando duplicados y winding, cuantización `1e-5` en unidades de datos MESH, **no metros mundiales**. Esas partes suman 12.496 de los 15.308 triángulos Enterprise. Cambian matrices/pose, materiales y multiplicidad; dos mallas quedan sin igualdad local acreditada. Por eso las sillas se clasifican como conjuntos modificados, con gran reutilización de forma, no como modelos enteramente exclusivos.

El sillón de capitán y los conjuntos centrales completos no tienen correspondencia triangular en su posición mundial actual. Son conjuntos distintos/modificados; no se ha demostrado exclusividad absoluta de todas sus subformas. Las consolas secundarias frontales Enterprise no tienen correspondencia en su emplazamiento analizado; identificar una eventual reutilización en otro lugar queda pendiente.

### Origen común e historia

La evidencia sostiene **una misma base arquitectónica compartida con modificaciones**, sin establecer quién la creó primero ni el árbol de versiones. Los metadatos públicos atribuyen ambos recursos a Cpt.Kirk / CaptainJamesKirk. Enterprise se publicó el 30-09-2025 y Ascendant el 06-06-2026, pero los DAE registran exportación Enterprise el 29-03-2024 (SketchUp 23.1.340) y Ascendant el 10-01-2020 (SketchUp 14.0.1). Fechas de publicación/exportación no equivalen a historia de autoría. Sería necesario testimonio del autor o archivos/versiones originales para resolver esa cronología. Fuentes: [API Enterprise](https://api.sketchfab.com/v3/models/a98a3da7570f433684f067c01298ad05), [API Ascendant](https://api.sketchfab.com/v3/models/5c882f022ccd45c285f76321af00da8f), XML locales y procedencia conservada.

## 5. Comparación de los catorce componentes

Los números son **MESH con caras / triángulos expandidos**, salvo indicación. La función confirmada procede de la auditoría Enterprise anterior, que sí registró revisión local de piezas; esta fase no añade afirmaciones visuales nuevas. Identidad geométrica y función operativa son evidencias diferentes.

| Componente | Enterprise | Ascendant | Edición, materiales y evidencia |
| --- | --- | --- | --- |
| 1. Suelo principal | Arquitectura integrada `ID13059/19639`, paneles y superficies a z≈−0,02 / 0,27 / 0,43 | Arquitectura integrada `ID20258/25316`; paneles `group_16/-001`: 17 / 2.018 por mitad | Cotas/obstáculos coincidentes; paneles GLASS_FLOOR y HONEYCOMB comunes. No hay un objeto único que sea exclusivamente todo el suelo. Separación funcional pendiente. |
| 2. Plataforma del capitán | z≈0,43; anclas `ID13285/13295/19865/19875` | Misma cota; anclas `ID20466/20474/25524/25532` | Geometría de estas anclas íntegramente equivalente; plataforma completa no identificada como módulo exclusivo. Materiales de estructura compartidos. |
| 3. Silla del capitán | `Captain_s_Chair_1`: 15 / 1.110; centro Y≈4,797 | `instance_193`: 125 / 72.280; centro Y≈3,913 | Enterprise confirmado; Ascendant candidato probable. 8 / 7 materiales de caras. Enterprise: 0 bloques con caras compartidos fuera; Ascendant: 76. Ninguno tiene operación de sentarse/levantarse acreditada. |
| 4. Consolas centrales | `Conn`: 38 / 6.336, doble cuerpo; con sus dos sillas: 88 / 36.952 | `group_1`: 1.492 / 321.408, incluye ambas estaciones/sillas; mitades `instance_9/80`, 651 / 152.112 cada una | Comparación incluyendo sillas evita atribuirles todo el sobrecoste a consolas. Enterprise 12 materiales en CONN, Ascendant 13 en conjunto completo. Ascendant separa padres de las dos estaciones; sus 262 bloques compartidos fuera exigen copias selectivas. |
| 5. Sillas delanteras | 25 / 15.308 cada una; 72 MESH incluyendo vacíos | 25 / 30.120 cada una; 72 MESH incluyendo vacíos | 5 materiales en ambos; 23/25 formas locales acreditadas comunes. Bases E z≈0,140/0,141, A z≈0,270: A corrige colocación respecto al nivel central; cambiar pose no demuestra mejor ergonomía. Datos compartidos fuera: 25 E / 17 A, con caras. |
| 6. Consolas laterales | Familias `Component_30`; curvas frontales `Console_2/.001`: 11 / 1.096 cada una | Familias perimetrales LCARS, dentro de las mitades arquitectónicas | Bandas LCARS/anclas comunes; consola completa funcional todavía no delimitada exhaustivamente. Curvas frontales E con 6 materiales y todos sus 11 bloques compartidos fuera; sin equivalencia acreditada en esa posición A. |
| 7. Consolas posteriores | Bandas `ID11576.001/18193.001`, 1 / 38 cada una | `ID19075.001/24160.001`, 1 / 38 cada una | Bandas geométricamente equivalentes, NewTrekLCARS común. Banda de pantalla no equivale a estación completa; proteger padres/asientos y datos compartidos. |
| 8. Pantallas | Principal `instance_8/ID1471`, 160 triángulos; displays laterales `Window_Display/.001` | Principal `instance_89/ID11615`, 160; otras bandas LCARS | Principal equivalente, textura VIEWSCREEN idéntica. Displays laterales E son conjuntos independientes de 3 MESH; equivalencia funcional A pendiente. UI dinámica y emisión no implementadas. |
| 9. Cerramientos perimetrales | Mitades `Component_19/-001`, 4.722 / 1.029.094 cada una, incluyen muebles | Mismos grupos, 4.702 / 1.029.094 cada una, incluyen muebles | ≈99,965% de claves comunes. E 18 materiales de caras por mitad, A 13. Una mitad no es una pared independiente; contiene suelo y puestos. 656 / 764 bloques con caras compartidos fuera, respectivamente. |
| 10. Columnas y soportes | Soportes inclinados identificados y otras familias integradas | Anclas equivalentes; `Component_27/-001`: 119 / 7.788 cada uno | Estos conjuntos A tienen 100% de claves presentes en E y 119 bloques compartidos fuera; 6 materiales. La función exacta de todos los soportes y cargas estructurales queda pendiente. No son una ventaja geométrica exclusiva A. |
| 11. Techo | `group_1`: 158 / 8.034; 222 MESH total | `group_11`: 157 / 15.080; 221 MESH total | Caja común z≈2,85..3,88; ≈99% de claves comunes, multiplicidad diferente. Ambos 6 materiales, 0 bloques con caras compartidos fuera del techo. Retirar temporalmente su visibilidad facilita inspección, no acredita una cubierta optimizada. |
| 12. Puertas y accesos | Huecos y arquitectura integrada; sin módulo operativo verificado | Arquitectura común; sin módulo operativo verificado | Identificación exhaustiva de hojas, jambas, pivotes y paso útil pendiente en ambos. No asumir puerta jugable a partir de un hueco. Materiales y número de subobjetos específicos pendientes. |
| 13. Iluminación arquitectónica | Geometría/materiales `WHITE_GLOW`, `GRATE_GLOW`, HONEYCOMB; 0 LIGHT en puente importado | Geometría/materiales correspondientes; 0 LIGHT | Texturas comunes y superficies coincidentes; emisión activa 0. No hay sistema de alarma/luces implementado. Delimitación completa y conteo de luminarias pendientes; un nombre GLOW no prueba iluminación. |
| 14. Zona posterior | Prisma de conexión: 18 objetos, 6.828 triángulos intersectados | Mismo prisma: 14 objetos, 6.828 triángulos intersectados | 100% de esos triángulos emparejados; cotas, cierre y desnivel equivalentes. Reparto en objetos distinto, arquitectura integrada en ambos. Mission Ops rectangular y mesa inexistentes como módulo implementado. |

Para IDs, cantidades y materiales por conjunto, usar el CSV de módulos y los mapas de diferencias; no sustituir identidades funcionales pendientes por nombres nuevos supuestos.

## 6. Modularidad útil y dependencias

En ambos DAE la jerarquía se expresa mediante padres y muchos nodos EMPTY; **no** equivale a un kit de paredes/suelos/puertas preparado para el juego. Los vacíos MESH proceden de geometrías fuente de líneas que el importador no convirtió a caras; varios preservan hijos/matrices. No eliminarlos en bloque.

Enterprise gana para las modificaciones inmediatas del capitán y CONN: 15 y 26 bloques con caras, respectivamente, sin usuarios fuera de cada conjunto. CONN continúa siendo una consola doble: separar sus dos cuerpos requeriría identificar/editar caras en una copia. Tapicería y reposabrazos del capitán no son automáticamente subpiezas mecánicas independientes.

Ascendant gana en separación jerárquica izquierda/derecha de estaciones centrales. Cada padre agrupa 774 MESH incluyendo vacíos; mover el grupo sería independiente de mover la otra estación, pero editar vértices no sería exclusivo: 363 bloques con caras de cada mitad se usan fuera. El conjunto completo usa 1.126 bloques con caras, 262 compartidos fuera. Más objetos seleccionables no implica menos trabajo funcional.

**No podemos eliminar una pared integrada por objeto completo con seguridad en ninguno.** `ID13059/19639` y los candidatos homólogos `ID20258/25316` incluyen grandes superficies de arquitectura/suelo. La huella mundial completa de estos objetos no es idéntica uno a uno; el volumen posterior sí coincide. El trabajo posterior debe separar las superficies necesarias, proteger el pavimento y conservar la parte exterior al recorte.

Procedimiento recomendado, aún sin ejecutar: duplicar el conjunto en una escena derivada versionada; registrar matrices y materiales; copiar `object.data` solamente cuando se necesite edición exclusiva; copiar materiales si el cambio afectaría otros usuarios; convertir correctamente entre coordenadas mundiales/locales; comprobar bordes, normales, continuidad y colisión después de separar. No hacer single-user indiscriminado: destruiría ventajas de instanciación y multiplicaría memoria sin necesidad.

## 7. Materiales, imágenes, UV y RobDev PBR

| Métrica homogénea | Enterprise | Ascendant |
| --- | ---: | ---: |
| Materiales cargados | 56 | 34 |
| Materiales usados por polígonos | **39** | **21** |
| Materiales de caras compartidos entre objetos | 35 | 20 |
| Imágenes FILE empaquetadas y referenciadas desde materiales usados | 20 | 9 |
| Bloques con caras y UV / sin UV | 1.350 / 788 | 152 / 2.781 |
| Apariciones con caras y UV | 5.526 | 714 |
| Objetos texturizados con caras sin UV | 0 | 0 |
| Imágenes necesarias ausentes | 0 | 0 |

**Corrección de definición:** los 55 materiales utilizados de Enterprise en la auditoría previa contaban referencias de slots, incluidas mallas de líneas/vacías o slots sin uso en caras. Los 39 actuales cuentan índices de material realmente presentes en polígonos. No se perdieron ni cambiaron materiales. Ascendant ya tenía documentada esta distinción. Las rutas externas relativas no resuelven junto a las escenas de análisis, pero los datos están empaquetados y sus SHA coinciden con las imágenes originales.

Hay **siete imágenes idénticas byte a byte** entre los dos DAE:

| Nombre | Resolución |
| --- | --- |
| `_58cd499217289.560ca8b44d983.jpg` | 1.024 × 646 |
| `Blinds_Roman_Hobbled_Blue.jpg` | 128 × 256 |
| `GRATE_GLOW.jpg` | 1.227 × 590 |
| `HONEYCOMB_GLOW_2.jpg` | 1.643 × 1.459 |
| `iso_web_yellow2.jpg` | 390 × 806 |
| `NewTrekLCARS.jpg` | 2.349 × 2.099 |
| `VIEWSCREEN_GLOW.jpg` | 1.073 × 208 |

Las otras 13 Enterprise son `__.jpg` 600×600, `Aluminum.jpg` 530×530, `material_28.png` 568×995, `material_3.jpg`, `material_3_0.jpg`, `material_3_1.jpg` 167×86 cada una, `material_4.jpg` 21×21, `material_43.jpg` 313×397, `material_44.jpg` 167×197, `material_46.jpg` 309×200, `material_48.jpg` 148×220, `material_54.jpg` 104×75 y `material_7.jpg` 300×438. Las otras dos Ascendant son `_0e3a929217289.560caa6605fe9.jpg` 1.024×623 y `Honeycomb_Grate.jpg` 1.425×1.420. Son metadatos y hashes, sin evaluación visual de calidad.

Se encontraron 18 pares de materiales con firma igual de valores Principled seleccionados, SHA de imágenes enlazadas, culling y modo de representación; hay relaciones uno a varios. Ejemplos: GLASS_FLOOR, LCARS, VIEWSCREEN, HONEYCOMB, GRATE y colores de estructura. **No** implica igualdad de todo el grafo shader, UV, apariencia ni identidad de material por nombre.

Todos los materiales usados de ambos tienen Metallic=0, Emission Strength=0 y Transmission Weight=0; Roughness=1 en los materiales usados. Las imágenes corresponden a acabado/color; no hay un conjunto de mapas normal/roughness/metallic/AO de producción. Los nombres GLOW no activan emisión. La existencia de UV no certifica densidad de texel, ausencia de solapamientos o aptitud para lightmaps; esta fase no analiza el contenido visual ni valida esos criterios.

La misma discrepancia **GLASS_FLOOR** existe en ambos DAE: E `ID6958`, A `ID15235`, 34 objetos de caras cada uno. El XML declara diffuse alpha≈0,2196078 y transparencia `RGB_ZERO`; la importación presenta Alpha=0, modo BLENDED. En Ascendant el GLB conserva alpha≈0,219608. Debe revisarse la interpretación antes de exportar; no es una ventaja diferencial de Ascendant. Enterprise también usa `ID20939`, llamado **Invisible** en el XML, Alpha=0 en 75 objetos: esa invisibilidad está declarada en la fuente y no se puede tratar como corrupción ni volver opaca indiscriminadamente. Las pruebas geométricas incluyen esas caras; la intención de colisión deberá decidirse por función.

RobDev PBR sigue siendo una especificación, no una biblioteca de producción ya aplicada. Enterprise ofrece más bloques con UV, pero sus materiales están más repartidos; Ascendant tiene menos materiales y mucho más acabado por color sin UV. En ambos conviene crear materiales maestros UE5 por propósito, conservar las interfaces aparte y decidir UV/triplanar por superficie. La silla E tiene 6/15 objetos con caras y UV; el candidato A, 23/125. Reemplazar acabados no evita comprobar usuarios compartidos, escalas del patrón y separación de caras. No se descargó ni aplicó PBR en esta fase.

## 8. Transitabilidad con condiciones idénticas

Se usó una cápsula matemática de **1,76 m de altura total y radio 0,34 m**: eje desde z del apoyo+0,34 hasta apoyo+1,42. Referencia humana nominal 1,80 m, sin crear figura nueva ni afirmar que la animación/postura está verificada. La altura de cápsula difiere 4 cm de esa referencia y se respetó el perfil de ensayo solicitado.

Para ambos: rayos descendentes desde z=0,60, alcance 1,50 m, pendiente de apoyo hasta 45°; distancia exacta segmento–triángulo con BVH; tolerancia de contacto de 1 mm; mismos puntos y recorridos, muestras separadas como máximo 2 cm. La búsqueda de candidatos utiliza siete esferas que cubren la cápsula. Se admiten como apoyo principal cotas ≥−0,12 m **solo para clasificar el ensayo**, no como aprobación funcional. Un rayo puede caer sobre mobiliario bajo: en medio de CONN Enterprise alcanza una superficie a z≈0,543, que no se acredita como suelo.

La clase `LIBRE_CONTINUO_PLANO` exige todas las cápsulas de muestra libres, apoyo dentro de la banda, variación de cota <1 mm y margen inferior de separación con superficies no de suelo >11 mm. Este margen cubre la interpolación horizontal entre muestras para superficies: supone continuidad del apoyo; no demuestra ausencia de microhuecos, ocupación de sólidos cerrados, contacto Chaos, respuesta a escalones ni NavMesh. No es simulación de CharacterMovement.

| Recorrido idéntico | Muestras libres E / A | Resultado |
| --- | ---: | --- |
| Frontal, `(0;−4,5)`→`(0;−0,6)` | 196/196 · 196/196 | Tramo plano libre en ambos, 3,90 m |
| Acceso central izquierdo | 234/330 · 234/330 | Transiciones/obstáculos; salto local de cota hasta 0,29 m |
| Acceso central derecho | 234/330 · 234/330 | Mismo problema |
| Tras CONN hacia capitán, `(0;2,3)`→`(0;3,8)` | **62/76 · 31/76** | Desnivel 0,16 m en ambos; la silla A añade ocupación al tramo |
| Lateral del capitán izquierdo | 122/122 · 122/122 | Tramo plano libre en ambos, 2,40 m |
| Lateral del capitán derecho | 122/122 · 122/122 | Tramo plano libre en ambos, 2,40 m |
| Conexión posterior, `(0;5,9)`→`(0;7,5)` | 46/81 · 46/81 | Cierre/caída de 1,11 m; no conexión jugable |
| Perímetro izquierdo | 511/511 · 511/511 | Tramo plano libre en ambos, ≈10,18 m |
| Perímetro derecho | 511/511 · 511/511 | Tramo plano libre en ambos, ≈10,18 m |

Se acreditan **los mismos cinco tramos planos**, no una red que conecte todos los niveles. El margen mínimo adicional perimetral es ≈12,17 mm: supera este ensayo pero deja poco margen para cambios de colisión o agente. Las coordenadas completas y obstáculos están en los JSON. No se mezclan directamente los porcentajes de ensayos previos diferentes.

Puntos diagnósticos comunes: frente z≈−0,02, altura vertical ≈3,61 m; entre soportes, ≈3,48 m; bajo soportes inclinados en X=±4,5,Y=−3, altura≈0,943 m y cápsula bloqueada; flancos centrales X=±2,45,Y=1,3 a z≈0,27, altura≈3,302 m; detrás del capitán en `(0;5,9)`, z≈0,43 y ≈2,611 m; perímetro X=±8,Y=0, ≈2,697 m. Estas alturas son rayos verticales al primer obstáculo, no la altura mínima de una habitación entera.

El punto entre consolas `(0;0,8)` está **bloqueado en ambos**. En A, desde apoyo z≈0,27, la primera superficie superior aparece a ≈0,782 m de altura; tener dos padres de consola no crea un pasillo central. En el fondo `(0;7,2)` hay una cápsula estática libre sobre z≈−0,68 con altura≈3,53 m, pero sin enlace aprobado al puente superior.

Cuadrícula común de 2.173 puntos, separación 0,40 m:

| Clase | Enterprise | Ascendant |
| --- | ---: | ---: |
| Sin apoyo | 460 | 460 |
| Apoyo inferior fuera de banda principal | 166 | 166 |
| Obstáculo/transición | 609 | 567 |
| Apoyo inclinado pendiente | 27 | 22 |
| Posición estática libre | 911 | 958 |

897 coordenadas XY son libres en ambos; 14 solo en E y 61 solo en A. La diferencia neta de 47 puntos favorece A en este muestreo estático, pero **no** equivale a 47 tramos, una superficie navegable adicional ni a una red conectada. Puede reflejar recolocación de mobiliario y rayos sobre superficies que no sean pavimento.

Conclusión operativa: no hay vencedor demostrado en navegación conectada. Los niveles y principales barreras son comunes; E tiene menos interferencia en el acceso central ensayado al capitán. Sentarse, levantarse, girar, dos NPC cruzándose y acceder a estaciones requieren ensayos adicionales con colisiones/animación reales. Una sola cápsula libre no demuestra convivencia de agentes; dos diámetros suman 1,36 m antes de márgenes.

## 9. Mission Ops y propuesta de escalinata

El diseño vigente exige una ampliación rectangular posterior con estaciones y gran mesa holográfica. Sigue siendo **obra nueva pendiente** en ambos puentes. La escalinata es una idea del autor **sin aprobación definitiva** y no se ha construido.

Condiciones medidas idénticas:

- Plataforma del capitán z≈0,43; fondo posterior z≈−0,68: descenso **1,11 m**.
- Cierre interior en X alrededor de Y≈6,46..6,53 y contorno exterior central hacia Y≈8,15026. Profundidad interna entre ambos límites ≈**1,69031 m**; no es una sala rectangular libre.
- Prisma diagnóstico X=±1,50, Y=6,40..8,30, Z=0,43..2,63: 6.828 triángulos por puente, 27,305539 m² de área recortada incluyendo duplicados; **todos los triángulos intersectados se emparejan a 0,1 mm**, 3.414 claves distintas. Esta comprobación acredita equivalencia geométrica del obstáculo, no solo igualdad de área.
- E intersecta 18 objetos y A 14 por distinto reparto de superficies. Se incluyen suelo de arranque, arquitectura integrada, marco/paneles y miembros superiores a z≈2,475. El conteo no es una lista de objetos autorizados a eliminar.

E: arquitectura `ID13059/19639`, arranque `ID13069/19649`, familia `ID13907..13972` y contrapartes `ID20485..20545`. A: arquitectura `ID20258/25316`, arranque `ID20266/25324`, familia `ID20998/21008/21018/21033/21043` y `ID26054/26062/26072/26082/26092`. Los mapas detallan su caja/uso; el prismado no permite eliminar la parte exterior del objeto.

Distancia Y entre el extremo posterior de la caja del sillón y la cara interior Y≈6,45995: E **1,15181 m**, A **2,11042 m**, ventaja A≈0,95861 m. Es una distancia de cajas, no una anchura de paso certificada. A desplaza el centro del sillón ≈0,884 m hacia delante y cambia su tamaño; no alarga el fondo entre los cierres ni elimina la caída. Ambos tienen espacio geométrico para estudiar un descansillo superior, sujeto a circulación/levantarse.

Ensayos algebraicos de escalera recta, **sin aprobación ergonómica ni normativa**: huella de prueba 0,28 m, descansillos de prueba 0,68 m cada uno. Este valor de descansillo únicamente permite comparar con el diámetro de cápsula; no es una dimensión de producción recomendada para personas/NPC.

| Contrahuellas | Altura cada una | Desarrollo horizontal, n−1 huellas | Con dos descansillos | Pendiente de la envolvente |
| --- | ---: | ---: | ---: | ---: |
| 6 | 0,185 m | 1,40 m | 2,76 m | 38,41° |
| 7 | 0,15857 m | 1,68 m | 3,04 m | 33,45° |
| 8 | 0,13875 m | 1,96 m | 3,32 m | 29,52° |

La variante de siete contrahuellas cabe casi exactamente **solo como tramo** entre Y≈6,46 y 8,15; deja ≈1 cm, insuficiente para su descansillo inferior dentro de ese intervalo. Incluso reutilizando el descansillo superior en la plataforma existente, tramo+descansillo inferior de prueba necesita 2,36 m frente a 1,69 m. Por tanto, esa variante debe extender el descansillo inferior a Mission Ops más allá del contorno actual, o estudiar otro arranque/recorrido con intervención en la plataforma. No hay una imposibilidad general de hacer escaleras: hay insuficiencia de ese intervalo para ese esquema concreto completo.

Es geométricamente razonable **estudiar** un acceso descendente integrado con la ampliación nueva, preservando el capitán y su circulación superior. Requiere separar el cierre interior, abrir selectivamente el contorno exterior, crear soporte y colisiones propios, revisar dintel/miembros superiores y conectar el nivel inferior a la sala nueva. No basta con retirar los paneles X. La rampa de colisión o los escalones discretos se decidirán al probar movimiento y navegación; la pendiente/contrahuella matemática no los certifica.

UE5 permite configurar `MaxStepHeight` y `WalkableFloorAngle`; sus valores efectivos, el agente NavMesh, su radio/altura y el manejo de bordes deben concordar. No se asumieron valores por defecto ni que una contrahuella de 0,159 m garantice paso. Referencia: [CharacterMovement de Epic](https://dev.epicgames.com/documentation/unreal-engine/API/Runtime/Engine/UCharacterMovementComponent).

**Balance Mission Ops:** empate en trabajo arquitectónico necesario; A aporta más distancia superior detrás del candidato a sillón, E aporta un capitán más simple/exclusivo y una selección posterior ya documentada. Ninguno acredita menos superficie obstructiva, menor caída ni una conexión lista. Mantener E evita una migración de base sin una mejora de conexión demostrada. Los perfiles completos están en ambos ensayos.

## 10. Vistas controladas y revisión humana

Se generaron exactamente **ocho PNG de 960×720**, cuatro pares: superior, general, central y posterior. Mismas cámaras ortográficas, posiciones/targets, escala por pareja, estudio Workbench, color gris común y parámetros de sombras/cavidad. Cubiertas E `group_1` y A `group_11` ocultas **solo en memoria**. Ningún cambio fue guardado; no se cambiaron materiales. El gris muestra geometría, incluidas caras cuyo material original es Invisible: **no es una comparación de acabado o transparencia original**.

Carpeta nueva: `output/capturas_revision/comparativa_enterprise_ascendant_v1/`, excluida de Git. [Galería humana local](../../output/capturas_revision/comparativa_enterprise_ascendant_v1/REVISION_HUMANA_LOCAL.html) y [manifiesto de cámaras/hashes](../../output/capturas_revision/comparativa_enterprise_ascendant_v1/MANIFIESTO_COMPARATIVA.json). Se verificaron contenedores PNG, dimensiones y SHA, **sin inspección visual por IA ni envío de imágenes/texturas de terceros a servicios externos**.

Revisión humana pendiente: confirmar la función de la silla y estaciones Ascendant; mirar cambios de pose en sillas; comprobar si los displays laterales están presentes; reconocer hojas de puertas y límites de grupos; revisar geometría posterior y miembros altos. La galería compara cada pareja lado a lado. Para revisar materiales originales, abrir las escenas existentes en Blender sin guardar sobre ellas; cualquier edición futura requiere una copia nueva. La calidad visual no recibe puntuación en esta auditoría.

## 11. Preparación para Unreal Engine 5

| Área | Comprobado hoy | Trabajo pendiente |
| --- | --- | --- |
| Escala/exportación | DAE en metros y coordenadas comunes | Conversión verificada a cm, pivotes/origen y hoja de exportación; prueba FBX/glTF según versión/importador real |
| Carga geométrica | A añade 328.850 triángulos expandidos, **15,38%** respecto a E | Agrupar módulos funcionales, conservar instancias útiles, elegir LOD/Nanite tras medir; sin estimaciones de FPS |
| Reflejos/normales | 5.363 / 6.209 MESH con determinante negativo | Verificar winding/normales tras exportar copia, culling de las superficies útiles y juntas |
| Topología única | E/A: 573/836 caras de área cero; 700.648/914.392 bordes límite por índices; 0/0 aristas con >2 caras; 0/40 pares con winding inconsistente | Los bordes de índices no equivalen a agujeros físicos por duplicación de vértices; limpieza dirigida, sin fusionar todo ni atribuir todos los bordes a defectos |
| Colisiones | Ensayos matemáticos sobre caras renderizadas | Colisiones por módulos, suelos continuos, puertas móviles y prueba con Character; no usar la apariencia transparente como criterio automático de colisión |
| Interactividad | Geometría seleccionable; anclas parciales | Actors/Blueprints, pivotes, UI dinámica, entradas/salidas de asientos, puertas y ocupación de puestos |
| Materiales | Imágenes originales empaquetadas; firmas parcialmente comunes | Resolver GLASS_FLOOR, conservar intención Invisible, UV/PBR, emisivos e instancias; no equivalencia automática de shaders Blender |
| NPC | Tramos geométricos libres y zonas obstruidas medidas | NavMesh conectado entre niveles, puertas, estaciones y futuro Mission Ops; paso simultáneo/evitación, entrada y salida de asientos |

En el repositorio no se encontraron `.uproject`, `.uasset` ni `.umap`; no hay implementación UE5 local acreditada aquí. Tampoco se acredita un pipeline ya aprobado de exportación/colisiones/interacción para estos dos modelos. Las reglas del contrato UE5 son requisitos, no funciones ejecutadas. No se importaron los dos puentes ni se abrió un proyecto UE5 durante esta fase.

Las unidades por defecto de longitud de UE son centímetros, según [Epic: unidades](https://dev.epicgames.com/documentation/unreal-engine/units-of-measurement-in-unreal-engine?lang=en-US). La elección de colisión simple/por polígonos debe comprobarse en el motor; no se infiere de que una malla sea triangular. [Epic: configuración de colisiones](https://dev.epicgames.com/documentation/en-us/unreal-engine/setting-up-collisions-with-static-meshes-in-unreal-engine). La navegación se genera a partir de la geometría de colisión y parámetros del agente: [Epic: navegación básica](https://dev.epicgames.com/documentation/en-us/unreal-engine/basic-navigation-in-unreal-engine). Se consultó documentación pública vigente; su versión mostrada no demuestra una versión UE instalada en el MSI.

## 12. Híbrido y derechos

**Viabilidad técnica del híbrido: sí; conveniencia actual: no acreditada.** Ambos comparten coordenadas métricas y arquitectura; sería posible transferir conjuntos completos a una copia nueva manteniendo matrices mundiales. No se hizo. El sillón A tiene distinta posición/tamaño y muchos datos compartidos; trasladarlo no mantiene automáticamente acceso/ergonomía. Sus centrales sí tienen dos padres independientes, pero incorporan 1.492 objetos con caras y 321.408 triángulos, frente a 88/36.952 de CONN E con sillas. No se ha medido una mejora de circulación que justifique ese intercambio.

Los soportes y grandes superficies comunes no aportan un beneficio por trasplantarlos. Una pieza aislada futura puede merecer evaluación cuando exista un requisito funcional claro; hoy añadiría remapeo de materiales/UV, usuarios de datos, colisiones y atribución sin mejora demostrada. La mayor cantidad de triángulos no prueba mayor calidad visual. No se recomienda C.

Los dos recursos declaran **CC BY 4.0** y autor Cpt.Kirk / CaptainJamesKirk en sus [metadatos Enterprise](https://api.sketchfab.com/v3/models/a98a3da7570f433684f067c01298ad05) y [Ascendant](https://api.sketchfab.com/v3/models/5c882f022ccd45c285f76321af00da8f). Las listas de tags públicas consultadas no incluyen NoAI. Esta consulta fue de metadatos; no se descargaron imágenes de los modelos. La adaptación/reutilización declarada exige atribución, enlace de licencia e indicación de cambios; la licencia no garantiza todos los derechos sobre texturas, marcas/interfaces o elementos de terceros. [Condiciones CC BY 4.0](https://creativecommons.org/licenses/by/4.0/).

Antes de distribuir el puente o un híbrido habrá que conservar fichas de procedencia de ambos recursos y resolver los derechos de elementos incorporados y del uso de Star Trek. Las referencias originales Theurgy siguen sujetas a las restricciones NoAI documentadas y a permisos de uso pendientes; no se usaron como entrada visual de IA. RobDev requiere licencias separadas de cada textura. No se publicó material de terceros.

## 13. Diferencias documentales, riesgos y decisión

El `PLAN.md` temprano describe un glTF/ZIP y 99 mallas/55 materiales/21 imágenes. El canon geométrico operativo de estas fases es la importación **DAE**, con jerarquía y 20 imágenes Enterprise; no son cifras intercambiables. El nombre heredado Kelvin no demuestra procedencia. La atribución de parecido a Theurgy en documentos tempranos tampoco constituye una comparación visual realizada en esta fase.

Se corrige aquí el significado de los 55 materiales usados Enterprise, sin reescribir la auditoría anterior. Se extiende el problema GLASS_FLOOR a ambos modelos, confirmado por XML. Las cinco rutas previas Enterprise se reprodujeron con condiciones comunes; el número superior de puntos estáticos libres Ascendant no demuestra una red superior. La propuesta antigua de suelo nivelado para Mission Ops permanece una opción documentada; la escalinata es una alternativa a estudiar, no reemplazo aprobado.

| Criterio prioritario | Balance basado en evidencia |
| --- | --- |
| Jugabilidad / red de navegación | Pendiente UE5; arquitectura y cinco tramos comunes; acceso central ensayado menos ocupado en E |
| Mission Ops | Mismo cierre/desnivel/intervención; A más distancia superior tras sillón; E menos complejidad del sillón y mapeo posterior previo |
| Modularidad útil | E capitán/CONN simples y exclusivos; A separación de padres centrales; suelo/paredes integrados en ambos |
| Calidad arquitectónica | Base común acreditada; ingeniería estructural y detalle funcional pendientes |
| Calidad visual | Pendiente revisión humana; sin puntuación |
| Materiales/PBR | Ambos básicos; E más UV, A menos materiales; transparencia común por resolver |
| Integración/optimización UE5 | E menor carga inicial y menor conjunto central; ninguno listo para importar como escenario final |
| Riesgos/derechos | Compartidos en gran parte; A más fragmentación y dependencias en conjuntos candidatos; licencias declaradas iguales |

**A es una recomendación técnica defendible para el siguiente prototipo**, no una certificación final ni una conclusión estética. B no mejora las barreras esenciales y aumenta el trabajo inmediato. C carece de beneficio funcional demostrado. D no es necesario para decidir la base de trabajo: las incertidumbres pendientes afectan a validación final de ambas opciones y se pueden probar empezando con E. No se han ejecutado cambios oficiales.

## 14. Orden de trabajo y primer ensayo UE5

1. Revisión humana local de los ocho diagnósticos y confirmación de puertas/estaciones/sillón Ascendant; conservar las atribuciones. Resolver la intención del vidrio y de las caras Invisible antes de convertir acabados o colisiones.
2. Tras aprobación de la base, preparar una **copia Enterprise nueva y versionada**: identificar un pequeño módulo con frente, transición de z≈−0,02 a 0,27 y plataforma z≈0,43. Delimitar suelo/paredes con datos independientes donde haga falta; mantener el maestro intacto. Preparar colisión, normales, matrices/pivotes y una exportación de prueba; no enviar todo el puente fragmentado como primer prototipo.
3. **Primer trabajo en UE5:** crear una escena de ensayo local del módulo elegido, con Character de radio **34 cm** y altura total **176 cm** (`CapsuleHalfHeight=88 cm`), referencia humana **180 cm**, material neutro y colisiones visibles. Verificar dimensiones importadas y recorrer ida/vuelta la transición de **29 cm** y el acceso a la plataforma de **16 cm**. Registrar perfil de movimiento, step height y pendiente; ensayar perfiles explícitos, por ejemplo 20 y 30 cm de escalón máximo, sin asumir que el segundo resuelve automáticamente la transición.
4. Generar NavMesh con el mismo agente y probar un NPC atravesando los enlaces, detenerse/salir de una estación, sentarse/levantarse y una puerta de prueba. Medir cruce jugador/NPC y márgenes; corregir colisiones/continuidad hasta que el recorrido sea estable. La lógica se construirá en UE5, no en `bpy`.
5. Estudiar en una copia/prototipo posterior los dos esquemas de Mission Ops —nivelado o descendente— con descansillos y sala nueva. Validar culling, dintel, suelo, movimiento y navegación; obtener aprobación del diseño antes de intervenir en arquitectura original.
6. Solo después ampliar el módulo jugable al puente completo y desarrollar el acabado RobDev, UI, iluminación y optimización medidas en el motor.

**Próximo paso concreto:** aprobar mantener Enterprise y preparar el módulo de prueba de dos transiciones de nivel con colisión verificable. Esta auditoría termina en la recomendación y evidencia; no ha construido el módulo, la escalera ni la ampliación.
