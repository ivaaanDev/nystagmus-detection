from pathlib import Path
import csv
import time

import cv2
import numpy as np

from protocol import (
    HORIZONTAL_PROTOCOL,
    TARGET_POSITIONS,
)

from recorder import CameraRecorder


WINDOW_NAME = "Horizontal Stimulus"

CANVAS_WIDTH = 1280
CANVAS_HEIGHT = 720

TARGET_RADIUS = 12

COUNTDOWN_SECONDS = 3


SUBJECT_ID = "S001"
REPETITION = 5


BASE_OUTPUT = Path(
    "experiments/"
    "exp_002_signal_characterization"
)


STIMULUS_LOG_PATH = (
    BASE_OUTPUT
    / "stimulus_logs"
    / f"exp002_{SUBJECT_ID.lower()}_rep{REPETITION:02d}_stimulus.csv"
)


VIDEO_PATH = (
    BASE_OUTPUT
    / "recordings"
    / f"exp002_{SUBJECT_ID.lower()}_rep{REPETITION:02d}_video.mp4"
)


FRAME_TIMESTAMPS_PATH = (
    BASE_OUTPUT
    / "recordings"
    / f"exp002_{SUBJECT_ID.lower()}_rep{REPETITION:02d}_frames.csv"
)


def normalized_to_pixels(position):
    x_norm, y_norm = position

    x_px = int(
        x_norm * CANVAS_WIDTH
    )

    y_px = int(
        y_norm * CANVAS_HEIGHT
    )

    return x_px, y_px


def create_blank_frame():
    return np.zeros(
        (
            CANVAS_HEIGHT,
            CANVAS_WIDTH,
            3,
        ),
        dtype=np.uint8,
    )


def create_stimulus_frame(
    target_name,
):
    frame = create_blank_frame()

    target_position = (
        TARGET_POSITIONS[target_name]
    )

    x, y = normalized_to_pixels(
        target_position
    )

    cv2.circle(
        frame,
        (x, y),
        TARGET_RADIUS,
        (255, 255, 255),
        -1,
    )

    return frame


def create_text_frame(text):
    frame = create_blank_frame()

    font = cv2.FONT_HERSHEY_SIMPLEX
    font_scale = 3
    thickness = 5

    (
        text_width,
        text_height,
    ), _ = cv2.getTextSize(
        text,
        font,
        font_scale,
        thickness,
    )

    x = (
        CANVAS_WIDTH
        - text_width
    ) // 2

    y = (
        CANVAS_HEIGHT
        + text_height
    ) // 2

    cv2.putText(
        frame,
        text,
        (x, y),
        font,
        font_scale,
        (255, 255, 255),
        thickness,
        cv2.LINE_AA,
    )

    return frame


def wait_for_start():
    frame = create_text_frame(
        "Presiona ESPACIO"
    )

    while True:
        cv2.imshow(
            WINDOW_NAME,
            frame,
        )

        key = cv2.waitKey(1) & 0xFF

        if key == 32:
            return True

        if (
            key == 27
            or key == ord("q")
        ):
            return False


def run_countdown():
    for number in range(
        COUNTDOWN_SECONDS,
        0,
        -1,
    ):
        frame = create_text_frame(
            str(number)
        )

        start = time.perf_counter()

        while (
            time.perf_counter()
            - start
            < 1.0
        ):
            cv2.imshow(
                WINDOW_NAME,
                frame,
            )

            key = cv2.waitKey(1) & 0xFF

            if (
                key == 27
                or key == ord("q")
            ):
                return False

    return True


def save_stimulus_log(rows):
    STIMULUS_LOG_PATH.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    fieldnames = [
        "event",
        "target",
        "planned_start_s",
        "planned_end_s",
        "actual_start_s",
        "actual_end_s",
        "actual_duration_s",
        "start_error_ms",
        "end_error_ms",
        "x_norm",
        "y_norm",
    ]

    with STIMULUS_LOG_PATH.open(
        "w",
        newline="",
        encoding="utf-8",
    ) as file:

        writer = csv.DictWriter(
            file,
            fieldnames=fieldnames,
        )

        writer.writeheader()

        writer.writerows(rows)


def get_camera_fourcc(recorder):
    camera_fourcc = int(
        recorder.camera.get(
            cv2.CAP_PROP_FOURCC
        )
    )

    return "".join(
        chr(
            (
                camera_fourcc
                >> (8 * i)
            )
            & 0xFF
        )
        for i in range(4)
    )


def run_protocol():
    cv2.namedWindow(
        WINDOW_NAME,
        cv2.WINDOW_NORMAL,
    )

    cv2.setWindowProperty(
        WINDOW_NAME,
        cv2.WND_PROP_FULLSCREEN,
        cv2.WINDOW_FULLSCREEN,
    )

    recorder = CameraRecorder(
        video_path=VIDEO_PATH,
        timestamps_path=(
            FRAME_TIMESTAMPS_PATH
        ),
        camera_index=1,
        requested_width=640,
        requested_height=360,
        requested_fps=30,
    )


    print()
    print("Cámara inicializada")

    print(
        f"Resolución: "
        f"{recorder.width}x{recorder.height}"
    )

    print(
        f"FPS reportados: "
        f"{recorder.reported_fps:.2f}"
    )

    print(
        "Formato de cámara: "
        f"{get_camera_fourcc(recorder)}"
    )

    print()

    # La cámara empieza a capturar desde aquí,
    # pero todavía NO guarda frames.
    recorder.start_capture()


    if not wait_for_start():
        recorder.release()

        cv2.destroyAllWindows()

        print(
            "Experimento cancelado "
            "antes de iniciar."
        )

        return


    if not run_countdown():
        recorder.release()

        cv2.destroyAllWindows()

        print(
            "Experimento cancelado "
            "durante el countdown."
        )

        return


    log_rows = []

    # Este será el reloj común para:
    #
    # - estímulo
    # - cámara
    #
    protocol_start = time.perf_counter()

    recorder.begin_recording(
        protocol_start
    )


    planned_start_s = 0.0

    aborted = False


    for event_index, step in enumerate(
        HORIZONTAL_PROTOCOL
    ):
        planned_end_s = (
            planned_start_s
            + step.duration_s
        )

        x_norm, y_norm = (
            TARGET_POSITIONS[
                step.target
            ]
        )

        stimulus_frame = (
            create_stimulus_frame(
                step.target
            )
        )


        actual_start_s = (
            time.perf_counter()
            - protocol_start
        )


        while True:
            elapsed_s = (
                time.perf_counter()
                - protocol_start
            )

            if (
                elapsed_s
                >= planned_end_s
            ):
                break


            # Aquí ya NO hacemos camera.read().
            #
            # El hilo de CameraRecorder se
            # encarga independientemente.
            cv2.imshow(
                WINDOW_NAME,
                stimulus_frame,
            )


            key = (
                cv2.waitKey(1)
                & 0xFF
            )


            if (
                key == 27
                or key == ord("q")
            ):
                aborted = True
                break


        actual_end_s = (
            time.perf_counter()
            - protocol_start
        )


        actual_duration_s = (
            actual_end_s
            - actual_start_s
        )


        start_error_ms = (
            actual_start_s
            - planned_start_s
        ) * 1000


        end_error_ms = (
            actual_end_s
            - planned_end_s
        ) * 1000


        log_rows.append(
            {
                "event": event_index,

                "target": step.target,

                "planned_start_s": round(
                    planned_start_s,
                    6,
                ),

                "planned_end_s": round(
                    planned_end_s,
                    6,
                ),

                "actual_start_s": round(
                    actual_start_s,
                    6,
                ),

                "actual_end_s": round(
                    actual_end_s,
                    6,
                ),

                "actual_duration_s": round(
                    actual_duration_s,
                    6,
                ),

                "start_error_ms": round(
                    start_error_ms,
                    3,
                ),

                "end_error_ms": round(
                    end_error_ms,
                    3,
                ),

                "x_norm": x_norm,

                "y_norm": y_norm,
            }
        )


        if aborted:
            break


        planned_start_s = (
            planned_end_s
        )


    # release() ahora:
    #
    # 1. detiene el hilo
    # 2. espera a que termine
    # 3. cierra VideoWriter
    # 4. libera la cámara
    # 5. guarda timestamps

    recorder.stop_recording()

    recorder.release()


    cv2.destroyAllWindows()


    save_stimulus_log(
        log_rows
    )


    print()
    print(
        "STIM-001G — "
        "Captura sincronizada"
    )

    print()


    for row in log_rows:
        print(
            f"{row['target']:>6} | "
            f"planeado="
            f"{row['planned_start_s']:.3f}s | "
            f"real="
            f"{row['actual_start_s']:.3f}s | "
            f"fin="
            f"{row['actual_end_s']:.3f}s"
        )


    print()

    print(
        f"Frames capturados: "
        f"{recorder.frame_number}"
    )


    if recorder.frame_number > 1:
        frame_times = [
            row["timestamp_s"]
            for row
            in recorder.timestamps
        ]


        recording_duration = (
            frame_times[-1]
            - frame_times[0]
        )


        measured_fps = (
            (len(frame_times) - 1)
            / recording_duration
            if recording_duration > 0
            else 0
        )


        print(
            "FPS medidos por timestamps: "
            f"{measured_fps:.2f}"
        )


        print(
            "Primer timestamp: "
            f"{frame_times[0]:.6f} s"
        )

        print(
            "Último timestamp: "
            f"{frame_times[-1]:.6f} s"
        )


    print()


    if aborted:
        print(
            "Protocolo cancelado "
            "por el usuario."
        )

    else:
        print(
            "Protocolo completado "
            "correctamente."
        )


    print()

    print(
        f"Video: {VIDEO_PATH}"
    )

    print(
        "Timestamps de frames: "
        f"{FRAME_TIMESTAMPS_PATH}"
    )

    print(
        "Log del estímulo: "
        f"{STIMULUS_LOG_PATH}"
    )


if __name__ == "__main__":
    run_protocol()
