import streamlit as st
import cv2
import tempfile
import sys
import os

# Add project root to Python path
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from vision.object_detection import detect_objects
from Planning.decision_engine import make_decision

st.set_page_config(page_title="Self Navigation System")

st.title("🚗 Self Navigation Vision System")

uploaded_file = st.file_uploader(
    "Upload an image",
    type=["jpg", "jpeg", "png"]
)

if uploaded_file is not None:

    # Save uploaded image temporarily
    with tempfile.NamedTemporaryFile(delete=False, suffix=".jpg") as temp_file:
        temp_file.write(uploaded_file.read())
        image_path = temp_file.name

    st.write("Image uploaded successfully")

    # Run object detection
    result, objects = detect_objects(image_path)

    if result is None:
        st.error("Failed to process image")
    else:

        # Navigation decision
        decision = make_decision(
            objects,
            result.shape[1]
        )

        # Convert BGR → RGB
        result_rgb = cv2.cvtColor(
            result,
            cv2.COLOR_BGR2RGB
        )

        # Display image
        st.image(
            result_rgb,
            caption="Detected Objects",
            use_container_width=True
        )
        st.header("Video Navigation")
        video_file = st.file_uploader(
            "Upload Video",
            type=["mp4"],
            key="video"
        )
        # Display detected objects
        st.subheader("Detected Objects")

        for obj in objects:
            st.write(obj)

        # Display decision
        st.subheader("Navigation Decision")

        st.success(decision)