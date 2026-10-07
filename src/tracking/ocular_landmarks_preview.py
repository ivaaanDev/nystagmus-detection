from pathlib import Path

import cv2
import mediapipe as mp


VIDEO_PATH = Path("data/raw/exp001_001_control_horizontal.mp4")
MODEL_PATH = Path("models/mediapipe/face_landmarker.task")

OUTPUT_PATH = Path(
    "experiments/exp_001_tracking/outputs/"
    "exp001_001_ocular_landmarks_frame0.png"
)


RIGHT_EYE = [
    33, 7, 163, 144, 145, 153, 154, 155,
    133, 246, 161, 160, 159, 158, 157, 173
]

LEFT_EYE = [
    263, 249, 390, 373, 374, 380, 381, 382,
    362, 466, 388, 387, 386, 385, 384, 398
]

RIGHT_IRIS = [468, 469, 470, 471, 472]
LEFT_IRIS = [473, 474, 475, 476, 477]


video = cv2.VideoCapture(str(VIDEO_PATH))

if not video.isOpened():
    raise ValueError(f"No se pudo abrir el video: {VIDEO_PATH}")


success, frame = video.read()
video.release()

if not success:
    raise ValueError("No se pudo leer el primer frame.")


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


def draw_landmark(index, radius):
    landmark = landmarks[index]

    x = int(landmark.x * width)
    y = int(landmark.y * height)

    cv2.circle(
        frame,
        (x, y),
        radius,
        (0, 255, 0),
        -1,
    )


for index in RIGHT_EYE:
    draw_landmark(index, 2)

for index in LEFT_EYE:
    draw_landmark(index, 2)


for index in RIGHT_IRIS:
    draw_landmark(index, 3)

for index in LEFT_IRIS:
    draw_landmark(index, 3)


OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)

cv2.imwrite(str(OUTPUT_PATH), frame)


cv2.imshow("EXP-001C - Ojos e iris", frame)

cv2.waitKey(0)

cv2.destroyAllWindows()


print(f"Landmarks ojo derecho: {len(RIGHT_EYE)}")
print(f"Landmarks ojo izquierdo: {len(LEFT_EYE)}")
print(f"Landmarks iris derecho: {len(RIGHT_IRIS)}")
print(f"Landmarks iris izquierdo: {len(LEFT_IRIS)}")
print(f"Imagen guardada en: {OUTPUT_PATH}")
