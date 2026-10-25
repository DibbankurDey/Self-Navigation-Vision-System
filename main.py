import os
import sys

# If run by Streamlit (Cloud or CLI), route directly to the Web Dashboard
is_streamlit = False
try:
    import streamlit as st
    from streamlit.runtime.scriptrunner import get_script_run_ctx
    if get_script_run_ctx() is not None:
        is_streamlit = True
except Exception:
    pass

if not is_streamlit and any("streamlit" in arg.lower() for arg in sys.argv):
    is_streamlit = True

if is_streamlit:
    import runpy
    current_dir = os.path.dirname(os.path.abspath(__file__))
    dashboard_app = os.path.join(current_dir, "dashboard", "app.py")
    runpy.run_path(dashboard_app, run_name="__main__")
    sys.exit(0)

# Otherwise, run local desktop OpenCV script
from navigation.voice_assistant import speak
from vision.object_detection import detect_objects
from vision.distance_estimator import estimate_distance
from Planning.decision_engine import make_decision
from Planning.collision_warning import collision_warning
import cv2
# Path to image
image_path = "data/images/road.jpg"

# Detect objects
result, objects = detect_objects(image_path)

print("\n========== DETECTED OBJECTS ==========\n")

for obj in objects:
    print(obj)

    distance = estimate_distance(obj)
    print("Distance:", distance)
    print()

# Navigation decision
decision = make_decision(objects, result.shape[1])

print("\n========== NAVIGATION DECISION ==========")
print(decision)
speak(decision)
# Collision warning
warning = collision_warning(objects)

print("\n========== COLLISION STATUS ==========")
print(warning)

if warning != "SAFE":
    speak(warning)

# Display warning on image
cv2.putText(
    result,
    warning,
    (20, 50),
    cv2.FONT_HERSHEY_SIMPLEX,
    1,
    (0, 0, 255),
    2
)

result = cv2.resize(result, (1200, 700))

cv2.imshow("Self Navigation Vision System", result)

cv2.waitKey(0)
cv2.destroyAllWindows()