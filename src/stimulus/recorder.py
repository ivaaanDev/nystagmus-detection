from pathlib import Path
import csv
import threading
import time

import cv2


class CameraRecorder:
    def __init__(
        self,
        video_path,
        timestamps_path,
        camera_index=0,
        requested_width=640,
        requested_height=360,
        requested_fps=30,
    ):
        self.video_path = Path(video_path)
        self.timestamps_path = Path(timestamps_path)

        self.camera = cv2.VideoCapture(
            camera_index,
            cv2.CAP_V4L2,
        )

        if not self.camera.isOpened():
            raise ValueError(
                f"No se pudo abrir la cámara {camera_index}."
            )

        # Solicitar MJPG explícitamente.
        self.camera.set(
            cv2.CAP_PROP_FOURCC,
            cv2.VideoWriter_fourcc(*"MJPG"),
        )

        self.camera.set(
            cv2.CAP_PROP_FRAME_WIDTH,
            requested_width,
        )

        self.camera.set(
            cv2.CAP_PROP_FRAME_HEIGHT,
            requested_height,
        )

        self.camera.set(
            cv2.CAP_PROP_FPS,
            requested_fps,
        )

        self.width = int(
            self.camera.get(
                cv2.CAP_PROP_FRAME_WIDTH
            )
        )

        self.height = int(
            self.camera.get(
                cv2.CAP_PROP_FRAME_HEIGHT
            )
        )

        self.reported_fps = self.camera.get(
            cv2.CAP_PROP_FPS
        )

        if self.reported_fps <= 0:
            self.reported_fps = requested_fps

        self.video_path.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        self.timestamps_path.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        fourcc = cv2.VideoWriter_fourcc(
            *"mp4v"
        )

        self.writer = cv2.VideoWriter(
            str(self.video_path),
            fourcc,
            self.reported_fps,
            (
                self.width,
                self.height,
            ),
        )

        if not self.writer.isOpened():
            self.camera.release()

            raise ValueError(
                "No se pudo crear el archivo de video."
            )

        self.timestamps = []
        self.frame_number = 0

        self.protocol_start = None

        # Detiene completamente el hilo.
        self.stop_event = threading.Event()

        # Indica si los frames deben guardarse.
        self.recording_event = threading.Event()

        self.thread = None
        self.capture_error = None


    def start_capture(self):
        """
        Comienza a leer la cámara continuamente.

        Los frames se descartan hasta que
        begin_recording() sea llamado.
        """

        if self.thread is not None:
            raise RuntimeError(
                "La captura ya fue iniciada."
            )

        self.stop_event.clear()
        self.recording_event.clear()

        self.thread = threading.Thread(
            target=self._capture_loop,
            name="camera-recorder",
        )

        self.thread.start()


    def begin_recording(
        self,
        protocol_start,
    ):
        """
        Activa la escritura de frames usando
        protocol_start como t = 0.
        """

        self.protocol_start = protocol_start

        self.recording_event.set()


    def stop_recording(self):
        """
        Deja de guardar frames, pero el hilo
        puede seguir consumiendo la cámara.
        """

        self.recording_event.clear()


    def _capture_loop(self):
        try:
            while not self.stop_event.is_set():

                success, frame = self.camera.read()

                if not success:
                    continue

                # Mientras no haya iniciado el protocolo,
                # simplemente descartamos los frames.
                if not self.recording_event.is_set():
                    continue

                capture_time = time.perf_counter()

                timestamp_s = (
                    capture_time
                    - self.protocol_start
                )

                self.writer.write(frame)

                self.timestamps.append(
                    {
                        "frame": self.frame_number,
                        "timestamp_s": round(
                            timestamp_s,
                            6,
                        ),
                    }
                )

                self.frame_number += 1

        except Exception as error:
            self.capture_error = error

            self.stop_event.set()


    def stop_capture(self):
        self.recording_event.clear()
        self.stop_event.set()

        if self.thread is not None:
            self.thread.join()

        self.thread = None


    def save_timestamps(self):
        with self.timestamps_path.open(
            "w",
            newline="",
            encoding="utf-8",
        ) as file:

            writer = csv.DictWriter(
                file,
                fieldnames=[
                    "frame",
                    "timestamp_s",
                ],
            )

            writer.writeheader()

            writer.writerows(
                self.timestamps
            )


    def release(self):
        self.stop_capture()

        self.writer.release()
        self.camera.release()

        self.save_timestamps()

        if self.capture_error is not None:
            raise RuntimeError(
                "Ocurrió un error durante "
                "la captura de cámara."
            ) from self.capture_error
