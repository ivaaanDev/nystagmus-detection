from pathlib import Path

import pandas as pd


CSV_PATH = Path(
    "experiments/exp_001_tracking/outputs/"
    "exp001_001_horizontal_tracking.csv"
)

OUTPUT_PATH = Path(
    "experiments/exp_002_signal_characterization/outputs/"
    "exp002_001_global_statistics.csv"
)


data = pd.read_csv(CSV_PATH)


valid_data = data[data["valid"] == 1].copy()


right_stats = valid_data["right_x"].describe()
left_stats = valid_data["left_x"].describe()


right_range = (
    valid_data["right_x"].max()
    - valid_data["right_x"].min()
)

left_range = (
    valid_data["left_x"].max()
    - valid_data["left_x"].min()
)


correlation = valid_data[
    ["right_x", "left_x"]
].corr().loc["right_x", "left_x"]


statistics = pd.DataFrame(
    {
        "metric": [
            "count",
            "mean",
            "median",
            "std",
            "min",
            "max",
            "range",
        ],
        "right_eye": [
            right_stats["count"],
            right_stats["mean"],
            valid_data["right_x"].median(),
            right_stats["std"],
            right_stats["min"],
            right_stats["max"],
            right_range,
        ],
        "left_eye": [
            left_stats["count"],
            left_stats["mean"],
            valid_data["left_x"].median(),
            left_stats["std"],
            left_stats["min"],
            left_stats["max"],
            left_range,
        ],
    }
)


OUTPUT_PATH.parent.mkdir(
    parents=True,
    exist_ok=True,
)

statistics.to_csv(
    OUTPUT_PATH,
    index=False,
)


print("EXP-002A — Caracterización global")
print()

print(statistics.to_string(index=False))

print()

print(
    "Correlación entre ambos ojos: "
    f"{correlation:.4f}"
)

print()

print(
    f"Archivo guardado en: {OUTPUT_PATH}"
)
