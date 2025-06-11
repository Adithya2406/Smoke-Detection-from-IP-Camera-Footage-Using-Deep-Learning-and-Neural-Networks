from pathlib import Path
import sys

# Sources
# IMAGE = 'Image'
# VIDEO = 'Video'
WEBCAM = 'Webcam'
RTSP = 'RTSP'
# YOUTUBE = 'YouTube'

SOURCES_LIST = [RTSP, WEBCAM]

# VIDEO_1_PATH = r"D:\BMSIT\Hackathon-fixed\hackathon\hackathon\hack\smoke_smoker_detect\videos\smoker_long4.mp4"
# VIDEOS_DICT = {
#     'video_1': VIDEO_1_PATH,
# }

DETECTION_MODEL = r"C:\Users\adith\Downloads\Team-Whirlpool_24hr_Hackathon\hack\smoke_fire.pt"
SEGMENTATION_MODEL = r"C:\Users\adith\Downloads\Team-Whirlpool_24hr_Hackathon\hack\smoker_robo.pt"

# Webcam
WEBCAM_PATH = 0
