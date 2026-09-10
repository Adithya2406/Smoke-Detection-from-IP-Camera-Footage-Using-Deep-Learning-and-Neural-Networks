# Smoke and Smoker Detection

A Streamlit application for detecting smoke, fire, and smoking activity in images and live camera feeds with YOLOv8 models.

## Features

- Separate smoke/fire and smoker-detection models
- Image upload, webcam, and runtime camera-stream inputs
- Configurable confidence threshold
- Annotated detection results
- Optional local sound, email, and phone alerts
- Credentials and private camera addresses loaded only at runtime

## Repository contents

| Path | Purpose |
|---|---|
| `app.py` | Streamlit user interface |
| `helper.py` | Inference, streaming, and alert helpers |
| `settings.py` | Portable model and input configuration |
| `smoke_fire.pt` | Smoke/fire detector |
| `smoker_robo.pt` | Smoker detector |
| `smoke_smoker_detect/` | Demo assets and reference YOLO weights |

## Setup

```bash
git clone <repository-url>
cd Smoke-Detection-from-IP-Camera-Footage-Using-Deep-Learning-and-Neural-Networks

python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
streamlit run app.py
```

The bundled models are used by default. To use different weights, set `SMOKE_MODEL_PATH` or `SMOKER_MODEL_PATH`.

## Camera streams

Select **Camera stream** in the sidebar and enter the address at runtime. The value is masked in the interface and is not written to the repository or a configuration file.

## Optional alerts

Alert delivery is disabled unless all required environment variables for a channel are configured.

Email variables:

```text
SMTP_HOST
SMTP_PORT
SMTP_USERNAME
SMTP_PASSWORD
ALERT_SENDER_EMAIL
ALERT_RECEIVER_EMAIL
```

Phone variables:

```text
TWILIO_ACCOUNT_SID
TWILIO_AUTH_TOKEN
TWILIO_FROM_NUMBER
TWILIO_TO_NUMBER
```

Store these values in your shell environment or an ignored local `.env` file. Never commit credentials or private camera addresses.

## Notes

- The audible alert uses the Windows sound API when available.
- Model accuracy depends on camera placement, lighting, smoke density, and the training distribution.
- This prototype should supplement—not replace—certified fire detection and emergency systems.
