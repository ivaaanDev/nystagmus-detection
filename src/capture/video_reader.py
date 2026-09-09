from pathlib import Path

import cv2


VIDEO_PATH = Path("data/raw/exp001_001_control_horizontal.mp4")


video = cv2.VideoCapture(str(VIDEO_PATH))

if not video.isOpened():
    raise ValueError(f"No se pudo abrir el video: {VIDEO_PATH}")


width = int(video.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(video.get(cv2.CAP_PROP_FRAME_HEIGHT))
fps = video.get(cv2.CAP_PROP_FPS)
total_frames_reported = int(video.get(cv2.CAP_PROP_FRAME_COUNT))

duration = total_frames_reported / fps


print(f"Archivo: {VIDEO_PATH.name}")
print(f"Resolución: {width}x{height}")
print(f"FPS: {fps:.2f}")
print(f"Frames reportados: {total_frames_reported}")
print(f"Duración estimada: {duration:.2f} segundos")


frames_read = 0

while True:
    success, frame = video.read()

    if not success:
        break

    frames_read += 1


video.release()


print(f"Frames leídos: {frames_read}")
