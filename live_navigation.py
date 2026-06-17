import cv2
from vision.object_detection import detect_objects
from Planning.decision_engine import make_decision
from navigation.voice_assistant import speak

cap = cv2.VideoCapture(0)

last_decision = ""

while True:

    ret, frame = cap.read()

    if not ret:
        break

    # Save frame temporarily
    cv2.imwrite("temp_frame.jpg", frame)

    result, objects = detect_objects("temp_frame.jpg")

    if result is None:
        continue

    decision = make_decision(objects, result.shape[1])

    # Speak only when decision changes
    if decision != last_decision:
        speak(decision)
        last_decision = decision

    cv2.putText(
        result,
        decision,
        (20, 50),
        cv2.FONT_HERSHEY_SIMPLEX,
        1,
        (0, 255, 0),
        2
    )

    cv2.imshow("Live Navigation", result)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()