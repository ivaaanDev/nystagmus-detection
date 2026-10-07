from pathlib import Path

import numpy as np
import pandas as pd


BASE_EXPERIMENT_PATH = Path(
    "experiments/exp_002_signal_characterization"
)

SUBJECT_ID = "s001"

REPETITIONS = range(1, 6)


# Ventana estable dentro de cada evento.
STABLE_START_S = 0.5
STABLE_END_S = 1.8


EVENT_NAMES = {
    0: "center_initial",
    1: "left",
    2: "center_middle",
    3: "right",
    4: "center_final",
}


def calculate_event_statistics(
    data,
    repetition,
):
    stable = data[
        (data["event_elapsed_s"] >= STABLE_START_S)
        &
        (data["event_elapsed_s"] < STABLE_END_S)
        &
        (data["valid"] == 1)
    ].copy()

    rows = []

    for event_number, event_name in EVENT_NAMES.items():

        event_data = stable[
            stable["event"] == event_number
        ]

        if event_data.empty:
            raise ValueError(
                f"Repetición {repetition}: "
                f"no hay datos para evento "
                f"{event_number}."
            )

        rows.append(
            {
                "repetition": repetition,
                "event": event_number,
                "event_name": event_name,
                "target": (
                    event_data[
                        "target"
                    ].iloc[0]
                ),
                "frames": len(
                    event_data
                ),
                "right_median": (
                    event_data[
                        "right_x"
                    ].median()
                ),
                "right_mean": (
                    event_data[
                        "right_x"
                    ].mean()
                ),
                "right_std": (
                    event_data[
                        "right_x"
                    ].std()
                ),
                "left_median": (
                    event_data[
                        "left_x"
                    ].median()
                ),
                "left_mean": (
                    event_data[
                        "left_x"
                    ].mean()
                ),
                "left_std": (
                    event_data[
                        "left_x"
                    ].std()
                ),
            }
        )

    return pd.DataFrame(rows)


def calculate_repetition_metrics(
    event_stats,
    repetition,
):
    indexed = (
        event_stats
        .set_index("event_name")
    )

    baseline_right = float(
        indexed.loc[
            "center_initial",
            "right_median",
        ]
    )

    baseline_left = float(
        indexed.loc[
            "center_initial",
            "left_median",
        ]
    )


    def right_delta(event_name):
        return float(
            indexed.loc[
                event_name,
                "right_median",
            ]
            - baseline_right
        )


    def left_delta(event_name):
        return float(
            indexed.loc[
                event_name,
                "left_median",
            ]
            - baseline_left
        )


    left_right_eye = right_delta(
        "left"
    )

    left_left_eye = left_delta(
        "left"
    )

    right_right_eye = right_delta(
        "right"
    )

    right_left_eye = left_delta(
        "right"
    )

    center_middle_right = right_delta(
        "center_middle"
    )

    center_middle_left = left_delta(
        "center_middle"
    )

    center_final_right = right_delta(
        "center_final"
    )

    center_final_left = left_delta(
        "center_final"
    )


    return {
        "repetition": repetition,

        "baseline_right": (
            baseline_right
        ),

        "baseline_left": (
            baseline_left
        ),

        "left_delta_right_eye": (
            left_right_eye
        ),

        "left_delta_left_eye": (
            left_left_eye
        ),

        "right_delta_right_eye": (
            right_right_eye
        ),

        "right_delta_left_eye": (
            right_left_eye
        ),

        "center_middle_delta_right_eye": (
            center_middle_right
        ),

        "center_middle_delta_left_eye": (
            center_middle_left
        ),

        "center_final_delta_right_eye": (
            center_final_right
        ),

        "center_final_delta_left_eye": (
            center_final_left
        ),

        # Diferencia entre ambos ojos
        # después de quitar sus propios
        # baselines.
        "left_interocular_difference": (
            left_left_eye
            - left_right_eye
        ),

        "right_interocular_difference": (
            right_left_eye
            - right_right_eye
        ),
    }


def aggregate_metric(
    data,
    metric,
):
    values = data[
        metric
    ].astype(float)

    mean = values.mean()

    std = values.std(
        ddof=1
    )

    result = {
        "metric": metric,
        "mean": mean,
        "std": std,
        "min": values.min(),
        "max": values.max(),
        "range": (
            values.max()
            - values.min()
        ),
    }

    # CV sólo tiene sentido aquí
    # si la media no está cerca de 0.
    if abs(mean) > 1e-9:
        result["cv_percent"] = (
            std
            / abs(mean)
            * 100
        )
    else:
        result["cv_percent"] = np.nan

    return result


def main():
    all_event_stats = []
    repetition_metrics = []

    for repetition in REPETITIONS:

        repetition_text = (
            f"rep{repetition:02d}"
        )

        aligned_path = (
            BASE_EXPERIMENT_PATH
            / "outputs"
            / (
                f"exp002_{SUBJECT_ID}_"
                f"{repetition_text}_aligned.csv"
            )
        )

        if not aligned_path.exists():
            raise FileNotFoundError(
                f"No existe: "
                f"{aligned_path}"
            )

        data = pd.read_csv(
            aligned_path
        )

        print()
        print(
            f"Analizando "
            f"{SUBJECT_ID.upper()} "
            f"- repetición {repetition}"
        )

        event_stats = (
            calculate_event_statistics(
                data,
                repetition,
            )
        )

        all_event_stats.append(
            event_stats
        )

        metrics = (
            calculate_repetition_metrics(
                event_stats,
                repetition,
            )
        )

        repetition_metrics.append(
            metrics
        )


    event_stats_data = pd.concat(
        all_event_stats,
        ignore_index=True,
    )

    metrics_data = pd.DataFrame(
        repetition_metrics
    )


    output_directory = (
        BASE_EXPERIMENT_PATH
        / "outputs"
    )


    event_stats_path = (
        output_directory
        / (
            f"exp002_{SUBJECT_ID}_"
            "repeatability_events.csv"
        )
    )


    metrics_path = (
        output_directory
        / (
            f"exp002_{SUBJECT_ID}_"
            "repeatability_metrics.csv"
        )
    )


    event_stats_data.to_csv(
        event_stats_path,
        index=False,
    )


    metrics_data.to_csv(
        metrics_path,
        index=False,
    )


    metrics_to_aggregate = [
        "baseline_right",
        "baseline_left",

        "left_delta_right_eye",
        "left_delta_left_eye",

        "right_delta_right_eye",
        "right_delta_left_eye",

        "center_middle_delta_right_eye",
        "center_middle_delta_left_eye",

        "center_final_delta_right_eye",
        "center_final_delta_left_eye",

        "left_interocular_difference",
        "right_interocular_difference",
    ]


    aggregate_rows = [
        aggregate_metric(
            metrics_data,
            metric,
        )
        for metric
        in metrics_to_aggregate
    ]


    aggregate_data = pd.DataFrame(
        aggregate_rows
    )


    aggregate_path = (
        output_directory
        / (
            f"exp002_{SUBJECT_ID}_"
            "repeatability_summary.csv"
        )
    )


    aggregate_data.to_csv(
        aggregate_path,
        index=False,
    )


    print()
    print(
        "================================"
    )

    print(
        "EXP-002D-A — REPETIBILIDAD"
    )

    print(
        "================================"
    )

    print()

    print(
        "Ventana estable: "
        f"{STABLE_START_S:.1f}s "
        f"a {STABLE_END_S:.1f}s"
    )

    print()

    print(
        "Métricas por repetición:"
    )

    print()

    print(
        metrics_data.to_string(
            index=False
        )
    )


    print()
    print(
        "Resumen entre repeticiones:"
    )

    print()

    print(
        aggregate_data.to_string(
            index=False
        )
    )


    print()

    print(
        "Estadísticas por evento: "
        f"{event_stats_path}"
    )

    print(
        "Métricas por repetición: "
        f"{metrics_path}"
    )

    print(
        "Resumen de repetibilidad: "
        f"{aggregate_path}"
    )


if __name__ == "__main__":
    main()
