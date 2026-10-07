from pathlib import Path

import cv2
import mediapipe as mp
import numpy as np
import pandas as pd


MODEL_PATH = Path(
    "models/mediapipe/face_landmarker.task"
)

BASE_EXPERIMENT_PATH = Path(
    "experiments/exp_002_signal_characterization"
)

SUBJECT_ID = "s001"

REPETITIONS = range(1, 6)


RIGHT_IRIS = [468, 469, 470, 471, 472]
LEFT_IRIS = [473, 474, 475, 476, 477]

RIGHT_EYE_CORNERS = (33, 133)
LEFT_EYE_CORNERS = (362, 263)


def landmark_to_point(landmark):
    return np.array(
        [landmark.x, landmark.y],
        dtype=np.float64,
    )


def iris_center(landmarks, iris_indices):
    points = np.array(
        [
            landmark_to_point(
                landmarks[index]
            )
            for index in iris_indices
        ]
    )

    return points.mean(axis=0)


def normalized_position(
    iris,
    corner_1,
    corner_2,
):
    if corner_1[0] <= corner_2[0]:
        left_corner = corner_1
        right_corner = corner_2

    else:
        left_corner = corner_2
        right_corner = corner_1

    eye_axis = (
        right_corner
        - left_corner
    )

    eye_length_squared = np.dot(
        eye_axis,
        eye_axis,
    )

    if eye_length_squared == 0:
        return None

    iris_vector = (
        iris
        - left_corner
    )

    position = np.dot(
        iris_vector,
        eye_axis,
    ) / eye_length_squared

    return float(position)


def calculate_eye_positions(
    landmarks,
):
    right_iris = iris_center(
        landmarks,
        RIGHT_IRIS,
    )

    left_iris = iris_center(
        landmarks,
        LEFT_IRIS,
    )

    right_corner_1 = landmark_to_point(
        landmarks[
            RIGHT_EYE_CORNERS[0]
        ]
    )

    right_corner_2 = landmark_to_point(
        landmarks[
            RIGHT_EYE_CORNERS[1]
        ]
    )

    left_corner_1 = landmark_to_point(
        landmarks[
            LEFT_EYE_CORNERS[0]
        ]
    )

    left_corner_2 = landmark_to_point(
        landmarks[
            LEFT_EYE_CORNERS[1]
        ]
    )

    right_x = normalized_position(
        right_iris,
        right_corner_1,
        right_corner_2,
    )

    left_x = normalized_position(
        left_iris,
        left_corner_1,
        left_corner_2,
    )

    return right_x, left_x


BaseOptions = mp.tasks.BaseOptions

FaceLandmarker = (
    mp.tasks.vision.FaceLandmarker
)

FaceLandmarkerOptions = (
    mp.tasks.vision.FaceLandmarkerOptions
)

RunningMode = (
    mp.tasks.vision.RunningMode
)


def process_recording(repetition):
    repetition_text = (
        f"rep{repetition:02d}"
    )

    video_path = (
        BASE_EXPERIMENT_PATH
        / "recordings"
        / (
            f"exp002_{SUBJECT_ID}_"
            f"{repetition_text}_video.mp4"
        )
    )

    timestamps_path = (
        BASE_EXPERIMENT_PATH
        / "recordings"
        / (
            f"exp002_{SUBJECT_ID}_"
            f"{repetition_text}_frames.csv"
        )
    )

    output_path = (
        BASE_EXPERIMENT_PATH
        / "outputs"
        / (
            f"exp002_{SUBJECT_ID}_"
            f"{repetition_text}_tracking.csv"
        )
    )


    print()
    print(
        f"Procesando {SUBJECT_ID.upper()} "
        f"- repetición {repetition}"
    )

    print(
        f"Video: {video_path}"
    )


    if not video_path.exists():
        raise FileNotFoundError(
            f"No existe el video: "
            f"{video_path}"
        )


    if not timestamps_path.exists():
        raise FileNotFoundError(
            "No existe el archivo de "
            f"timestamps: {timestamps_path}"
        )


    timestamps_data = pd.read_csv(
        timestamps_path
    )


    required_columns = {
        "frame",
        "timestamp_s",
    }

    missing_columns = (
        required_columns
        - set(timestamps_data.columns)
    )

    if missing_columns:
        raise ValueError(
            "Faltan columnas en "
            f"{timestamps_path}: "
            f"{missing_columns}"
        )


    if timestamps_data.empty:
        raise ValueError(
            "El archivo de timestamps "
            "está vacío."
        )


    expected_frames = np.arange(
        len(timestamps_data)
    )

    csv_frames = (
        timestamps_data["frame"]
        .to_numpy()
    )

    if not np.array_equal(
        expected_frames,
        csv_frames,
    ):
        raise ValueError(
            "La numeración de frames del "
            "CSV no es consecutiva desde 0."
        )


    video = cv2.VideoCapture(
        str(video_path)
    )

    if not video.isOpened():
        raise ValueError(
            "No se pudo abrir el video: "
            f"{video_path}"
        )


    reported_fps = video.get(
        cv2.CAP_PROP_FPS
    )


    options = FaceLandmarkerOptions(
        base_options=BaseOptions(
            model_asset_path=str(
                MODEL_PATH
            )
        ),
        running_mode=RunningMode.VIDEO,
        num_faces=1,
    )


    rows = []

    frame_number = 0

    previous_timestamp_ms = -1


    with FaceLandmarker.create_from_options(
        options
    ) as landmarker:

        while True:
            success, frame = video.read()

            if not success:
                break


            if frame_number >= len(
                timestamps_data
            ):
                video.release()

                raise ValueError(
                    "El video contiene más "
                    "frames que frames.csv."
                )


            timestamp_s = float(
                timestamps_data.iloc[
                    frame_number
                ]["timestamp_s"]
            )


            # MediaPipe VIDEO necesita
            # timestamps monotónicos
            # expresados en milisegundos.
            timestamp_ms = int(
                round(
                    timestamp_s * 1000
                )
            )


            # Protección por si dos timestamps
            # distintos terminan redondeándose
            # al mismo milisegundo.
            if (
                timestamp_ms
                <= previous_timestamp_ms
            ):
                timestamp_ms = (
                    previous_timestamp_ms
                    + 1
                )


            previous_timestamp_ms = (
                timestamp_ms
            )


            frame_rgb = cv2.cvtColor(
                frame,
                cv2.COLOR_BGR2RGB,
            )


            mp_image = mp.Image(
                image_format=(
                    mp.ImageFormat.SRGB
                ),
                data=frame_rgb,
            )


            result = (
                landmarker.detect_for_video(
                    mp_image,
                    timestamp_ms,
                )
            )


            if result.face_landmarks:
                landmarks = (
                    result.face_landmarks[0]
                )

                (
                    right_x,
                    left_x,
                ) = calculate_eye_positions(
                    landmarks
                )

                valid = (
                    right_x is not None
                    and left_x is not None
                )

            else:
                right_x = None
                left_x = None
                valid = False


            rows.append(
                {
                    "frame": frame_number,
                    "timestamp_s": (
                        timestamp_s
                    ),
                    "right_x": right_x,
                    "left_x": left_x,
                    "valid": int(valid),
                }
            )


            frame_number += 1


    video.release()


    if frame_number != len(
        timestamps_data
    ):
        raise ValueError(
            "El número de frames del video "
            "no coincide con frames.csv. "
            f"Video: {frame_number}, "
            "timestamps: "
            f"{len(timestamps_data)}"
        )


    data = pd.DataFrame(
        rows
    )


    output_path.parent.mkdir(
        parents=True,
        exist_ok=True,
    )


    data.to_csv(
        output_path,
        index=False,
    )


    total_frames = len(data)

    valid_frames = int(
        data["valid"].sum()
    )

    invalid_frames = (
        total_frames
        - valid_frames
    )

    valid_percentage = (
        valid_frames
        / total_frames
        * 100
        if total_frames > 0
        else 0
    )


    print(
        f"FPS del MP4: "
        f"{reported_fps:.2f}"
    )

    print(
        f"Frames procesados: "
        f"{total_frames}"
    )

    print(
        f"Frames válidos: "
        f"{valid_frames}"
    )

    print(
        f"Frames no válidos: "
        f"{invalid_frames}"
    )

    print(
        "Disponibilidad bajo "
        "criterio actual: "
        f"{valid_percentage:.2f}%"
    )

    print(
        f"Primer timestamp: "
        f"{data['timestamp_s'].iloc[0]:.6f}s"
    )

    print(
        f"Último timestamp: "
        f"{data['timestamp_s'].iloc[-1]:.6f}s"
    )

    print(
        f"CSV guardado en: "
        f"{output_path}"
    )


    return {
        "repetition": repetition,
        "frames": total_frames,
        "valid_frames": valid_frames,
        "invalid_frames": (
            invalid_frames
        ),
        "valid_percentage": (
            valid_percentage
        ),
        "first_timestamp_s": (
            data[
                "timestamp_s"
            ].iloc[0]
        ),
        "last_timestamp_s": (
            data[
                "timestamp_s"
            ].iloc[-1]
        ),
    }


def main():
    summaries = []

    for repetition in REPETITIONS:
        summary = process_recording(
            repetition
        )

        summaries.append(
            summary
        )


    summary_data = pd.DataFrame(
        summaries
    )


    summary_path = (
        BASE_EXPERIMENT_PATH
        / "outputs"
        / (
            f"exp002_{SUBJECT_ID}_"
            "tracking_summary.csv"
        )
    )


    summary_data.to_csv(
        summary_path,
        index=False,
    )


    print()
    print(
        "================================"
    )

    print(
        "EXP-002D — TRACKING COMPLETADO"
    )

    print(
        "================================"
    )

    print()

    print(
        summary_data.to_string(
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
