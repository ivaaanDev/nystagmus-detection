from pathlib import Path

import cv2


VIDEO_PATH = Path("data/raw/exp001_001_control_horizontal.mp4")


video = cv2.VideoCapture(str(VIDEO_PATH))

if not video.isOpened():
    raise ValueError(f"No se pudo abrir el video: {VIDEO_PATH}")


fps = video.get(cv2.CAP_PROP_FPS)

if fps <= 0:
    raise ValueError("El video no reporta una tasa de FPS válida.")


delay_ms = max(1, round(1000 / fps))


while True:
    success, frame = video.read()

    if not success:
        break

    frame_number = int(video.get(cv2.CAP_PROP_POS_FRAMES)) - 1
    timestamp_ms = video.get(cv2.CAP_PROP_POS_MSEC)
    timestamp_s = timestamp_ms / 1000

    text = f"Frame: {frame_number} | Tiempo: {timestamp_s:.3f} s"

    cv2.putText(
        frame,
        text,
        (10, 30),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.6,
        (255, 255, 255),
        2,
    )

    cv2.imshow("EXP-001A - Video", frame)

    key = cv2.waitKey(delay_ms) & 0xFF

    if key == ord("q"):
        break


video.release()
cv2.destroyAllWindows()
