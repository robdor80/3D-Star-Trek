# Fase 3 — Escala y transitabilidad Enterprise / trabajo Theurgy

Fecha: 2026-10-10. Equipo MSI Windows. Rama exclusiva `feat/theurgy-escala-transitabilidad`, HEAD inicial `60e04b6`. Git limpio al comenzar. Blender **5.2.2 LTS**, ejecutable local verificado. Auditoría geométrica y preparación de copia; **sin prueba de juego en Unreal Engine**.

## 1. Resultado ejecutivo

La escala actual es **creíble como base de ensayo** y se conserva con factor global **1,000**. La conversión DAE pulgadas → metros ya estaba acreditada; esta fase aporta referencias humanas y medidas ergonómicas. La aprobación final sigue pendiente del Character real y una importación UE5.

Se creó `blender/principal/theurgy_trabajo_v0_1.blend`. Conserva geometría, UV, jerarquía, transformaciones, slots y shaders usados del Enterprise; añade solamente auxiliares. No se ha abierto ninguna pared ni construido Mission Ops. El capitán se conserva íntegro.

Cinco polilíneas planas tienen espacio geométrico continuo para la cápsula de ensayo: frente central, dos recorridos perimetrales y dos accesos laterales/posteriores al capitán. **No equivalen a un puente entero ya recorrible**: hay escalones, pasos bajo soportes bloqueados, puestos ocupados por muebles y una conexión trasera cerrada con caída de suelo de **1,11 m**.

## 2. Fuente, copia y seguridad

| Archivo / comprobación | Resultado |
| --- | --- |
| Original inmutable | `blender/principal/enterprise_importacion_inicial.blend`, 21.386.736 bytes |
| SHA-256 original antes y después | `0a55058552623995200fd5e16ddc327d5a6b2f6c54bbb9754f8340d01c885148` |
| Copia inicial | Copia de archivo verificada byte a byte antes de ejecutar bpy |
| Copia preparada | `blender/principal/theurgy_trabajo_v0_1.blend`, 21.399.605 bytes |
| SHA-256 copia preparada | `a47bf96edd671bfbf6f68ccbadf8ee03938fd81e68df18ba3a41e65badefb093` |
| Respaldo automático de Blender | `theurgy_trabajo_v0_1.blend1`, idéntico al original por SHA-256 |
| Contenido importado tras reabrir | 12.453 objetos originales; huella de matrices, padres, colecciones, vértices, loops, UV y slots idéntica |
| Materiales / imágenes | 55 shaders usados idénticos; 20 texturas empaquetadas con hashes idénticos a fase 2 |
| Única diferencia de datos huérfanos | El material predeterminado `Material`, con cero usuarios en el original, no persiste al guardar Blender. No se eliminó por script ni era un material usado del puente |
| Git | `.blend` / `.blend1` / capturas excluidos; sin staging, commit ni push |

No se editaron vértices, caras, materiales usados, padres, nombres ni transformaciones de objetos originales, tampoco en la copia. No se modificaron preferencias guardadas ni se instalaron herramientas. Todos los auxiliares llevan `fase3_auxiliar=True` y `exportar_UE5=False`.

Los **81 archivos de assets del inventario histórico** mantienen su contenido y ruta; se detectan **151 archivos actuales**, por lo que hay 70 adicionales respecto a aquella instantánea. La fase 3 no los ha creado ni auditado funcionalmente. La comprobación de cierre registra hashes de los 151, sin atribuir a esta fase la incorporación de los 70. No se escribió en assets ni se inspeccionaron imágenes Theurgy: sus restricciones NoAI siguen vigentes.

## 3. Método y límites

Datos principales: [mediciones de planta](fase3_bpy_v1/MEDICIONES_FASE3.json), [recorridos y ergonomía finales](fase3_rutas_v4/MEDICIONES_FASE3.json), [contraste de puestos](fase3_rutas_v4/ERGONOMIA_PUESTOS.json), [zonas clasificadas](fase3_rutas_v4/ZONAS_TRANSITABILIDAD.csv) y [verificación de integridad](VERIFICACION_FINAL_FASE3.json). El CSV de planta contiene 5.525 muestras. La referencia de objetos sigue siendo [MAPA_OBJETOS_ENTERPRISE.csv](MAPA_OBJETOS_ENTERPRISE.csv); no se sobrescribió.

- BVH mundial con **2.138.266 triángulos originales**, incluidas transformaciones y reflexiones heredadas. No se agregan las mallas auxiliares al cálculo.
- Distancia **segmento central de cápsula ↔ triángulo**: intersección interior, extremos contra triángulo y distancias a sus tres aristas. Siete consultas de proximidad cubren el segmento para reunir candidatos; la decisión se hace mediante distancia geométrica, no cajas de objetos.
- Cápsula vertical: radio **0,34 m**, altura total **1,76 m**, half-height **0,88 m**. Contacto admitido con tolerancia de **1 mm**. Se ensayaron analíticamente suelo tangente, cruce, pared, arista y recorte fuera del volumen.
- Planta a **0,25 m**; perfiles a 0,025–0,05 m; nueve polilíneas finales a intervalos **≤0,02 m**. En recorridos planos se separa el contacto de geometría completamente bajo los pies y se exige margen de obstáculos >0,011 m: cubre la distancia a la muestra más próxima y variación de cota <1 mm. Es una comprobación de **espacio continuo frente a superficies**, sin demostrar apoyo sobre posibles microhuecos del pavimento.
- Rayo de apoyo ordinario desde z=0,60 m, normal geométrica con pendiente absoluta ≤45°. Puede encontrar detalles bajos o la base inferior; no se declara pisable todo impacto. Para alturas de asientos se excluyen sillas y Conn y se incluyen módulos de pavimento, especialmente GLASS_FLOOR.
- Geometría considerada por ambas caras, sin interpretar volúmenes cerrados como sólidos. No reproduce sidedness, hulls, skin width, perching, escalado de cápsula ni sweeps de Chaos/CharacterMovement. Las pendientes no son validación de WalkableFloorAngle.
- No se simulan agacharse, saltar, subir escalones, animación de sentarse, cámara en tercera persona ni NavMesh. No se localizaron `.uproject`, `.uasset` o `.umap` en el repositorio, incluidos archivos ignorados. No se abrió UE5 ni se verificó su versión instalada.

Las cinco rutas aprobadas aquí tienen cota mínima z=-0,02 m. **“TRANSITABLE YA” significa libre en este ensayo geométrico**, pendiente de validación UE5. No es aprobación de colisiones ni del hito jugable del contrato técnico.

De 5.525 posiciones, 4.305 tienen apoyo según el rayo; 2.447 admiten la cápsula estática. De estas, **2.361** tienen apoyo z≥-0,12 m; otras 86 están sobre superficies inferiores que no se admiten automáticamente como pavimento. Hay 439 impactos por debajo de esa cota. Estas cifras cuentan muestras, no metros cuadrados, habitaciones ni porcentaje del puente listo para juego.

## 4. Escala, cotas y ergonomía

METRIC, METERS, `scale_length=1,0`; Z vertical; frente hacia −Y, fondo hacia +Y. Caja mundial del puente: **21,354 × 16,301 × 4,560 m**. Incluye base inferior y cubierta, no mide su espacio pisable. No se ha certificado babor/estribor.

| Elemento | Medición comprobada | Lectura para juego |
| --- | --- | --- |
| Capitán, caja del conjunto | 1,208 × 1,022 × 1,449 m; z=0,324..1,773 | Parte inferior penetra la cota del suelo; no confundir altura de caja con altura sobre pavimento |
| Asiento capitán, XY=(0;4,60) | Superficie z=0,942654; suelo z=0,430000; altura **0,512654 m** | Escala plausible de ensayo; postura/animación pendientes |
| Sillas CONN, cojines ID21442.001 / ID21442 | Superficie z≈0,6456 / 0,6458; pavimento z≈0,2700; altura **0,3756 / 0,3758 m** | Asientos bajos respecto al pavimento actual; revisar colocación y postura, sin reescalado global |
| Sillas CONN, conjunto | Cajas ≈0,676 × 0,680 × 1,092 m; bases mínimas z≈0,140 / 0,141 | Bases quedan ≈0,130 / 0,129 m bajo la superficie GLASS_FLOOR de ensayo |
| Consola doble Conn | Caja 4,080 × 2,067 × 1,132 m; altura máxima mundial z=1,027 | No son dos consolas independientes ni una altura única de uso |
| Superficie de mando en XY=(±1;0,50) | ID21014, z≈0,98673 | ≈1,007 m sobre el nivel delantero z=-0,02; ≈0,717 m sobre nivel posterior z=0,27. No sustituye medición de alcance sentado |
| Pavimento central delantero | z≈-0,02 | Nivel de referencia inferior de circulación |
| Nivel detrás de Conn | z≈0,27 | Desnivel +0,29 m respecto al anterior |
| Plataforma capitán / perímetro | z≈0,43 | Incremento +0,16 m; total +0,45 m desde el frente |
| Parte posterior tras X | Apoyo central z≈-0,68 | Caída de 1,11 m desde plataforma; no es continuidad útil a Mission Ops |

Las alturas delanteras se contrastaron con rayos entre superficies: GLASS_FLOOR `ID6957` / `ID16806` está a z≈0,27 y HONEYCOMB subyacente a z≈0,18. **Medir solo las seis mallas grandes de arquitectura daba falsamente el fondo z=-0,68 bajo esos asientos.** El análisis final v4 incluye esos paneles; las mediciones preliminares de arquitectura restringida quedan sustituidas. El contacto del asiento del capitán con suelo se toma del BVH mundial; una cadena de rayos scene.ray_cast exactamente sobre la unión X=0 no halló todos los contactos inferiores y no se usa para corregir esa cota.

Propuesta: mantener factor global 1,000 y revisar **localmente** las sillas delanteras. Si GLASS_FLOOR se adopta como soporte efectivo a z=0,27, elevar sus conjuntos ≈0,13 m colocaría sus bases sobre ese plano y dejaría el asiento ≈0,506 m sobre suelo. Es una hipótesis geométrica, **no una operación aplicada ni una altura ergonómica aprobada**; comprobar piernas, reposapiés, alcance de controles y animación antes de trasladarlas. Si cambia la colisión del suelo, recalcular esta propuesta. Un factor uniforme para elevar esos asientos también elevaría el del capitán y alteraría todos los pasos.

## 5. Pasos, alturas libres y giros

Las anchuras de rayos son secciones a cotas concretas; no son el mínimo de todo un túnel ni acreditan puertas. Se midieron cuatro niveles sobre suelo: 0,35 / 0,75 / 1,25 / 1,65 m. Se conserva cada impacto con objeto e índice de cara en el JSON.

| Lugar | Medida útil | Resultado |
| --- | --- | --- |
| Entre soportes, XY=(0;-3) | Menor sección X en cuatro niveles: **4,049 m**; altura axial libre **3,480 m** | Cápsula cabe; perfil lateral completo limita sus centros a X≈-1,575..1,575. Diferencia debida a obstáculos en otras cotas |
| Frente, XY=(0;-4) | Altura axial **3,610 m** | Ruta frontal de 3,90 m libre |
| Laterales junto a Conn, XY=(±2,45;1,30) | Cápsula libre sobre z≈0,27; altura axial ≈**3,302 m** | Puntos útiles; entrada a esa franja exige resolver transiciones, no declarar una ruta plana al frente |
| Franja secundaria a Y=1,30 | Centros libres a X≈-2,55..-2,40 y +2,325..+2,55; otras franjas a nivel inferior | Margen lateral pequeño y discontinuidad de suelo; reservar/revisar, no dimensionar una puerta sumando el diámetro a esas franjas |
| Accesos capitán, XY=(±1,20;4,70) | Cápsula libre; altura axial ≈**3,070 m** | Admiten giro vertical de la cápsula, simétrica; cuerpo animado y cámara no probados |
| Detrás del capitán, XY=(0;5,90) | Altura axial **2,611 m**; sección Y a +0,75 m **1,163 m** | Una cápsula cabe; reserva limitada detrás del respaldo |
| Soporte exterior izquierdo, XY=(-6,50;-3) | Altura axial **2,777 m** | Punto libre exterior al soporte |
| Bajo soporte, XY=(±4,50;-3) | Primer obstáculo superior a **0,943 m**; secciones X de 0,349 / 0,532 / 0,203 m a tres cotas | **No pasa** la cápsula erguida. Bloqueos de triángulos de la estructura; no simples problemas de textura |
| Entre brazos de silla CONN, z=0,75 | Sección X ≈**0,572 / 0,601 m** | Menor que 0,68 m; la posición sentada no sirve como corredor para cápsula erguida |
| Delante del respaldo CONN, z=0,90 | Sección Y ≈**0,713 / 0,704 m** | Muy justa en esa cota; no compensa el bloqueo entre brazos a menor altura |

En X=0, Y=4,70, el sillón bloquea el perfil; los centros de cápsula admitidos en el tramo ensayado X=-2..2 están en **[-2;-0,925] y [0,925;2] m**. A Y=5,90 todos los centros X=-2..2 ensayados están libres. No debe proponerse un acceso recto atravesando el sillón.

Distancia entre extremo posterior de la silla y frente del cerramiento X: **6,45995−5,30814≈1,15181 m**. Una cápsula de diámetro 0,68 deja aproximadamente 0,472 m de reserva longitudinal total; espacio suficiente para la ruta de ensayo individual, sin asegurar cruce de NPC, animación de levantarse o cámara orbital.

## 6. Clasificación espacial

| Zona | Clasificación solicitada | Evidencia / actuación |
| --- | --- | --- |
| Frente central, (0;-4,50) → (0;-2) → (0;-0,60) | **TRANSITABLE YA** | 196/196 posiciones libres; suelo plano z≈-0,02; margen de obstáculos ≥0,032 m |
| Perímetro izquierdo, (-8;-2) → (-8;2) → (-6;4) → (-3;5,50) | **TRANSITABLE YA** | 511/511, z≈0,43; longitud 10,183 m; margen mínimo ≈0,0122 m |
| Perímetro derecho, simétrico geométricamente | **TRANSITABLE YA** | 511/511, mismo nivel y longitud; no certifica todo el anillo |
| Rodear capitán por izquierda: (-1,20;4,70) → (-1,20;5,90) → (0;5,90) | **TRANSITABLE YA** | 122/122; 2,40 m; margen ≥0,032 m |
| Rodear capitán por derecha, X=+1,20 | **TRANSITABLE YA** | 122/122; mismos criterios |
| Accesos directos alrededor de Conn hacia capitán | **TRANSITABLE CON AJUSTES** | 234/330 muestras libres por lado; cambios de cota de 0,29 y 0,16 m. Probar step-up/colisiones o rutas/rampas; no borrar peldaños automáticamente |
| Detrás de Conn → frente del capitán, X=0 | **TRANSITABLE CON AJUSTES** | 62/76 libres; salto +0,16 m a Y≈2,88. La cápsula estática choca cerca de aristas; movimiento con step-up aún no probado |
| Pasos directos bajo estructuras inclinadas | **NO TRANSITABLE** | Altura/secciones incompatibles con cápsula erguida; rodear las estructuras |
| Posiciones ocupadas por sillones / cuerpos de consola | **NO TRANSITABLE** | Son obstáculos para caminar; su uso sentado requiere estado y colisión específicos |
| Cruce central del cerramiento X hacia el fondo | **NO TRANSITABLE** | 46/81 puntos libres, cierre entre ellos y caída -1,11 m; no hay ruta continua |
| Techo, bandas superiores, monitores y gráficos sin pisada | **SOLO DECORATIVA** | No reservarlos como navegación. Las estructuras portantes pueden seguir bloqueando cuando intersectan circulación |
| Puertas, identificación de hojas y volumen detrás del X | **REQUIERE REVISIÓN** | No hay puerta funcional validada; fondo inferior no equivale a futura sala transitable |
| Franjas estrechas de acceso a puestos y giro con NPC/cámara | **REQUIERE REVISIÓN** | Perfil disponible, pero falta recorrido y colisión real del actor |

Estas clases se aplican a las coordenadas y rutas descritas; no se asignan indiscriminadamente a zonas Theurgy cuyos límites físicos siguen pendientes. Cinco rutas libres aisladas **no garantizan conexión entre sus niveles**.

Reservar los recorridos planos medidos como walkable y preservar accesos laterales a los puestos. Para trazados nuevos, ensayar **1,60 m** en pasos donde se quiera cruce de dos cápsulas: 2×0,68 + 0,24 m de margen total. En secundarios individuales, **1,20 m** proporciona 0,52 m de margen total. Son propuestas de diseño de ensayo, no requisitos de UE5 ni normativa de accesibilidad.

## 7. Desniveles, pendientes, visión e interacciones

Las rutas directas registran salto de suelo -0,02→0,27 cerca de (±2,66;2,28), y 0,27→0,43 cerca de (±1,54;3,22) o (0;2,88). `ID2030` / `ID14887` son piezas bajas a z=0,06..0,10 que bloquean muestras próximas; pueden pertenecer a la transición, **no son candidatos de eliminación por ese dato**. Las plataformas `ID13069/19649/13079/19659` también aparecen como contactos de arista.

El mayor ángulo de apoyo aceptado en el grid es **43,182°**; incluye detalles y mobiliario, por lo que no prueba una rampa continua ni su orientación efectiva. La pendiente de las superficies altas de ID21014 cerca de XY=(±1;0,5) es aproximadamente 11,34°; es un tablero, no una rampa. Diseñar una rampa futura para salvar 0,29 m con 10° exigiría un desarrollo horizontal ≈1,645 m; para 0,16 m ≈0,907 m. Estos cálculos son **alternativas propuestas**, no rampas existentes ni geometría creada.

Seis líneas de visión de ensayo, desde ojos elegidos en (0;4,60;1,60), (-1;1,48;1,20) y (-1,20;4,70;2,03) hacia dos puntos del área frontal, no encuentran triángulos intermedios. Acreditan visibilidad por rayos concretos, no campo de visión, posición ocular definitiva ni cobertura total de la pantalla.

Cuatro empties de `DIAGNOSTICO` marcan hipótesis: asiento capitán (0;4,60;0,85), interacción Conn X negativa/positiva (±1;1,48;1,20), unión Mission Ops (0;6,53;0,43). **No cambian pivotes de objetos**, no implementan sentarse ni son actores UE5. La cota del marcador de asiento es una hipótesis inicial; la superficie medida es z≈0,943 y el anclaje de pelvis se debe recalibrar con animación. Los puntos de entrada/salida laterales útiles son (±1,20;4,70;0,43); comprobar la transición al asiento y no mantener una cápsula erguida dentro del mueble.

## 8. Copia organizada y capturas

Se añadieron **37 objetos auxiliares** y cinco colecciones: `REF_ESCALA`, `REF_TRANSITABILIDAD`, `ANALISIS_POSTERIOR`, `DIAGNOSTICO`, `CANDIDATOS_MISSION_OPS`. Hay una figura esquemática de cajas de **1,80 m** —sin anatomía ni rig— y una cápsula tessellada de dimensiones verificadas **0,68 × 0,68 × 1,76 m**. Se sitúan junto al capitán a X=±1,20, Y=4,70, con pies z≈0,43. La copia guardada tiene **12 marcadores de medida** de la primera corrida; los cinco puntos de sondeo añadidos después existen solo en el informe final. Incluye 18 marcadores de candidatos y cuatro de interacción, además de las dos referencias y el volumen de unión.

La jerarquía original conserva sus dos colecciones; no se vincularon originales a colecciones nuevas ni se ocultó el techo en el archivo guardado. Para inspección manual ocultar temporalmente `group_1`; hacerlo de nuevo visible al salir. El helper del volumen es wire y se dibuja delante en viewport, pero **no es una abertura**. Los auxiliares tienen `exportar_UE5=False` como metadato; un exportador genérico no lo respeta automáticamente: excluir sus colecciones y seleccionar solo módulos de producción.

Capturas verificadas, colores de diagnóstico sin PBR:

- [Capitán, referencias y cerramiento](../../output/capturas_revision/fase3_v1/capitan_escala_posterior.png): figura amarilla, cápsula cian y volumen naranja; pared conservada.
- [Planta local posterior](../../output/capturas_revision/fase3_v1/posterior_planta.png): parte del volumen está oculta por arquitectura, prueba del cerramiento conservado.
- [Planta numérica](../../output/capturas_revision/fase3_graficos_v2/planta_capsula.png): no interpreta imágenes de referencia; verde significa cápsula libre en muestra, azul las cinco rutas comprobadas.
- [Sección numérica posterior](../../output/capturas_revision/fase3_graficos_v2/seccion_posterior.png): muestra caída de suelo y empalme propuesto, sin malla nueva.

## 9. Consecuencias para Unreal Engine 5

Unreal usa centímetros por defecto; comprobar allí **180 cm** de referencia humana, diámetro de cápsula **68 cm**, altura **176 cm** y half-height **88 cm**, incluida su escala mundial. El half-height incluye hemisferios. Fuentes oficiales consultadas: [Unidades](https://dev.epicgames.com/documentation/en-us/unreal-engine/units-of-measurement-in-unreal-engine), [UCapsuleComponent](https://dev.epicgames.com/documentation/en-us/unreal-engine/API/Runtime/Engine/UCapsuleComponent/GetScaledCapsuleHalfHeight). La web mostraba documentación 5.8; esto **no identifica la versión instalada del proyecto**.

`MaxStepHeight` y `WalkableFloorAngle` son parámetros del CharacterMovement, no conclusiones del render. Registrar valores reales del Blueprint antes de adjudicar pasos; fuente [API oficial CharacterMovement](https://dev.epicgames.com/documentation/en-us/unreal-engine/API/Runtime/Engine/UCharacterMovementComponent). Propuesta de prueba: 20 cm / 45°, después comparar 30 cm para el salto de 29 cm. No se afirma ningún valor predeterminado ni se fija locomoción final. Coordinar Agent Radius/Height y desniveles de NavMesh con ese Character.

Preparar colisiones simples de suelo, paredes, cuerpos de estaciones y soportes; el suelo conserva capas finas y normales/reflexiones que este ensayo trató por ambas caras. Una colisión convexa de toda una mitad `ID13059` cerraría pasillos y huecos. Las sillas interactivas requieren entrada/salida y política de cápsula al sentarse. Excluir helpers, pantallas decorativas y capas luminosas de colisión cuando corresponda. Validar coste y sidedness en UE5, no exportar el BVH de esta auditoría como solución final.

Persisten 10.721 MESH, 2,138 M triángulos expandidos, 5.363 MESH con determinante mundial negativo y materiales compartidos. No se aplicaron transformaciones; preparar copias de exportación verificadas y evitar doble ×100. No se certifican draw calls, Nanite, UV lightmap, rendimiento, materiales PBR ni NPC por tener espacio geométrico.

## 10. Reproducción y prioridades

Scripts nuevos en `scripts/blender_python/`:

1. `medir_transitabilidad_enterprise.py`: BVH, grid, cápsulas, perfiles, rutas, medidas de puestos, caras posteriores; `--preparar-copia` solo admite copia idéntica al original y salida nueva. `--solo-rutas` mide sin guardar.
2. `medir_ergonomia_puestos.py`: cadenas de impactos y secciones en puestos, sin save.
3. `verificar_y_capturar_fase3.py`: reabre, verifica geometría/UV/transforms/shaders/texturas, pruebas analíticas y dos renders temporales.
4. `visualizar_mediciones_fase3.py`: gráficos desde JSON con Pillow del runtime preinstalado; no abre ninguna imagen de assets.

Ejemplo de nueva lectura, desde la raíz en PowerShell, cambiando salida por carpeta inexistente:

```powershell
& 'C:\Program Files\Blender Foundation\Blender 5.2\blender.exe' `
  --disable-autoexec --background 'blender/principal/theurgy_trabajo_v0_1.blend' `
  --python-exit-code 1 --python 'scripts/blender_python/medir_transitabilidad_enterprise.py' `
  -- --salida 'docs/auditorias/fase3_lectura_nueva' --solo-rutas
```

Para reproducir la preparación, **crear antes otra copia `theurgy_*.blend` byte a byte del original** y usar `--preparar-copia`, salida nueva y sin `--solo-rutas`. Nunca reutilizar la copia preparada ni el original como destino. La sintaxis y las ejecuciones se comprobaron. Los datos finales de rutas son **v4**; v2/v3 eran mediciones preliminares, no versiones del puente, y se conservan con hashes verificados en `temp/fase3_resultados_preliminares/`, excluido de Git. No regenerar encima de informes o mapas existentes.

Prioridad: (1) crear prototipo UE5 con conversión y Character registrados; (2) validar suelo por capas, escalones y accesos a puestos; (3) ejecutar intervención posterior reversible según [plan fase 4](PLAN_FASE_4_INTERVENCION_POSTERIOR.md); (4) fijar cotas y escala tras aceptación; (5) ampliar arquitectura Mission Ops y después puestos/mesa; (6) materiales y presentación. La preparación posterior detallada está en [PREPARACION_MISSION_OPS.md](PREPARACION_MISSION_OPS.md).
