from ultralytics import YOLO
from vision.lane_detection_video import detect_lanes
import cv2

model = YOLO("yolov8n.pt")

video = cv2.VideoCapture("data/video/road_video.mp4")

while True:

    ret, frame = video.read()

    if not ret:
        break

    results = model(frame)

    annotated_frame = results[0].plot()
    
    annotated_frame = detect_lanes(annotated_frame)

    cv2.imshow("Self Navigation", annotated_frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

video.release()
cv2.destroyAllWindows()