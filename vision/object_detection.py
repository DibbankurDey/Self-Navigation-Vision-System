from ultralytics import YOLO
import cv2

model = YOLO("yolov8n.pt")

def detect_objects(image_path):

    img = cv2.imread(image_path)

    if img is None:
        print("Error loading image")
        return None

    results = model(img)

    detected_objects = []

    for box in results[0].boxes:

        class_id = int(box.cls[0])

        class_name = model.names[class_id]

        confidence = float(box.conf[0])
        x1, y1, x2, y2 = box.xyxy[0]
        
        detected_objects.append({
        "class": class_name,
        "confidence": confidence,
        "x1": int(x1),
        "y1": int(y1),
        "x2": int(x2),
        "y2": int(y2)
    })

    annotated = results[0].plot()

    return annotated, detected_objects