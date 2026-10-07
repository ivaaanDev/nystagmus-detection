from pathlib import Path

import cv2
import mediapipe as mp


VIDEO_PATH = Path("data/raw/exp001_001_control_horizontal.mp4")
MODEL_PATH = Path("models/mediapipe/face_landmarker.task")

OUTPUT_PATH = Path(
    "experiments/exp_001_tracking/outputs/"
    "exp001_001_landmarks_frame0.png"
)


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


if not result.face_landmarks:
    raise ValueError("No se detectó ningún rostro.")


landmarks = result.face_landmarks[0]

height, width, _ = frame.shape


for landmark in landmarks:
    x_px = int(landmark.x * width)
    y_px = int(landmark.y * height)

    cv2.circle(
        frame,
        (x_px, y_px),
        1,
        (0, 255, 0),
        -1,
    )


OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)

cv2.imwrite(str(OUTPUT_PATH), frame)


cv2.imshow("EXP-001B - Landmarks", frame)

cv2.waitKey(0)

cv2.destroyAllWindows()


print(f"Landmarks dibujados: {len(landmarks)}")
print(f"Imagen guardada en: {OUTPUT_PATH}")
