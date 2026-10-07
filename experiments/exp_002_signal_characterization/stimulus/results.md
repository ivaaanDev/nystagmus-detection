# Resultados STIM-001

## STIM-001A/B — Presentación inicial del estímulo

Se implementó una ventana en pantalla completa capaz de presentar
un objetivo visual siguiendo la secuencia:

Centro → Izquierda → Centro → Derecha → Centro.

Cada posición tuvo una duración programada de 2 segundos.

La ejecución visual del protocolo se completó correctamente.

---

## STIM-001C — Registro temporal

Se incorporó un reloj global utilizando `time.perf_counter()` y el
registro automático de los tiempos de ejecución.

### Resultados observados

| Objetivo | Inicio planeado | Inicio registrado | Fin registrado |
|---|---:|---:|---:|
| Centro | 0.000 s | 0.000 s | 2.001 s |
| Izquierda | 2.000 s | 2.002 s | 4.002 s |
| Centro | 4.000 s | 4.002 s | 6.003 s |
| Derecha | 6.000 s | 6.004 s | 8.001 s |
| Centro | 8.000 s | 8.003 s | 10.002 s |

Las desviaciones registradas por software fueron del orden de pocos
milisegundos.

Estos valores representan tiempos registrados por el software y no
constituyen una validación física de la actualización del monitor.

---

## STIM-001D — Cuenta regresiva y control de inicio

Se añadió:

- pantalla de espera;
- inicio mediante barra espaciadora;
- cuenta regresiva 3 → 2 → 1;
- inicio del protocolo después del countdown;
- cierre automático después de la secuencia.

La secuencia completa funcionó correctamente.

---

## STIM-001E — Integración inicial de cámara

Se integró la captura de cámara dentro del mismo proceso encargado de
presentar el estímulo.

### Configuración solicitada

- Cámara: `/dev/video1`
- Resolución: 640×360
- FPS solicitados: 30

### Configuración reportada

- Resolución: 640×360
- FPS reportados por OpenCV: 30.00

### Resultados

- Frames capturados: 146
- FPS calculados mediante timestamps: 14.51
- Duración aproximada: 10.06 s

La integración síncrona produjo retrasos aproximados de 50–60 ms en
las transiciones del estímulo.

### Verificación del dispositivo

Mediante V4L2 se verificó que `/dev/video1` admite:

- MJPG, 640×360, 30 FPS;
- YUYV, 640×360, 30 FPS.

La configuración activa durante la prueba fue:

- formato YUYV 4:2:2;
- resolución 640×360;
- 30 FPS reportados.

### Conclusión

La tasa observada de aproximadamente 14.51 FPS no parece corresponder
a una limitación declarada del dispositivo.

La implementación síncrona actual se considera la principal candidata
a producir la reducción de la tasa de captura y los retrasos del
estímulo.

La captura deberá desacoplarse del hilo principal antes de realizar
las cinco grabaciones formales.


## STIM-001F/G — Captura sincronizada con precalentamiento

Se modificó el sistema para mantener la cámara capturando frames antes
del inicio experimental, descartándolos durante la espera y la cuenta
regresiva.

La grabación comenzó únicamente al establecer el tiempo de referencia
del protocolo.

### Configuración

- Cámara: `/dev/video1`
- Formato: MJPG
- Resolución: 640x360
- FPS reportados: 30.00

### Resultados

- Frames capturados: 299
- FPS calculados mediante timestamps: 29.92
- Primer frame: 0.015445 s
- Último frame: 9.975783 s

Tiempos del estímulo:

| Objetivo | Planeado | Inicio registrado | Fin registrado |
|---|---:|---:|---:|
| Centro | 0.000 s | 0.008 s | 2.001 s |
| Izquierda | 2.000 s | 2.001 s | 4.005 s |
| Centro | 4.000 s | 4.007 s | 6.002 s |
| Derecha | 6.000 s | 6.003 s | 8.005 s |
| Centro | 8.000 s | 8.006 s | 10.004 s |

### Conclusión

El precalentamiento de la cámara eliminó prácticamente el retraso
inicial observado en STIM-001F.

La adquisición mantuvo aproximadamente 30 FPS y las transiciones del
estímulo presentaron desviaciones temporales del orden de pocos
milisegundos.

La herramienta se considera suficientemente estable para iniciar las
pruebas formales de repetibilidad.

Los tiempos corresponden al reloj de software y no constituyen una
medición física del instante exacto de actualización del monitor.
