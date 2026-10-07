# STIM-001 — Herramienta de estímulo horizontal controlado

## Objetivo

Desarrollar una herramienta experimental capaz de presentar un
estímulo visual horizontal bajo una secuencia temporal controlada y
registrar los tiempos de ejecución.

La herramienta será utilizada para mejorar la reproducibilidad de las
capturas realizadas durante EXP-002.

## Protocolo

Secuencia:

1. Centro — 2 s
2. Izquierda — 2 s
3. Centro — 2 s
4. Derecha — 2 s
5. Centro — 2 s

Duración experimental total: 10 s.

Antes del inicio se presenta:

- pantalla de espera;
- inicio mediante barra espaciadora;
- cuenta regresiva de 3 segundos.

## Posiciones normalizadas

- Izquierda: (0.25, 0.50)
- Centro: (0.50, 0.50)
- Derecha: (0.75, 0.50)

## Componentes

- `protocol.py`: definición del protocolo.
- `stimulus_runner.py`: presentación y control temporal.
- `recorder.py`: adquisición de video y timestamps.

## Salidas esperadas

Por repetición:

- video de cámara;
- timestamps de cada frame;
- log temporal del estímulo.

## Criterio de éxito

La herramienta deberá:

- ejecutar correctamente la secuencia;
- registrar los tiempos del estímulo;
- capturar el video;
- utilizar una referencia temporal común;
- minimizar la interferencia entre adquisición y presentación.
