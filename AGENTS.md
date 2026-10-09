# Reglas permanentes para Codex

## Objetivo
Construir y documentar un puente de mando 3D explorable para el
videojuego Star Trek usando Blender y scripts Python reproducibles.
Enterprise Kelvin es el punto de partida 3D y USS Theurgy aporta
referencias visuales. No asumir medidas sin verificarlas.

## Seguridad de activos
- NUNCA modificar, renombrar, mover o borrar archivos de `assets/`.
- Trabajar siempre con copias o modelos derivados en `blender/`.
- Antes de operaciones destructivas, crear un respaldo verificable.
- No borrar escenas aprobadas ni sustituir `puente_master.blend` sin respaldo.
- No publicar ni subir a Git material de terceros sin autorizacion.

## Normas 3D
- Usar sistema metrico; registrar unidades y escala real comprobada.
- Mantener nombres descriptivos para objetos, colecciones y materiales.
- Separar consolas, asientos, arquitectura, iluminacion y elementos moviles.
- Usar `blender/principal/` para la escena maestra.
- Usar `blender/componentes/` para las piezas independientes.
- Mantener geometria editable y facilitar exportacion posterior al motor.
- Diseñar primero la operatividad de las consolas y despues su apariencia.

## Trabajo automatizado
- Guardar scripts Blender en `scripts/blender_python/`.
- Verificar que Blender esta instalado antes de invocarlo.
- Hacer scripts repetibles y evitar sobrescrituras por defecto.
- Documentar en `docs/` auditorias, decisiones y cambios relevantes.
- Exportar pruebas a `output/`, sin confundirlas con modelos maestros.
- No iniciar acciones Git destructivas sin autorizacion explicita.

## Primer trabajo
Inventariar los archivos que el usuario coloque en `assets/`.
Auditar formato, dimensiones, escala, mallas, materiales y texturas
antes de comenzar a modelar el puente definitivo.
