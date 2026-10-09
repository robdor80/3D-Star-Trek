# Fase 3 — Preparación de la conexión Mission Ops

2026-10-10 · MSI Windows · `feat/theurgy-escala-transitabilidad`. Copia preparada: `blender/principal/theurgy_trabajo_v0_1.blend`. La silla del capitán, el cerramiento X, su suelo y toda la arquitectura original siguen **sin edición geométrica ni traslado**.

## 1. Hallazgo decisivo

El cerramiento X no es la única barrera posterior. Detrás de él existe un fondo inferior a **z≈-0,68 m** y otro cierre arquitectónico hacia **Y≈8,15 m**. La plataforma del capitán está a **z≈0,43 m** y el perfil central cae **1,11 m** a partir de Y≈6,46. **Retirar dos paneles no produciría una conexión pisable al exterior del núcleo.** Hay que resolver cerramiento interior, soporte de suelo y salida a través del contorno exterior.

Mission Ops sigue siendo obra nueva: no se ha encontrado ni generado su sala rectangular, puestos o mesa holográfica. La banda curva de monitores del núcleo es un recurso existente que debe protegerse; no acredita que la ampliación ya exista.

## 2. Coordenadas y espacio real

| Referencia | Coordenadas / medidas mundiales en metros |
| --- | --- |
| Frente de puente | −Y; fondo +Y; Z vertical |
| Silla capitán | X=-0,594624..0,613121; Y=4,286453..5,308144; Z=0,323806..1,772788 |
| Frente de marco X | Y≈6,45995 |
| Paneles triangulares | Y≈6,52995 |
| Distancia respaldo → frente X | ≈1,15181 m, medida entre envolventes reales |
| Suelo antes del X | z≈0,43, por perfil central y plataformas ID13069 / ID19649 |
| Apoyo detrás del X | z≈-0,68 en los perfiles X=0 y X=±1,20 |
| Contorno exterior posterior | Límite Y≈8,15026 a X≈0; curva, no una pared plana universal |
| Techo nominal posterior | z≈2,85; estructuras locales pueden variar; comprobar volumen después de separación |
| Punto de enlace propuesto | (0;6,53;0,43), como datum de la cara posterior del X |
| Arranque de suelo continuo propuesto | Y≈6,46, manteniendo cota z=0,43 y verificando junta con pavimento existente |

La cápsula cabe en XY=(0;5,90), altura libre axial ≈2,611 m. Las rutas desde X=±1,20, Y=4,70 hasta detrás del capitán están libres en el ensayo continuo. No abrir un corredor sobre el eje ocupado por la silla: se llega a la nueva conexión **rodeando el sillón**, que se conserva.

Los tres perfiles posteriores (X=0 y ±1,20; Y=5,40..8,40, muestras 0,025 m) muestran obstáculos cerca de Y=6,46..6,85 y un tramo inferior que admite posiciones estáticas de cápsula. Este tramo **no se clasifica como una extensión jugable actual**, por discontinuidad de suelo y cierres. Datos: [MEDICIONES_FASE3.json](fase3_rutas_v4/MEDICIONES_FASE3.json).

## 3. Huella de conexión propuesta, todavía sin construir

**Propuesta de ensayo:** apertura centrada X=0, ancho libre **3,00 m** (X=-1,50..1,50), altura libre **2,20 m** (Z=0,43..2,63). Volumen de revisión **Y=6,40..8,30**, profundidad 1,90 m, que incluye margen anterior y salida más allá del límite actual. El helper `VOLUMEN_CONEXION_PROPUESTO_NO_ABIERTO` marca ese prisma, no modifica el puente.

El suelo nuevo de empalme empezaría aproximadamente en Y=6,46 y llegaría a Y=8,30: **3,00 × 1,84 m**, ≈5,52 m², antes de prolongarlo a la sala nueva. No superponer pavimento opaco sobre suelo aprobado en Y=6,40..6,46; resolver una junta y el borde real tras inspección de caras. El prisma de diagnóstico tiene 5,70 m² de planta porque añade ese margen de inspección.

Justificación: dos cápsulas de diámetro 0,68 ocupan 1,36 m y quedarían 1,64 m de reserva transversal total dentro de 3 m; no es validación de tráfico, NPC o estaciones. Los 2,20 m de altura dejan 0,44 m sobre cápsula y 0,40 m sobre figura humana. Entre z=2,63 y techo nominal z=2,85 quedan **0,22 m**, sin acreditar espacio para un dintel definitivo. La nueva abertura deberá conservar su ancho y alto útiles después de remates y colisiones.

La anchura coincide con una intervención central del X, cuyo marco triangular abarca más allá de X=±1,50. No implica eliminar la totalidad de los marcos triangulares. Las piezas superiores a z≈2,475 intersectan el volumen y también requieren revisión: no bastará actuar sobre los paneles bajos. La curva exterior podría requerir ensanchar el área de separación para sostener jambas y suelo; esto se decidirá en fase 4 sobre una copia y no se aprueba automáticamente.

**No se fijan en esta fase** ancho/fondo totales de la sala Mission Ops, número de puestos, dimensiones de mesa o distribución. El canon exige ampliación rectangular integrada detrás del capitán; sus medidas se resolverán tras validar el empalme y las referencias autorizadas. Las imágenes/modelos Theurgy con NoAI no se han pasado a visión/OCR/IA ni importado.

## 4. Mapa fino de candidatos

Se recortaron matemáticamente los triángulos por las seis caras del volumen propuesto. Se conservan objeto, ID ENT, ruta, malla compartida, **índices de polígonos originales**, área dentro del prisma, cajas recortadas y rol geométrico. La fuente exacta es el SHA-256 del original de fase 2.

Datos finales: [CANDIDATOS_POSTERIOR.json](fase3_rutas_v4/CANDIDATOS_POSTERIOR.json). Hay **18 objetos** con superficies intersectadas y **6.828 índices de polígonos distintos dentro de sus respectivos objetos**. Esos índices identifican caras que **tocan/intersectan** el volumen; no aseguran que toda la cara esté dentro. No son una selección de borrado aprobada ni deben reutilizarse después de cambiar topología.

| Candidato | Caras totales / intersectadas por objeto | Acción posterior propuesta |
| --- | ---: | --- |
| ID13059 / ID19639 | 7.580 / 1.418 cada uno | Arquitectura integrada. Separar/recortar únicamente superficies necesarias; jamás eliminar ambas mitades completas |
| ID13069 / ID19649 | 2.140 / 8 cada uno | Contacto horizontal a z=0,43. **CONSERVAR**, proteger como arranque del pavimento |
| ID13907 / ID20485 | 976 / 644 cada uno | Marcos triangulares. Copiar y estudiar recorte; porciones fuera de X=±1,50 quedan fuera de apertura |
| ID13917 / ID20495 | 484 / 484 cada uno | Paneles interiores. Todas sus caras intersectan el prisma, pero el objeto se extiende fuera de él: no autoriza eliminación completa |
| ID13927 / ID20505 | 248 / 248 cada uno | Miembros centrales inferiores; revisar separación y hueco útil |
| ID13937 / ID20515 | 236 / 120 cada uno | Miembros centrales superiores; conservar porciones por encima de abertura si son reutilizables |
| ID13952 / ID20525 | 122 / 122 cada uno | Paneles centrales inferiores; revisar en copia |
| ID13962 / ID20535 | 362 / 122 cada uno | Nuevos candidatos superiores respecto a fase 2; no ignorarlos |
| ID13972 / ID20545 | 734 / 248 cada uno | Piezas a z≈2,475..2,728; interfieren en parte con altura útil propuesta |

Entre las dos mallas grandes se intersectan superficies cerca del X y otras hacia el contorno exterior; el JSON de polígonos no separa por sí solo semánticamente **estructura, jambas, dintel o revestimiento**. Es una delimitación geométrica fina que reduce el ámbito a revisar, no un plano estructural terminado. No demuestra que esos elementos sean portantes en una nave real.

El cerramiento se denomina “azul en X” según contexto/documentación del usuario. Las capturas nuevas son grises: confirman su forma y ubicación, **no certifican su acabado azul ni PBR**.

## 5. Qué conservar y qué preparar para separación

Conservar íntegros `Captain_s_Chair_1` y sus 15 MESH; su tapicería conjunta `ID21637`, carcasa `ID21647`, reposabrazos integrados `ID21655` y pedestal `ID21628`. Ninguno de esos objetos figura en los 18 candidatos del prisma.

Conservar el pavimento anterior, las superficies de arranque z=0,43, los contornos `ID14178/ID20751` y las estaciones laterales/posteriores. Las bandas de monitores `ID11576.001/ID18193.001` no intersectan este prisma central, pero hay que proteger sus mallas compartidas y evitar trasladar sus padres con asientos incluidos. El no intersectar la propuesta central no garantiza que queden fuera de una sala Mission Ops más ancha futura.

Preparar copias de `ID13059/ID19639` y de los 14 miembros pequeños del X. Guardar explícitamente matrices mundiales, materiales y mapas de caras. Las dos mitades tienen reflexión diferente; una operación en coordenadas locales sin convertir el volumen mundial cortaría regiones equivocadas. Antes de editar verificar `data.users` y volver single-user las **copias** que lo necesiten. Las capas de materiales compartidas no se cambian en esta fase.

## 6. Riesgos y dependencias

1. **Suelo inexistente a la cota de conexión:** elevar una superficie inferior o simplemente quitar paredes no garantiza soporte; diseñar un módulo de empalme independiente y colisión propia.
2. **Cierres consecutivos:** comprobar paso a través del plano X y del contorno exterior, no solo visibilidad por un hueco central.
3. **Arquitectura integrada:** recortar porciones completas de triángulos que solo intersectan el prisma puede abrir agujeros laterales o perder suelo. Separación con revisión visual y comprobación de bordes obligatorias.
4. **Altura superior:** miembros ID13962/13972 y simétricos penetran parcialmente la altura de 2,20 m propuesta. Dintel, techo y remates deben quedar fuera del volumen libre.
5. **Capitán y circulación:** mantener rutas laterales; la mesa futura no puede ocupar el espacio de levantar/salir del asiento ni el prisma central de paso.
6. **UE5 y permisos:** dimensiones, colisiones, locomoción y NavMesh pendientes de ensayo; licencias y uso de referencias Theurgy deben resolverse antes de reutilizar/distribuir recursos restringidos. No reinterpretar permiso de referencia como licencia de importación de modelo/texturas.

Capturas: [referencias junto al capitán](../../output/capturas_revision/fase3_v1/capitan_escala_posterior.png) y [sección propuesta](../../output/capturas_revision/fase3_graficos_v2/seccion_posterior.png). La pared y el suelo originales continúan en la copia guardada. El procedimiento concreto está en [PLAN_FASE_4_INTERVENCION_POSTERIOR.md](PLAN_FASE_4_INTERVENCION_POSTERIOR.md).
