from pathlib import Path

import pandas as pd


BASE_EXPERIMENT_PATH = Path(
    "experiments/exp_002_signal_characterization"
)

SUBJECT_ID = "s001"

REPETITIONS = range(1, 6)


def align_repetition(repetition):
    repetition_text = (
        f"rep{repetition:02d}"
    )

    tracking_path = (
        BASE_EXPERIMENT_PATH
        / "outputs"
        / (
            f"exp002_{SUBJECT_ID}_"
            f"{repetition_text}_tracking.csv"
        )
    )

    stimulus_path = (
        BASE_EXPERIMENT_PATH
        / "stimulus_logs"
        / (
            f"exp002_{SUBJECT_ID}_"
            f"{repetition_text}_stimulus.csv"
        )
    )

    output_path = (
        BASE_EXPERIMENT_PATH
        / "outputs"
        / (
            f"exp002_{SUBJECT_ID}_"
            f"{repetition_text}_aligned.csv"
        )
    )


    print()
    print(
        f"Alineando {SUBJECT_ID.upper()} "
        f"- repetición {repetition}"
    )


    if not tracking_path.exists():
        raise FileNotFoundError(
            f"No existe: {tracking_path}"
        )


    if not stimulus_path.exists():
        raise FileNotFoundError(
            f"No existe: {stimulus_path}"
        )


    tracking = pd.read_csv(
        tracking_path
    )

    stimulus = pd.read_csv(
        stimulus_path
    )


    required_tracking = {
        "frame",
        "timestamp_s",
        "right_x",
        "left_x",
        "valid",
    }

    required_stimulus = {
        "event",
        "target",
        "actual_start_s",
        "actual_end_s",
        "x_norm",
        "y_norm",
    }


    missing_tracking = (
        required_tracking
        - set(tracking.columns)
    )

    missing_stimulus = (
        required_stimulus
        - set(stimulus.columns)
    )


    if missing_tracking:
        raise ValueError(
            "Faltan columnas en tracking: "
            f"{missing_tracking}"
        )


    if missing_stimulus:
        raise ValueError(
            "Faltan columnas en stimulus: "
            f"{missing_stimulus}"
        )


    stimulus = stimulus.sort_values(
        "actual_start_s"
    ).reset_index(drop=True)


    tracking["event"] = pd.NA
    tracking["target"] = pd.NA

    tracking["stimulus_x_norm"] = pd.NA
    tracking["stimulus_y_norm"] = pd.NA

    tracking["event_start_s"] = pd.NA
    tracking["event_end_s"] = pd.NA

    tracking["event_elapsed_s"] = pd.NA


    for index, stimulus_row in (
        stimulus.iterrows()
    ):
        event_start = float(
            stimulus_row[
                "actual_start_s"
            ]
        )


        # El final lógico del estímulo es
        # el inicio del siguiente evento.
        #
        # Para el último evento usamos
        # actual_end_s.
        if index < len(stimulus) - 1:
            event_end = float(
                stimulus.iloc[
                    index + 1
                ]["actual_start_s"]
            )

        else:
            event_end = float(
                stimulus_row[
                    "actual_end_s"
                ]
            )


        mask = (
            (
                tracking["timestamp_s"]
                >= event_start
            )
            &
            (
                tracking["timestamp_s"]
                < event_end
            )
        )


        tracking.loc[
            mask,
            "event",
        ] = int(
            stimulus_row["event"]
        )


        tracking.loc[
            mask,
            "target",
        ] = stimulus_row["target"]


        tracking.loc[
            mask,
            "stimulus_x_norm",
        ] = float(
            stimulus_row["x_norm"]
        )


        tracking.loc[
            mask,
            "stimulus_y_norm",
        ] = float(
            stimulus_row["y_norm"]
        )


        tracking.loc[
            mask,
            "event_start_s",
        ] = event_start


        tracking.loc[
            mask,
            "event_end_s",
        ] = event_end


        tracking.loc[
            mask,
            "event_elapsed_s",
        ] = (
            tracking.loc[
                mask,
                "timestamp_s"
            ]
            - event_start
        )


    total_frames = len(
        tracking
    )

    assigned_frames = int(
        tracking["target"]
        .notna()
        .sum()
    )

    unassigned_frames = (
        total_frames
        - assigned_frames
    )


    tracking.to_csv(
        output_path,
        index=False,
    )


    print(
        f"Frames totales: "
        f"{total_frames}"
    )

    print(
        f"Frames alineados: "
        f"{assigned_frames}"
    )

    print(
        f"Frames sin estímulo: "
        f"{unassigned_frames}"
    )


    print()
    print("Frames por evento:")


    event_counts = (
        tracking
        .dropna(
            subset=["event"]
        )
        .groupby(
            [
                "event",
                "target",
            ]
        )
        .size()
    )


    print(
        event_counts.to_string()
    )


    print()

    print(
        f"CSV guardado en: "
        f"{output_path}"
    )


    return {
        "repetition": repetition,
        "total_frames": total_frames,
        "assigned_frames": (
            assigned_frames
        ),
        "unassigned_frames": (
            unassigned_frames
        ),
    }


def main():
    summaries = []

    for repetition in REPETITIONS:
        summary = align_repetition(
            repetition
        )

        summaries.append(
            summary
        )


    summary = pd.DataFrame(
        summaries
    )


    summary_path = (
        BASE_EXPERIMENT_PATH
        / "outputs"
        / (
            f"exp002_{SUBJECT_ID}_"
            "alignment_summary.csv"
        )
    )


    summary.to_csv(
        summary_path,
        index=False,
    )


    print()
    print(
        "================================"
    )

    print(
        "EXP-002D — ALINEACIÓN COMPLETADA"
    )

    print(
        "================================"
    )

    print()

    print(
        summary.to_string(
            index=False
        )
    )

    print()

    print(
        "Resumen guardado en: "
        f"{summary_path}"
    )


if __name__ == "__main__":
    main()
