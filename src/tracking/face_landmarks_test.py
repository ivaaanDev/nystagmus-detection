from pathlib import Path

import cv2
import mediapipe as mp


VIDEO_PATH = Path("data/raw/exp001_001_control_horizontal.mp4")
MODEL_PATH = Path("models/mediapipe/face_landmarker.task")


video = cv2.VideoCapture(str(VIDEO_PATH))

if not video.isOpened():
    raise ValueError(f"No se pudo abrir el video: {VIDEO_PATH}")


success, frame = video.read()

video.release()


if not success:
    raise ValueError("No se pudo leer el primer frame del video.")


frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

mp_image = mp.Image(
    image_format=mp.ImageFormat.SRGB,
    data=frame_rgb,
)


BaseOptions = mp.tasks.BaseOptions
FaceLandmarker = mp.tasks.vision.FaceLandmarker
FaceLandmarkerOptions = mp.tasks.vision.FaceLandmarkerOptions
RunningMode = mp.tasks.vision.RunningMode


options = FaceLandmarkerOptions(
    base_options=BaseOptions(model_asset_path=str(MODEL_PATH)),
    running_mode=RunningMode.IMAGE,
    num_faces=1,
)


with FaceLandmarker.create_from_options(options) as landmarker:
    result = landmarker.detect(mp_image)


print(f"Rostros detectados: {len(result.face_landmarks)}")

if result.face_landmarks:
    landmarks = result.face_landmarks[0]

    print(f"Landmarks detectados: {len(landmarks)}")
