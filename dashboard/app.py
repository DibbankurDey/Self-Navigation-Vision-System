import streamlit as st
import cv2
import tempfile
import sys
import os
import pandas as pd
import numpy as np

# Add project root to Python path
PROJECT_ROOT = os.path.dirname(os.path.dirname(__file__))
if PROJECT_ROOT not in sys.path:
    sys.path.append(PROJECT_ROOT)

from vision.object_detection import detect_objects
from vision.distance_estimator import estimate_distance
from vision.lane_detection_video import detect_lanes
from Planning.decision_engine import make_decision
from Planning.collision_warning import collision_warning

st.set_page_config(
    page_title="Self-Navigation Vision System",
    page_icon="🚗",
    layout="wide"
)

# Custom CSS for polished aesthetic
st.markdown("""
<style>
    .metric-card {
        background: #1e222d;
        border-radius: 10px;
        padding: 15px;
        margin-bottom: 10px;
        border: 1px solid #2d3345;
    }
    .badge-safe {
        background-color: #1b5e20;
        color: #ffffff;
        padding: 6px 14px;
        border-radius: 8px;
        font-weight: bold;
        display: inline-block;
    }
    .badge-warning {
        background-color: #b71c1c;
        color: #ffffff;
        padding: 6px 14px;
        border-radius: 8px;
        font-weight: bold;
        display: inline-block;
    }
    .decision-badge {
        font-size: 1.3rem;
        font-weight: 700;
        padding: 10px 18px;
        border-radius: 10px;
        text-align: center;
    }
</style>
""", unsafe_allow_html=True)

st.title("🚗 Self-Navigation Vision System")
st.caption("AI-powered obstacle detection, lane guidance, collision warnings, and navigation planning")

tabs = st.tabs(["📷 Image Navigation", "🎥 Video Navigation", "⚙️ Diagnostics & Info"])

# ----------------- TAB 1: IMAGE NAVIGATION -----------------
with tabs[0]:
    st.subheader("Image-Based Navigation Analysis")
    
    col_input, col_view = st.columns([1, 2])
    
    with col_input:
        img_source = st.radio("Select Image Source:", ["Sample Road Image", "Upload Custom Image"], horizontal=True)
        image_path = None
        img_array = None

        if img_source == "Sample Road Image":
            sample_path = os.path.join(PROJECT_ROOT, "data", "images", "road.jpg")
            if os.path.exists(sample_path):
                image_path = sample_path
                st.info("Loaded default sample: `data/images/road.jpg`")
            else:
                st.error("Default sample image not found at `data/images/road.jpg`")
        else:
            uploaded_file = st.file_uploader("Upload road image", type=["jpg", "jpeg", "png"])
            if uploaded_file is not None:
                with tempfile.NamedTemporaryFile(delete=False, suffix=".jpg") as tmp:
                    tmp.write(uploaded_file.read())
                    image_path = tmp.name

        voice_alert = st.checkbox("Announce decision via voice (pyttsx3)", value=False)
        process_btn = st.button("🚀 Analyze Image", type="primary", use_container_width=True)

    if (image_path is not None and process_btn) or (image_path is not None and "analyzed_img" in st.session_state):
        with st.spinner("Processing image with YOLOv8 & Navigation Engine..."):
            result, objects = detect_objects(image_path)
            st.session_state["analyzed_img"] = True
            
        if result is None:
            st.error("Error reading or processing the image.")
        else:
            decision = make_decision(objects, result.shape[1])
            warning = collision_warning(objects)

            # Voice announcement if enabled
            if voice_alert:
                try:
                    from navigation.voice_assistant import speak
                    speak(f"Navigation: {decision}. Collision status: {warning}")
                except Exception as e:
                    st.warning(f"Voice output unavailable: {e}")

            with col_view:
                # Key telemetry row
                m1, m2, m3 = st.columns(3)
                with m1:
                    st.metric("Detected Obstacles", len(objects))
                with m2:
                    if warning == "SAFE":
                        st.markdown("**Collision Status**<br><span class='badge-safe'>SAFE</span>", unsafe_allow_html=True)
                    else:
                        st.markdown("**Collision Status**<br><span class='badge-warning'>⚠️ COLLISION RISK</span>", unsafe_allow_html=True)
                with m3:
                    st.metric("Navigation Command", decision)

                # Show annotated image
                annotated_rgb = cv2.cvtColor(result, cv2.COLOR_BGR2RGB)
                st.image(annotated_rgb, caption="Object Detection & Navigation Overlay", use_container_width=True)

            # Detailed object table
            if objects:
                st.markdown("### 📋 Detected Objects Telemetry")
                table_rows = []
                for idx, obj in enumerate(objects, start=1):
                    dist = estimate_distance(obj)
                    table_rows.append({
                        "ID": idx,
                        "Class": obj["class"].capitalize(),
                        "Confidence": f"{obj['confidence'] * 100:.1f}%",
                        "Distance Estimate": dist,
                        "Bounding Box (X1, Y1, X2, Y2)": f"({obj['x1']}, {obj['y1']}, {obj['x2']}, {obj['y2']})"
                    })
                df = pd.DataFrame(table_rows)
                st.dataframe(df, use_container_width=True, hide_index=True)
            else:
                st.info("No obstacles detected in view. Road appears completely clear.")

# ----------------- TAB 2: VIDEO NAVIGATION -----------------
with tabs[1]:
    st.subheader("Video-Based Navigation & Lane Tracking")
    
    col_v_input, col_v_ctrl = st.columns([1, 1])
    
    with col_v_input:
        video_source = st.radio("Select Video Source:", ["Sample Road Video", "Upload Video"], horizontal=True)
        video_path = None

        if video_source == "Sample Road Video":
            default_vid = os.path.join(PROJECT_ROOT, "data", "video", "road_video.mp4")
            if os.path.exists(default_vid):
                video_path = default_vid
                st.info("Loaded default sample: `data/video/road_video.mp4`")
            else:
                st.error("Default sample video not found.")
        else:
            up_vid = st.file_uploader("Upload MP4 Video", type=["mp4"])
            if up_vid is not None:
                with tempfile.NamedTemporaryFile(delete=False, suffix=".mp4") as tmp_v:
                    tmp_v.write(up_vid.read())
                    video_path = tmp_v.name

    with col_v_ctrl:
        max_frames = st.slider("Max Frames to Process in Stream:", min_value=10, max_value=200, value=60, step=10)
        enable_lanes = st.checkbox("Overlay Lane Detection Lines", value=True)
        start_video = st.button("▶️ Start Video Stream Processing", type="primary")

    if video_path and start_video:
        cap = cv2.VideoCapture(video_path)
        fps = int(cap.get(cv2.CAP_PROP_FPS)) or 30
        total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        
        st.write(f"Processing video ({total_frames} total frames, displaying up to {max_frames} frames)...")

        video_placeholder = st.empty()
        status_placeholder = st.empty()
        progress_bar = st.progress(0.0)

        frame_count = 0
        from ultralytics import YOLO
        yolo_model = YOLO("yolov8n.pt")

        while cap.isOpened() and frame_count < max_frames:
            ret, frame = cap.read()
            if not ret:
                break
            
            frame_count += 1
            progress_bar.progress(frame_count / max_frames)

            # YOLO inference
            results = yolo_model(frame, verbose=False)
            annotated = results[0].plot()

            if enable_lanes:
                annotated = detect_lanes(annotated)

            # Extract objects for decision
            detected_objs = []
            for box in results[0].boxes:
                c_id = int(box.cls[0])
                conf = float(box.conf[0])
                bx1, by1, bx2, by2 = box.xyxy[0]
                detected_objs.append({
                    "class": yolo_model.names[c_id],
                    "confidence": conf,
                    "x1": int(bx1),
                    "y1": int(by1),
                    "x2": int(bx2),
                    "y2": int(by2)
                })

            decision = make_decision(detected_objs, frame.shape[1])
            warning = collision_warning(detected_objs)

            # Render status
            status_placeholder.markdown(
                f"**Frame:** {frame_count}/{max_frames} | "
                f"**Objects:** {len(detected_objs)} | "
                f"**Decision:** `{decision}` | "
                f"**Collision Warning:** `{warning}`"
            )

            # Convert BGR to RGB
            annotated_rgb = cv2.cvtColor(annotated, cv2.COLOR_BGR2RGB)
            video_placeholder.image(annotated_rgb, caption=f"Live Feed - Frame {frame_count}", use_container_width=True)

        cap.release()
        st.success(f"Video stream analysis complete! Processed {frame_count} frames.")

# ----------------- TAB 3: DIAGNOSTICS & INFO -----------------
with tabs[2]:
    st.subheader("System Architecture & Environment Diagnostics")
    
    col_d1, col_d2 = st.columns(2)
    with col_d1:
        st.markdown("""
        ### Module Architecture
        - **`vision/object_detection.py`**: YOLOv8 neural network object detector
        - **`vision/lane_detection_video.py`**: Canny edge + Hough transform lane detector
        - **`vision/distance_estimator.py`**: Heuristic bounding-box distance estimator
        - **`Planning/decision_engine.py`**: Trajectory steering & collision avoidance decision engine
        - **`Planning/collision_warning.py`**: Proximity risk alert system
        - **`navigation/voice_assistant.py`**: Text-to-speech audio guidance via `pyttsx3`
        """)

    with col_d2:
        model_exists = os.path.exists(os.path.join(PROJECT_ROOT, "yolov8n.pt"))
        img_exists = os.path.exists(os.path.join(PROJECT_ROOT, "data", "images", "road.jpg"))
        vid_exists = os.path.exists(os.path.join(PROJECT_ROOT, "data", "video", "road_video.mp4"))

        st.markdown("### Asset Verification")
        st.write(f"- YOLOv8 Weights (`yolov8n.pt`): {'✅ Present' if model_exists else '❌ Missing'}")
        st.write(f"- Sample Image (`data/images/road.jpg`): {'✅ Present' if img_exists else '❌ Missing'}")
        st.write(f"- Sample Video (`data/video/road_video.mp4`): {'✅ Present' if vid_exists else '❌ Missing'}")
        st.write(f"- OpenCV Version: `{cv2.__version__}`")