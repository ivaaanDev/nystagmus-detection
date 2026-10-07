from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd


CSV_PATH = Path(
    "experiments/exp_001_tracking/outputs/"
    "exp001_001_horizontal_tracking.csv"
)

OUTPUT_PATH = Path(
    "experiments/exp_001_tracking/outputs/"
    "exp001_001_horizontal_tracking.png"
)


data = pd.read_csv(CSV_PATH)


valid_data = data[data["valid"] == 1]


plt.figure(figsize=(12, 6))


plt.plot(
    valid_data["timestamp_s"],
    valid_data["right_x"],
    label="Ojo derecho",
)

plt.plot(
    valid_data["timestamp_s"],
    valid_data["left_x"],
    label="Ojo izquierdo",
)


plt.xlabel("Tiempo (s)")
plt.ylabel("Posición horizontal normalizada")

plt.title(
    "EXP-001-001 — Seguimiento horizontal ocular"
)

plt.legend()

plt.grid(
    True,
    alpha=0.3,
)


plt.tight_layout()


OUTPUT_PATH.parent.mkdir(
    parents=True,
    exist_ok=True,
)

plt.savefig(
    OUTPUT_PATH,
    dpi=150,
)

plt.show()


print(
    f"Gráfica guardada en: {OUTPUT_PATH}"
)
