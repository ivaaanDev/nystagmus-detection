# EXP-002 — Caracterización de la señal horizontal

## Objetivo

Caracterizar cuantitativamente las series temporales horizontales
obtenidas durante EXP-001 antes de aplicar técnicas de filtrado,
calibración o corrección de artefactos.

## Preguntas experimentales

1. ¿Qué rango de valores presenta cada ojo?
2. ¿Qué variabilidad presenta la señal cruda?
3. ¿Las señales de ambos ojos evolucionan de forma relacionada?
4. ¿Existen diferencias importantes entre las escalas de ambos ojos?
5. ¿La señal contiene valores ausentes o no válidos?

## Entrada

Archivo:

`exp001_001_horizontal_tracking.csv`

Generado durante EXP-001 a partir de la muestra de control
EXP-001-001.

## Métricas iniciales

Para cada ojo:

- número de observaciones;
- media;
- mediana;
- desviación estándar;
- mínimo;
- máximo;
- rango.

Entre ambos ojos:

- correlación de Pearson.

## Alcance

Este experimento caracteriza la señal obtenida, pero no determina
todavía exactitud clínica, velocidad ocular ni presencia de nistagmo.

No se aplicará filtrado ni suavizado durante esta etapa.
