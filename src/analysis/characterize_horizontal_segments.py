from pathlib import Path

import pandas as pd


CSV_PATH = Path(
    "experiments/exp_001_tracking/outputs/"
    "exp001_001_horizontal_tracking.csv"
)

OUTPUT_PATH = Path(
    "experiments/exp_002_signal_characterization/outputs/"
    "exp002_002_segment_statistics.csv"
)


SEGMENTS = {
    "center_initial": (0.5, 1.8),
    "left": (2.5, 3.8),
    "center_middle": (5.2, 6.4),
    "right": (7.4, 8.7),
    "center_final": (9.6, 11.2),
}


data = pd.read_csv(CSV_PATH)

valid_data = data[data["valid"] == 1].copy()


def calculate_statistics(values):
    return {
        "count": len(values),
        "mean": values.mean(),
        "median": values.median(),
        "std": values.std(),
        "min": values.min(),
        "max": values.max(),
        "range": values.max() - values.min(),
    }


rows = []


for segment_name, (start_s, end_s) in SEGMENTS.items():

    segment = valid_data[
        (valid_data["timestamp_s"] >= start_s)
        & (valid_data["timestamp_s"] <= end_s)
    ]

    right_stats = calculate_statistics(
        segment["right_x"]
    )

    left_stats = calculate_statistics(
        segment["left_x"]
    )

    rows.append(
        {
            "segment": segment_name,
            "start_s": start_s,
            "end_s": end_s,

            "right_count": right_stats["count"],
            "right_mean": right_stats["mean"],
            "right_median": right_stats["median"],
            "right_std": right_stats["std"],
            "right_min": right_stats["min"],
            "right_max": right_stats["max"],
            "right_range": right_stats["range"],

            "left_count": left_stats["count"],
            "left_mean": left_stats["mean"],
            "left_median": left_stats["median"],
            "left_std": left_stats["std"],
            "left_min": left_stats["min"],
            "left_max": left_stats["max"],
            "left_range": left_stats["range"],
        }
    )


statistics = pd.DataFrame(rows)


right_baseline = statistics.loc[
    statistics["segment"] == "center_initial",
    "right_median",
].iloc[0]

left_baseline = statistics.loc[
    statistics["segment"] == "center_initial",
    "left_median",
].iloc[0]


statistics["right_delta"] = (
    statistics["right_median"]
    - right_baseline
)

statistics["left_delta"] = (
    statistics["left_median"]
    - left_baseline
)


OUTPUT_PATH.parent.mkdir(
    parents=True,
    exist_ok=True,
)

statistics.to_csv(
    OUTPUT_PATH,
    index=False,
)


columns_to_print = [
    "segment",

    "right_median",
    "right_std",
    "right_delta",

    "left_median",
    "left_std",
    "left_delta",
]


print(
    "EXP-002B — Caracterización por periodos"
)

print()

print(
    statistics[
        columns_to_print
    ].to_string(index=False)
)


print()

print(
    "Baseline ojo derecho: "
    f"{right_baseline:.4f}"
)

print(
    "Baseline ojo izquierdo: "
    f"{left_baseline:.4f}"
)


print()

print(
    f"Archivo guardado en: {OUTPUT_PATH}"
)
