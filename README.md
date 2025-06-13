## Smoke Detection from IP Camera Footage Using Deep Learning and Neural Networks
A robust tool for real-time smoke and smoker detection from IP camera streams, leveraging deep learning and neural networks to provide instant alerts and notifications for enhanced safety and monitoring.

---
**Table of Contents**
- Overview  
- Features  
- How It Works  
- Installation  
- Usage  
- Application  
- Alerts & Notifications  
- Requirements  
- Contributing  
- License  

---
## Overview
This project enables rapid detection of smoke and smokers from live IP camera feeds using advanced deep learning models. It is designed for real-time monitoring in environments where early smoke detection is critical, such as industrial sites, public spaces, and residential buildings. The system provides immediate alerts via multiple channels to ensure prompt response and minimize risks.

---
## Features
- Real-time smoke and smoker detection using neural networks  
- Supports multiple input streams: Webcam and RTSP (IP camera)  
- User-friendly web interface powered by Streamlit  
- Choice between Smoke Detection and Smoker Detection models  
- Multi-channel alert system: phone call, buzzer, and email with attachment  
- Easy deployment and configuration  

---
## How It Works
1. The system captures video streams from a webcam or IP camera (RTSP).
2. Deep learning models process each frame to detect smoke or smokers.
3. Upon detection, the system triggers alerts to notify users via configured channels.
4. The web interface allows users to select the detection model and input stream, and monitor results in real time.

---
## Installation
1. **Clone the repository:**
   ```bash
   git clone https://github.com/Adithya2406/Smoke-Detection-from-IP-Camera-Footage-Using-Deep-Learning-and-Neural-Networks.git
   cd Smoke-Detection-from-IP-Camera-Footage-Using-Deep-Learning-and-Neural-Networks
   ```
2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```
3. **Configure alert settings:**  
   Update the configuration files or environment variables for phone, email, and buzzer integration as needed.

---
## Usage
1. **Run the application:**
   ```bash
   streamlit run app.py
   ```
2. The web application will open automatically in your default browser (localhost).
3. Select the detection model: *Smoker Detection* or *Smoke Detection*.
4. Choose your video input: *Webcam* or *RTSP* stream.
5. Monitor the live detection results and receive alerts upon detection.

---
## Application
- **Fire safety monitoring** in factories, warehouses, and public buildings
- **Early warning systems** for residential and commercial complexes
- **Surveillance** in smoke-free zones and public transport
- **Industrial process monitoring** to detect hazardous emissions

---
## Alerts & Notifications
On detecting smoke or a smoker, the system can automatically:
- Make a phone call to a designated number
- Activate a buzzer for local alerts
- Send an email with an image attachment of the detected event

---
## Requirements
- Python 3.7+
- Streamlit
- OpenCV
- Deep learning frameworks (e.g., TensorFlow, PyTorch)

---
## Contributing
Pull requests are welcome! For major changes, please open an issue first to discuss your ideas.

---
## License
This project is licensed under the MIT License.

---
*For questions or support, please raise an issue on the repository.*
---

![image](https://github.com/OmkarDaivajna/Smoke_Detection/assets/117528879/4dc0e113-fd9b-44bd-9a8c-a1e8d187e334)

