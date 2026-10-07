## EXP-002A — Caracterización global

Se analizaron las 320 observaciones válidas generadas durante
EXP-001.

### Resultados

| Métrica | Ojo derecho | Ojo izquierdo |
|---|---:|---:|
| Media | 0.492311 | 0.545867 |
| Mediana | 0.485998 | 0.537610 |
| Desviación estándar | 0.105112 | 0.110667 |
| Mínimo | 0.344282 | 0.388482 |
| Máximo | 0.700225 | 0.753422 |
| Rango | 0.355943 | 0.364940 |

La correlación de Pearson entre ambas señales fue de 0.9979.

### Interpretación

Las series correspondientes a ambos ojos presentan una asociación
lineal positiva elevada durante la muestra analizada, consistente con
el movimiento horizontal conjugado observado visualmente.

Los rangos observados son similares entre ambos ojos, aunque existe un
desplazamiento basal entre sus posiciones normalizadas.

La desviación estándar global no se interpreta como ruido del sistema,
ya que el registro incluye movimientos oculares voluntarios de gran
amplitud.

### Conclusión

Los resultados justifican realizar una caracterización separada de
los periodos de fijación y desplazamiento antes de introducir técnicas
de filtrado o calibración.

## EXP-002B — Caracterización por periodos

Se dividió la muestra EXP-001-001 en cinco regiones de interés
correspondientes a periodos visualmente estables de la grabación.

### Resultados principales

| Periodo | Δ ojo derecho | Δ ojo izquierdo |
|---|---:|---:|
| Centro inicial | 0.000000 | 0.000000 |
| Izquierda | -0.130148 | -0.133855 |
| Centro intermedio | 0.014657 | 0.012784 |
| Derecha | 0.198966 | 0.210631 |
| Centro final | -0.017121 | -0.010923 |

Los desplazamientos de ambos ojos presentan dirección y magnitud
similares.

Las desviaciones estándar dentro de los periodos estables fueron
considerablemente menores que los desplazamientos observados entre
posiciones.

El retorno al centro no produjo exactamente el mismo valor que el
baseline inicial. Esta diferencia puede estar relacionada con
movimiento residual del sujeto, desplazamiento de cabeza, variabilidad
del seguimiento o una combinación de estos factores.

### Consideración metodológica

Los intervalos utilizados en este experimento fueron seleccionados de
manera exploratoria después de observar la señal.

Por tanto, los resultados sirven para caracterizar el prototipo, pero
en experimentos posteriores las posiciones y tiempos deberán definirse
mediante un protocolo controlado.

### Conclusión

La señal normalizada permite diferenciar cuantitativamente las
posiciones horizontal izquierda, centro y derecha en la muestra
evaluada.

Los resultados justifican analizar las señales respecto a su propio
baseline antes de combinar información de ambos ojos.

## EXP-002C — Comparación interocular respecto al baseline

Las señales de ambos ojos fueron transformadas respecto a su propia
mediana durante el periodo de centro inicial.

### Baselines

- Ojo derecho: 0.486764
- Ojo izquierdo: 0.536891

Para cada señal se calculó:

dx = x - baseline

De esta manera, la posición inicial de referencia quedó aproximadamente
centrada alrededor de cero para ambos ojos.

### Resultados

- Correlación de Pearson: 0.9979
- Diferencia absoluta media entre ojos: 0.007072
- RMSE interocular: 0.009552

### Observaciones

Después de eliminar el desplazamiento basal individual, las señales
correspondientes a ambos ojos presentan una evolución temporal muy
similar.

Los desplazamientos hacia la izquierda producen valores negativos y
los desplazamientos hacia la derecha producen valores positivos en
ambas señales.

La correlación se mantuvo respecto al análisis de las señales originales,
lo cual es consistente con que la sustracción de una constante modifica
el nivel basal pero no la relación lineal temporal entre las señales.

Se conserva una pequeña diferencia entre ambos ojos, especialmente en
algunas transiciones y durante el retorno final al centro.

### Interpretación

La diferencia absoluta media y el RMSE se utilizan únicamente como
medidas de concordancia entre las dos señales estimadas.

No representan error respecto a una posición ocular verdadera ni
precisión clínica, ya que todavía no se dispone de un valor de referencia
externo.

### Conclusión

El centrado mediante un baseline independiente para cada ojo permite
comparar las señales en una referencia común y reduce el efecto del
desplazamiento basal existente entre ambos ojos.

La representación basada en desplazamiento respecto al baseline se
considera adecuada para continuar con pruebas de repetibilidad.
