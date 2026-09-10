import os
from pathlib import Path


ROOT = Path(__file__).resolve().parent

IMAGE = "Image"
WEBCAM = "Webcam"
RTSP = "Camera stream"
SOURCES_LIST = [IMAGE, WEBCAM, RTSP]

SMOKE_MODEL = Path(os.getenv("SMOKE_MODEL_PATH", ROOT / "smoke_fire.pt"))
SMOKER_MODEL = Path(os.getenv("SMOKER_MODEL_PATH", ROOT / "smoker_robo.pt"))
WEBCAM_PATH = int(os.getenv("WEBCAM_INDEX", "0"))
