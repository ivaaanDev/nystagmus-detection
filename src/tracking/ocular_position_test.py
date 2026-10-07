from pathlib import Path

import cv2
import mediapipe as mp
import numpy as np


VIDEO_PATH = Path("data/raw/exp001_001_control_horizontal.mp4")
MODEL_PATH = Path("models/mediapipe/face_landmarker.task")


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
            landmark_to_point(landmarks[index])
            for index in iris_indices
        ]
    )

    return points.mean(axis=0)


def normalized_position(iris, corner_1, corner_2):
    # Aseguramos que el eje siempre vaya
    # de izquierda a derecha dentro de la imagen.
    if corner_1[0] <= corner_2[0]:
        left_corner = corner_1
        right_corner = corner_2
    else:
        left_corner = corner_2
        right_corner = corner_1

    eye_axis = right_corner - left_corner

    eye_length_squared = np.dot(
        eye_axis,
        eye_axis,
    )

    if eye_length_squared == 0:
        raise ValueError(
            "Las esquinas del ojo tienen la misma posición."
        )

    iris_vector = iris - left_corner

    position = np.dot(
        iris_vector,
        eye_axis,
    ) / eye_length_squared

    return position


def read_frame_at_time(video, timestamp_s):
    video.set(
        cv2.CAP_PROP_POS_MSEC,
        timestamp_s * 1000,
    )

    success, frame = video.read()

    if not success:
        raise ValueError(
            f"No se pudo leer el frame en {timestamp_s} segundos."
        )

    return frame


def calculate_eye_positions(frame, landmarker):
    frame_rgb = cv2.cvtColor(
        frame,
        cv2.COLOR_BGR2RGB,
    )

    mp_image = mp.Image(
        image_format=mp.ImageFormat.SRGB,
        data=frame_rgb,
    )

    result = landmarker.detect(mp_image)

    if not result.face_landmarks:
        return None

    landmarks = result.face_landmarks[0]

    right_iris = iris_center(
        landmarks,
        RIGHT_IRIS,
    )

    left_iris = iris_center(
        landmarks,
        LEFT_IRIS,
    )

    right_corner_1 = landmark_to_point(
        landmarks[RIGHT_EYE_CORNERS[0]]
    )

    right_corner_2 = landmark_to_point(
        landmarks[RIGHT_EYE_CORNERS[1]]
    )

    left_corner_1 = landmark_to_point(
        landmarks[LEFT_EYE_CORNERS[0]]
    )

    left_corner_2 = landmark_to_point(
        landmarks[LEFT_EYE_CORNERS[1]]
    )

    right_position = normalized_position(
        right_iris,
        right_corner_1,
        right_corner_2,
    )

    left_position = normalized_position(
        left_iris,
        left_corner_1,
        left_corner_2,
    )

    return right_position, left_position


video = cv2.VideoCapture(str(VIDEO_PATH))

if not video.isOpened():
    raise ValueError(
        f"No se pudo abrir el video: {VIDEO_PATH}"
    )


BaseOptions = mp.tasks.BaseOptions
FaceLandmarker = mp.tasks.vision.FaceLandmarker
FaceLandmarkerOptions = mp.tasks.vision.FaceLandmarkerOptions
RunningMode = mp.tasks.vision.RunningMode


options = FaceLandmarkerOptions(
    base_options=BaseOptions(
        model_asset_path=str(MODEL_PATH)
    ),
    running_mode=RunningMode.IMAGE,
    num_faces=1,
)


timestamps = [
    1.0,  # Centro
    3.0,  # Izquierda
    7.0,  # Derecha
]


with FaceLandmarker.create_from_options(options) as landmarker:

    for timestamp_s in timestamps:
        frame = read_frame_at_time(
            video,
            timestamp_s,
        )

        positions = calculate_eye_positions(
            frame,
            landmarker,
        )

        if positions is None:
            print(
                f"{timestamp_s:.1f} s -> rostro no detectado"
            )
            continue

        right_x, left_x = positions

        print(
            f"{timestamp_s:.1f} s -> "
            f"right_x={right_x:.4f}, "
            f"left_x={left_x:.4f}"
        )


video.release()
