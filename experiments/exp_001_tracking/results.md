# Resultados EXP-001

## EXP-001A — Lectura y previsualización del video

### Muestra

EXP-001-001 — control horizontal.

### Resultados técnicos

- Resolución: 640x360 px
- FPS reportados por OpenCV: 27.35
- Frames reportados: 320
- Frames decodificados: 320
- Duración estimada: 11.70 segundos
- Diferencia entre frames reportados y decodificados: 0

### Observaciones visuales

- El video se reproduce correctamente.
- El contador de frames aumenta correctamente.
- El tiempo mostrado aumenta durante la reproducción.
- El movimiento observado coincide con el movimiento realizado durante la captura.
- La región ocular es visualmente distinguible en la resolución utilizada.

### Conclusión

OpenCV pudo procesar completamente la muestra EXP-001-001 sin pérdida
de frames durante la decodificación.

La etapa de adquisición desde archivo se considera funcional para continuar
con las pruebas de localización de landmarks faciales y oculares.

Estos resultados no permiten todavía determinar la precisión del seguimiento
ocular ni la capacidad para detectar nistagmo.
