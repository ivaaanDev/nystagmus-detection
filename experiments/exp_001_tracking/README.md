# EXP-001 — Seguimiento ocular base

## Objetivo

Evaluar la viabilidad de obtener la posición horizontal y vertical relativa del ojo cuadro a cuadro a partir de un video capturado con una cámara convencional.

## Pregunta experimental

¿Es posible obtener una trayectoria temporal estable del movimiento ocular mediante seguimiento visual del iris en un video convencional?

## Entrada

Video corto grabado bajo condiciones controladas:

* cámara fija;
* iluminación estable;
* rostro frontal;
* resolución conocida;
* tasa de cuadros conocida;
* movimientos oculares voluntarios horizontales y verticales.

## Procedimiento general

Procesar el video cuadro a cuadro, localizar la región ocular y estimar la posición relativa del iris.

Registrar para cada cuadro:

* número de frame;
* tiempo;
* posición horizontal;
* posición vertical;
* estado válido/no válido del seguimiento.

## Salidas

1. Archivo CSV con las coordenadas obtenidas.
2. Gráfica de posición horizontal respecto al tiempo.
3. Gráfica de posición vertical respecto al tiempo.
4. Porcentaje de cuadros en los que fue posible realizar el seguimiento.
5. Registro de errores y observaciones.

## Criterio inicial de éxito

La trayectoria obtenida debe corresponder visualmente con los movimientos oculares realizados durante la grabación y debe permitir distinguir cambios voluntarios hacia izquierda, derecha, arriba y abajo.

Este experimento no pretende todavía medir nistagmo, determinar velocidad ocular clínica ni realizar clasificación automática.

## Observaciones

Los resultados obtenidos servirán para identificar limitaciones del método de seguimiento y definir los experimentos posteriores de normalización, calibración y validación.
# EXP-001 — Seguimiento ocular base

## Objetivo

Evaluar la viabilidad de obtener la posición horizontal y vertical relativa del ojo cuadro a cuadro a partir de un video capturado con una cámara convencional.

## Pregunta experimental

¿Es posible obtener una trayectoria temporal estable del movimiento ocular mediante seguimiento visual del iris en un video convencional?

## Entrada

Video corto grabado bajo condiciones controladas:

* cámara fija;
* iluminación estable;
* rostro frontal;
* resolución conocida;
* tasa de cuadros conocida;
* movimientos oculares voluntarios horizontales y verticales.

## Procedimiento general

Procesar el video cuadro a cuadro, localizar la región ocular y estimar la posición relativa del iris.

Registrar para cada cuadro:

* número de frame;
* tiempo;
* posición horizontal;
* posición vertical;
* estado válido/no válido del seguimiento.

## Salidas

1. Archivo CSV con las coordenadas obtenidas.
2. Gráfica de posición horizontal respecto al tiempo.
3. Gráfica de posición vertical respecto al tiempo.
4. Porcentaje de cuadros en los que fue posible realizar el seguimiento.
5. Registro de errores y observaciones.

## Criterio inicial de éxito

La trayectoria obtenida debe corresponder visualmente con los movimientos oculares realizados durante la grabación y debe permitir distinguir cambios voluntarios hacia izquierda, derecha, arriba y abajo.

Este experimento no pretende todavía medir nistagmo, determinar velocidad ocular clínica ni realizar clasificación automática.

## Observaciones

Los resultados obtenidos servirán para identificar limitaciones del método de seguimiento y definir los experimentos posteriores de normalización, calibración y validación.
