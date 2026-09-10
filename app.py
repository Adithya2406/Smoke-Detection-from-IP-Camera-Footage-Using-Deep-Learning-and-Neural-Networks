from pathlib import Path

from PIL import Image
import streamlit as st

import helper
import settings


st.set_page_config(
    page_title="Smoke and Smoker Detection",
    page_icon="🔥",
    layout="wide",
    initial_sidebar_state="expanded",
)
st.title("Smoke and Smoker Detection with YOLOv8")
st.caption("Run object detection on an image, webcam, or user-provided camera stream.")

model_type = st.sidebar.selectbox(
    "Detection model", ("Smoker Detection", "Smoke Detection")
)
confidence = st.sidebar.slider("Confidence threshold", 0.05, 1.0, 0.40, 0.05)
source_type = st.sidebar.selectbox("Input source", settings.SOURCES_LIST)

model_path = (
    settings.SMOKER_MODEL
    if model_type == "Smoker Detection"
    else settings.SMOKE_MODEL
)

try:
    model = helper.load_model(Path(model_path))
except Exception as exc:
    st.error(f"Unable to load model from {model_path}")
    st.exception(exc)
    st.stop()

if source_type == settings.IMAGE:
    source = st.sidebar.file_uploader(
        "Choose an image", type=("jpg", "jpeg", "png", "bmp", "webp")
    )
    if source is not None:
        image = Image.open(source).convert("RGB")
        left, right = st.columns(2)
        left.image(image, caption="Input", use_container_width=True)
        if st.sidebar.button("Detect objects"):
            plotted, labels = helper.detect_image(model, image, confidence)
            right.image(plotted, caption="Detections", use_container_width=True)
            if labels:
                st.success("Detected: " + ", ".join(sorted(labels)))
                helper.send_configured_alert(
                    f"{model_type}: {', '.join(sorted(labels))}"
                )
            else:
                st.info("No objects met the selected confidence threshold.")

elif source_type == settings.WEBCAM:
    if st.sidebar.button("Start detection"):
        helper.play_stream(settings.WEBCAM_PATH, model, confidence, model_type)

elif source_type == settings.RTSP:
    stream_address = st.sidebar.text_input(
        "Camera stream address",
        type="password",
        help="Entered at runtime and never stored by the application.",
    )
    if st.sidebar.button("Start detection"):
        if not stream_address:
            st.sidebar.error("Enter a camera stream address.")
        else:
            helper.play_stream(stream_address, model, confidence, model_type)
