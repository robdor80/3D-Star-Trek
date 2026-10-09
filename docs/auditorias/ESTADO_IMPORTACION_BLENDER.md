# Estado de importación Blender — cierre fase 2

Fecha: 10 de octubre de 2026. MSI Windows. La auditoría inicial sigue siendo una instantánea histórica; este documento registra la nueva importación guardada por el usuario.

| Comprobación | Resultado / evidencia |
| --- | --- |
| Escena requerida existe | blender/principal/enterprise_importacion_inicial.blend, 21.386.736 bytes |
| Blender ejecutado | 5.2.2 LTS, hash d13f752e3b9c |
| Extensión local | Collada Support 1.2.2, manifiesto en perfil Windows de Blender 5.2 |
| Importación nueva ejecutada por Codex | Ninguna; se abrió el .blend guardado |
| Validación visual previa del usuario | Geometría/texturas visibles, piezas reconocibles, superposiciones ocultas; evidencia comunicada, no inspección de su ventana por Codex |
| Jerarquía importada | Colección model.dae y raíz EMPTY SketchUp; 12.451 objetos importados |
| Estructura | 10.721 MESH, 1.729 EMPTY y una cámara importada; no objeto único indivisible |
| Auxiliares de Scene | Camera y Light en Collection; no forman parte del puente importado |
| Unidades guardadas | METRIC / METERS / scale_length 1.0 |
| Conversión fuente | DAE pulgadas 0,0254 m; caja importada coincide con ese factor |
| Escala real jugable | Pendiente de calibración humana/cápsula UE5 |
| Texturas | 20 FILE empaquetadas, SHA-256 coincide con fuentes; ninguna necesaria ausente |
| Rutas externas | Las veinte //textures no resuelven; el empaquetado conserva los datos |
| Techo | Existe: group_1; se ocultó solo en proceso de render, sin guardar |
| Diferencias fuente/importación | MESH vacíos equivalentes a DAE solo líneas; 48 triángulos menos coinciden con degenerados de índice repetido/área cero |
| Modificadores / constraints | Ninguno en objetos actuales |
| Seguridad del original | SHA-256 inalterado antes/después de auditoría y renders |

La presencia del manifiesto verifica instalación de la extensión, no sus opciones exactas en la importación previa ni su estado en la UI actual. No se cambiaron preferencias ni se reinstaló el complemento. Cargar el .blend no requiere volver a importar DAE. Los parámetros elegidos por el usuario no constan en un registro reproducible; lo auditado es el resultado guardado.

SHA-256 fuente: `0a55058552623995200fd5e16ddc327d5a6b2f6c54bbb9754f8340d01c885148`.

## Reproducción de lectura

Desde la raíz del repositorio en PowerShell, elegir siempre una carpeta de salida nueva:

```powershell
& 'C:\Program Files\Blender Foundation\Blender 5.2\blender.exe' `
  --disable-autoexec --background `
  'C:\Users\andro\Documents\GitHub\3D Star Trek\blender\principal\enterprise_importacion_inicial.blend' `
  --python-exit-code 1 `
  --python 'C:\Users\andro\Documents\GitHub\3D Star Trek\scripts\blender_python\auditar_enterprise.py' `
  -- --salida 'C:\Users\andro\Documents\GitHub\3D Star Trek\docs\auditorias\enterprise_bpy_siguiente'
```

La carpeta enterprise_bpy_siguiente no debe existir; la salida incluye JSON completo y CSV técnico inicial. El script no guarda el .blend. Para contrastar con DAE usar contrastar_importacion_enterprise.py; para incorporar verificaciones funcionales usar generar_mapa_enterprise.py con IDENTIFICACIONES_ENTERPRISE.json y otra salida CSV, preservando notas anteriores.

## Diagnóstico visual

Con inspeccionar_enterprise.py, `--salida CARPETA_NUEVA` produce cuatro vistas. `--ocultar group_1` revela el interior solo durante el proceso. `--objetos Captain_s_Chair_1 Conn --aislar` muestra grupos individuales; selección por ID también admitida. Modos Workbench grises/cian, sin evaluación PBR. No se hace save, no se altera jerarquía ni geometría y se comprueba hash fuente antes/después.

Los manifiestos de las cuatro carpetas enterprise_* en output/capturas_revision registran visibilidad temporal, cámaras y fuente. No son nuevos maestros Blender.

## Estado de trabajo

Auditoría completada en la rama existente audit/inventario-inicial-3d. Sin commit ni push. La escena importada era un archivo local no versionado al iniciar esta fase y se preservó. Sigue pendiente la calibración funcional, el mapa de caras del cerramiento X y la validación en UE5. Los requisitos Theurgy/NoAI, conservación del capitán y Mission Ops de nueva construcción siguen vigentes.
