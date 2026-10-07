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

## EXP-001B.2 — Validación visual de landmarks

MediaPipe Face Landmarker detectó 478 landmarks sobre la muestra
EXP-001-001.

### Observaciones

- Los landmarks se encuentran visualmente alineados con el rostro.
- El contorno de ambos ojos se encuentra correctamente localizado.
- Se observan landmarks correspondientes a la región del iris.
- No se aprecia un desplazamiento global evidente de la malla facial.
- La resolución 640x360 permite distinguir visualmente la región ocular.

### Resultado

La localización facial se considera funcional para continuar con el
aislamiento y análisis de los landmarks correspondientes a los ojos e iris.

Esta evaluación es visual y no constituye todavía una medición de precisión
del seguimiento ocular.


## EXP-001C como validación visual inicial.
Salida de ocular_landmarks_preview.py

## EXP-001D.1 — Posición ocular normalizada en un frame

### Resultados

- Ojo derecho: 0.4713
- Ojo izquierdo: 0.5303

Ambos valores se encuentran próximos al centro geométrico del eje ocular.

Se identificó que la orientación de los puntos utilizados como extremos
del ojo no es consistente entre ambos ojos, provocando que las escalas
normalizadas tengan sentidos opuestos.

Antes de construir la serie temporal se decidió normalizar ambos ejes
en una misma dirección espacial.

## EXP-001D.2 — Validación de dirección horizontal

Se evaluó la posición horizontal normalizada en tres instantes
correspondientes a movimientos conocidos de la muestra EXP-001-001.

| Tiempo | Movimiento | Ojo derecho | Ojo izquierdo |
|-------:|------------|------------:|--------------:|
| 1.0 s | Centro     | 0.4765      | 0.5417        |
| 3.0 s | Izquierda  | 0.3706      | 0.4005        |
| 7.0 s | Derecha    | 0.6512      | 0.7171        |

### Observaciones

En ambos ojos, la posición normalizada disminuyó durante el
desplazamiento hacia la izquierda y aumentó durante el desplazamiento
hacia la derecha.

Las señales de ambos ojos presentan la misma orientación.

Se observó una diferencia entre los valores basales de ambos ojos,
por lo que las señales se conservarán inicialmente de manera
independiente y no se realizará todavía un promedio entre ellas.

### Conclusión

La coordenada horizontal normalizada utilizada responde de manera
coherente con los movimientos voluntarios realizados durante la
captura.

Este resultado valida inicialmente el método para continuar con la
generación de una serie temporal sobre el video completo.


## EXP-001D.3 — Seguimiento horizontal sobre el video completo

La muestra EXP-001-001 fue procesada utilizando MediaPipe Face
Landmarker en modo VIDEO.

### Resultados

- Frames procesados: 320
- Frames con coordenadas calculables: 320
- Frames sin coordenadas calculables: 0
- Disponibilidad inicial del seguimiento: 100.00 %

Se generó una serie temporal independiente para la posición horizontal
normalizada de ambos ojos.

### Consideración

El valor de 100 % representa únicamente la disponibilidad técnica de
coordenadas bajo el criterio actual de validez. No representa precisión
del seguimiento ni confiabilidad clínica.

La detección de parpadeos, artefactos y movimientos anómalos todavía no
forma parte de este criterio.


## EXP-001E — Serie temporal horizontal

Se generaron las series temporales correspondientes a la posición
horizontal normalizada de ambos ojos a partir de los 320 frames de la
muestra EXP-001-001.

### Observaciones

La gráfica permite distinguir visualmente las etapas del protocolo de
captura:

1. mirada aproximadamente centrada;
2. desplazamiento hacia la izquierda;
3. regreso al centro;
4. desplazamiento hacia la derecha;
5. regreso al centro.

Las señales correspondientes a ambos ojos presentan una evolución
temporal similar y responden en la misma dirección ante los movimientos
realizados.

Se observa un desplazamiento basal entre las señales de ambos ojos, por
lo que no se considera apropiado promediarlas directamente en esta
etapa.

También se observan pequeñas variaciones durante periodos de fijación y
en las transiciones entre posiciones.

### Conclusión

La posición horizontal normalizada calculada a partir de los landmarks
oculares permite recuperar cualitativamente el movimiento horizontal
realizado durante la captura.

El resultado valida inicialmente el pipeline de seguimiento horizontal,
pero todavía no determina su exactitud, precisión clínica ni
confiabilidad frente a artefactos.
