# Plan fase 4 — Empalme posterior reversible y prototipo jugable

2026-10-10. **Documento de propuesta; ninguna intervención de esta fase ejecutada.** Fuente: copia `theurgy_trabajo_v0_1.blend`, SHA-256 `a47bf96edd671bfbf6f68ccbadf8ee03938fd81e68df18ba3a41e65badefb093`. Geometría fuente ligada al SHA-256 del Enterprise original que consta en los informes fase 2/3.

## Resultado que debe producir la fase 4

Un **tramo de conexión comprobablemente recorrible** desde la plataforma del capitán hasta una pequeña superficie de ensayo fuera del núcleo, sin construir Mission Ops completa. Conservar sillón, suelo anterior y estaciones laterales; retirar/reemplazar solamente lo necesario en una nueva copia, con originales recuperables. Probar colisiones y locomoción en UE5 antes de diseñar puestos y mesa.

Las dimensiones **3,00 m de ancho, 2,20 m de altura y suelo z=0,43 m** son la propuesta de fase 3, no geometría aprobada en el motor. No existe aprobación para publicar modelos o texturas ni para hacer commit/push.

## Secuencia técnica

1. **Verificar y respaldar.** Comprobar hashes original/copia. Crear respaldo verificable de v0_1 y nueva copia con nombre/versionado inequívoco, por ejemplo `theurgy_trabajo_v0_2.blend`, sin sobrescribir ninguna. Registrar rama, Blender, fecha y manifiesto de entrada. Rechazar destinos existentes y cualquier ruta en assets.
2. **Validar el Character y la conversión antes de cerrar dimensiones.** Registrar versión concreta UE5, perfil real de cápsula, cámara, MaxStepHeight, WalkableFloorAngle y agente NavMesh. Importar referencias derivadas de 180 cm / 68×176 cm y una superficie mínima propia; medir en el motor para evitar doble ×100. No instalar herramientas ni crear un proyecto en ubicación no acordada por inferencia.
3. **Revisar y aprobar la selección de caras.** Cargar `fase3_rutas_v4/CANDIDATOS_POSTERIOR.json`. Seleccionar y aislar visualmente los 18 candidatos, verificando qué porciones forman suelo, X, contorno exterior y piezas superiores. Los 6.828 índices son intersecciones, **no una orden de borrado**. Separar triángulos cruzados en el límite, conservando fuera del volumen y las caras a z=0,43. Registrar antes/después y nueva correspondencia ENT→pieza derivada.
4. **Crear originales recuperables dentro de la copia.** Duplicar controladamente los objetos a intervenir; volver single-user sus datos cuando proceda. Archivar los originales en colección explícita de respaldo local; ocultarlos para la prueba en lugar de eliminarlos. No renombrar ni alterar la fuente Enterprise, ni trasladar padres amplios que arrastren sillas/monitores. Revisar reflejos de matrices mundiales antes de cortar.
5. **Abrir únicamente la conexión de ensayo.** Trabajar sobre duplicados de los 14 miembros del X y las porciones necesarias de ID13059/19639. Mantener capitán y suelo de arranque. Resolver cierre interior Y≈6,46..6,53 y contorno exterior Y≈8,15. Comprobar que jambas/dintel/piezas superiores no penetran el volumen X=±1,50, z=0,43..2,63. No eliminar las mitades arquitectónicas completas.
6. **Dar continuidad al suelo.** Crear un módulo propio de empalme aproximadamente X=±1,50, Y=6,46..8,30, cota de pisada z=0,43; longitud ≈1,84 m y área ≈5,52 m², ajustando juntas al corte real. Añadir una pequeña plataforma de ensayo exterior para llegada/retorno, con perímetro y caída protegidos en la prueba. La base posterior actual está 1,11 m más baja; no dejar un agujero ni usarla como conexión sin corregir.
7. **Preparar colisiones y exportación de prueba.** Suelo y contorno separados, hulls simples donde sea viable; no una envolvente convexa de media nave. Excluir helpers, respaldos y capas decorativas de la exportación. Validar normales/sidedness y dimensiones; registrar importador FBX/glTF, opciones y pivotes. No reemplazar materiales ni crear biblioteca PBR en este lote.
8. **Probar UE5 de ida y vuelta.** Character con cápsula ensayada, rutas laterales alrededor del capitán, empalme y regreso; comprobar caminar, girar, colisión con jambas, caída, contacto del suelo y cámara. Hacer prueba con NPC/NavMesh y dos agentes si se mantiene la intención de cruce. Registrar vídeos/capturas y parámetros. Volver a Blender para corregir causas, sin parchear escalas distintas en ambos programas.
9. **Guardar versión de intervención revisable.** Registrar piezas/caras afectadas, hashes, pruebas, riesgos pendientes y restauración de visibilidad de respaldos. Mantener v0_1 recuperable. Entregar propuesta concreta antes de cerrar geometría definitiva o ampliar toda la sala. Sin commit/push automático.

## Criterios de aceptación

| Prueba | Evidencia exigida |
| --- | --- |
| Original y activos preservados | SHA-256 original sin cambios y verificación del manifiesto de assets, sin modificaciones por la tarea |
| Capitán intacto | 15 mallas y materiales conservados; transformaciones mundiales iguales salvo cambio local expresamente acordado |
| Paso posterior efectivo | Ancho y alto **libres tras colisiones/remates** iguales a objetivo aceptado; no solo caja de helper |
| Continuidad | Ninguna caída de 1,11 m en la ruta; juntas del pavimento sin hueco visible ni bloqueo invisible |
| Piso y paredes | Character no atraviesa soporte ni laterales; pruebas de avance/retroceso y contacto en bordes |
| Accesos al capitán | Dos rutas laterales conservadas, salida del asiento/cámara sin bloqueo tras la unión |
| NPC / tráfico | NavMesh conectado entre núcleo y plataforma, radios/alturas coherentes; cruce ensayado si se exige |
| Reversibilidad | Originales locales recuperables, v0_1 intacta, manifiesto y correspondencias suficientes para restaurar |
| Escala | Figura 180 cm y cápsula 68×176 cm verificadas en UE5, sin doble conversión |

La fase 4 no se considerará completada con un render de Blender. Si todavía no hay proyecto UE5 o no se ha decidido su versión/perfil Character, puede prepararse la selección reversible en Blender, pero el resultado continuará **pendiente de validación jugable**.

## Decisiones pendientes que no bloquean esta auditoría

- Aceptación de la propuesta de paso 3×2,20 m y cota 0,43 para intervención futura.
- Perfil de Character/NPC/cámara y criterios reales de escalones. Los cambios +0,29 y +0,16 m del núcleo deben tener prueba independiente: un empalme posterior correcto no resuelve toda su navegación.
- Colisión de capas de suelo GLASS_FLOOR/HONEYCOMB y posición de sillas delanteras; no trasladarlas basándose en una única hipótesis de soporte.
- Dimensiones de la sala rectangular, estaciones y mesa Mission Ops: **fases posteriores** al empalme; mantener el eje de circulación libre.
- Uso posterior de referencias restringidas, materiales e interfaces y política de publicación/licencias.

Referencias de trabajo: [escala y transitabilidad](ESCALA_Y_TRANSITABILIDAD_ENTERPRISE.md), [mapa posterior](PREPARACION_MISSION_OPS.md), [contrato UE5](../uss-theurgy/UE5_ESCENARIO_JUGABLE.md) y [diseño maestro](../uss-theurgy/DISENO_MAESTRO.md).
