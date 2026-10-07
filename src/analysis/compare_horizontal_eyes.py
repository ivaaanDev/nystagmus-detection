from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


CSV_PATH = Path(
    "experiments/exp_001_tracking/outputs/"
    "exp001_001_horizontal_tracking.csv"
)

OUTPUT_CSV = Path(
    "experiments/exp_002_signal_characterization/outputs/"
    "exp002_003_baseline_centered_signal.csv"
)

OUTPUT_PLOT = Path(
    "experiments/exp_002_signal_characterization/outputs/"
    "exp002_003_baseline_centered_signal.png"
)


BASELINE_START = 0.5
BASELINE_END = 1.8


data = pd.read_csv(CSV_PATH)

valid_data = data[
    data["valid"] == 1
].copy()


baseline_data = valid_data[
    (valid_data["timestamp_s"] >= BASELINE_START)
    & (valid_data["timestamp_s"] <= BASELINE_END)
]


right_baseline = baseline_data[
    "right_x"
].median()

left_baseline = baseline_data[
    "left_x"
].median()


valid_data["right_dx"] = (
    valid_data["right_x"]
    - right_baseline
)

valid_data["left_dx"] = (
    valid_data["left_x"]
    - left_baseline
)


valid_data["interocular_difference"] = (
    valid_data["left_dx"]
    - valid_data["right_dx"]
)


correlation = valid_data[
    ["right_dx", "left_dx"]
].corr().loc[
    "right_dx",
    "left_dx",
]


mae = np.mean(
    np.abs(
        valid_data["interocular_difference"]
    )
)


rmse = np.sqrt(
    np.mean(
        valid_data[
            "interocular_difference"
        ] ** 2
    )
)


OUTPUT_CSV.parent.mkdir(
    parents=True,
    exist_ok=True,
)


valid_data.to_csv(
    OUTPUT_CSV,
    index=False,
)


plt.figure(
    figsize=(12, 6)
)


plt.plot(
    valid_data["timestamp_s"],
    valid_data["right_dx"],
    label="Ojo derecho",
)

plt.plot(
    valid_data["timestamp_s"],
    valid_data["left_dx"],
    label="Ojo izquierdo",
)


plt.axhline(
    0,
    linewidth=1,
    linestyle="--",
)


plt.xlabel(
    "Tiempo (s)"
)

plt.ylabel(
    "Desplazamiento horizontal relativo al baseline"
)

plt.title(
    "EXP-002C — Señales horizontales centradas en baseline"
)

plt.legend()

plt.grid(
    True,
    alpha=0.3,
)

plt.tight_layout()


plt.savefig(
    OUTPUT_PLOT,
    dpi=150,
)


plt.show()


print(
    f"Baseline derecho: {right_baseline:.6f}"
)

print(
    f"Baseline izquierdo: {left_baseline:.6f}"
)

print()

print(
    "Correlación de señales centradas: "
    f"{correlation:.4f}"
)

print(
    "Diferencia absoluta media entre ojos: "
    f"{mae:.6f}"
)

print(
    "RMSE entre ojos: "
    f"{rmse:.6f}"
)

print()

print(
    f"CSV guardado en: {OUTPUT_CSV}"
)

print(
    f"Gráfica guardada en: {OUTPUT_PLOT}"
)
