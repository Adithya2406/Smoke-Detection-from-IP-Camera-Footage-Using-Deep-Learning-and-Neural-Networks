import os
import platform
import smtplib
from email.mime.text import MIMEText
from pathlib import Path

import cv2
import numpy as np
from PIL import Image
import streamlit as st
from ultralytics import YOLO


def load_model(model_path: Path):
    if not model_path.exists():
        raise FileNotFoundError(model_path)
    return YOLO(str(model_path))


def _labels(result):
    labels = set()
    if result.boxes is None:
        return labels
    for class_id in result.boxes.cls.tolist():
        labels.add(str(result.names[int(class_id)]))
    return labels


def detect_image(model, image: Image.Image, confidence: float):
    result = model.predict(np.asarray(image), conf=confidence, verbose=False)[0]
    plotted = cv2.cvtColor(result.plot(), cv2.COLOR_BGR2RGB)
    return plotted, _labels(result)


def _beep():
    if platform.system() == "Windows":
        try:
            import winsound

            winsound.Beep(2000, 1200)
        except RuntimeError:
            pass


def _send_email(message: str):
    host = os.getenv("SMTP_HOST")
    username = os.getenv("SMTP_USERNAME")
    password = os.getenv("SMTP_PASSWORD")
    sender = os.getenv("ALERT_SENDER_EMAIL")
    receiver = os.getenv("ALERT_RECEIVER_EMAIL")
    if not all((host, username, password, sender, receiver)):
        return False

    port = int(os.getenv("SMTP_PORT", "587"))
    email = MIMEText(message)
    email["From"] = sender
    email["To"] = receiver
    email["Subject"] = "Smoke detection alert"

    with smtplib.SMTP(host, port) as server:
        server.starttls()
        server.login(username, password)
        server.sendmail(sender, [receiver], email.as_string())
    return True


def _place_call(message: str):
    account_sid = os.getenv("TWILIO_ACCOUNT_SID")
    auth_token = os.getenv("TWILIO_AUTH_TOKEN")
    to_number = os.getenv("TWILIO_TO_NUMBER")
    from_number = os.getenv("TWILIO_FROM_NUMBER")
    if not all((account_sid, auth_token, to_number, from_number)):
        return False

    from twilio.rest import Client

    client = Client(account_sid, auth_token)
    client.calls.create(
        twiml=f"<Response><Say>{message}</Say></Response>",
        to=to_number,
        from_=from_number,
    )
    return True


def send_configured_alert(message: str):
    _beep()
    try:
        email_sent = _send_email(message)
        call_placed = _place_call(message)
        if email_sent or call_placed:
            st.toast("Configured alert sent.")
    except Exception as exc:
        st.warning(f"Detection succeeded, but alert delivery failed: {exc}")


def play_stream(source, model, confidence: float, model_type: str):
    capture = cv2.VideoCapture(source)
    if not capture.isOpened():
        st.error("Unable to open the selected video source.")
        return

    frame_slot = st.empty()
    stop = st.button("Stop")
    alert_sent = False

    try:
        while capture.isOpened() and not stop:
            ok, frame = capture.read()
            if not ok:
                break
            result = model.predict(frame, conf=confidence, verbose=False)[0]
            labels = _labels(result)
            frame_slot.image(
                result.plot(),
                caption="Live detections",
                channels="BGR",
                use_container_width=True,
            )
            if labels and not alert_sent:
                send_configured_alert(
                    f"{model_type}: {', '.join(sorted(labels))}"
                )
                alert_sent = True
    finally:
        capture.release()
