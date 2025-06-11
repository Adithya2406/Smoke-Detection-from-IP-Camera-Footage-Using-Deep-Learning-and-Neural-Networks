# Python In-built packages
from pathlib import Path
import PIL
import torch
from twilio.rest import Client

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from getpass import getpass


# External packages
import streamlit as st

# Local Modules
import settings
import helper
import winsound
frequency = 2000
duration = 4000

account_sid = ''
auth_token = ''
client = Client(account_sid, auth_token)


# Setting page layout
st.set_page_config(
    page_title="Smoker / Smoke Detection using YOLOv8",
    page_icon="🚬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Main page heading
st.title("Smoker / Smoke Detection using YOLOv8")

# Model Options
model_type = st.sidebar.selectbox(
    "Select Task...", ('Smoker Detection','Smoke Detection'))

confidence = 0.40
# confidence = float(st.sidebar.slider(
#     "Select Model Confidence", 40, 40, 40)) / 100

# Selecting Detection Or Segmentation
if model_type == 'Smoke Detection':
    model_path = Path(settings.DETECTION_MODEL)
elif model_type == 'Smoker Detection':
    model_path = Path(settings.SEGMENTATION_MODEL)

# Load Pre-trained ML Model
try:
    model = helper.load_model(model_path)
except Exception as ex:
    st.error(f"Unable to load model. Check the specified path: {model_path}")
    st.error(ex)

st.sidebar.header("Image/Video Input Source")
source_radio = st.sidebar.selectbox(
    "Select Source", settings.SOURCES_LIST)

 source_img = None
 if source_radio == settings.IMAGE:
     source_img = st.sidebar.file_uploader(
         "Choose an image...", type=("jpg", "jpeg", "png", 'bmp', 'webp'))

     col1, col2 = st.columns(2)

     with col1:
         try:
             uploaded_image = PIL.Image.open(source_img)
             st.image(source_img, caption="Uploaded Image",
                         use_column_width=True)
         except Exception as ex:
             st.error("Error occurred while opening the image.")
             st.error(ex)

     with col2:
         if st.sidebar.button('Detect Objects'):
             res = model.predict(uploaded_image,
                                 conf=confidence
                                 )
              st.write(res[0].names)
            
             boxes = res[0].boxes
             res_plotted = res[0].plot()[:, :, ::-1]
             st.image(res_plotted, caption='Detected Image',
                         use_column_width=True)
             try:
                 with st.expander("Detection Results"):
                     for box in boxes:
                         st.write(box.data)
                         box_no_data = box.cls
                         st.write(box_no_data.item())

                         if model_type == 'Smoker Detection': 
                             if box_no_data.item() == 0.0:
                                 class_name = "Smoker"
                                 st.write(class_name)
                                 winsound.Beep(frequency,duration)
                                 img = st.image(res_plotted, caption='Detected Image',use_column_width=True)
                                 st.image(img)

                         if model_type == 'Smoke Detection': 
                             if box_no_data.item() == 0.0:
                                 class_name = "Fire"
                                 st.write(class_name)
                                 winsound.Beep(frequency,duration)
                                 img = st.image(res_plotted, caption='Detected Image',use_column_width=True)

                                 sender_email = ''
                                 receiver_email = ''
                                 if model_type=='Smoker Detection':
                                     subject = 'Alert, Someone is smoking near your area!'
                                 else:
                                     subject = "Alert, Fire or smoke detected!"
                                 message = 'PLease check it ASAP'
                                 # Create a MIMEText object for the email content
                                 msg = MIMEMultipart()
                                 msg['From'] = sender_email
                                 msg['To'] = receiver_email
                                 msg['Subject'] = subject

                                 # Attach the message to the email
                                 msg.attach(MIMEText(message, 'plain'))
                                 gmail_user = ""
                                 gmail_password = ""

                                 # Connect to Gmail's SMTP server
                                 with smtplib.SMTP('smtp.gmail.com', 587) as server:
                                     server.starttls()  # Enable TLS encryption

                                     # Log in to your Gmail account
                                     server.login(gmail_user, gmail_password)

                                     # Send the email
                                     server.sendmail(sender_email, receiver_email, msg.as_string())

                                 print('Email sent successfully!')
                                

                                 call = client.calls.create(
                                     twiml='<Response><Say>Fire Fire Fire.</Say></Response>',
                                     to="", 
                                     from_="",
                                 )
                                 st.image(img)
                               
                             if box_no_data.item() == 1.0:
                                 class_name = "Smoke"
                                 st.write(class_name)
                                 winsound.Beep(frequency,duration)
                                 img = st.image(res_plotted, caption='Detected Image',use_column_width=True)
                                 sender_email = ''
                                 receiver_email = ''
                                 if model_type=='Smoker Detection':
                                     subject = 'Alert, Someone is smoking near your area!'
                                 else:
                                     subject = "Alert, Fire or smoke detected!"
                                 message = 'PLease check it ASAP'
                                 # Create a MIMEText object for the email content
                                 msg = MIMEMultipart()
                                 msg['From'] = sender_email
                                 msg['To'] = receiver_email
                                 msg['Subject'] = subject

                                 # Attach the message to the email
                                  msg.attach(MIMEText(message, 'plain'))
                                  image2 = MIMEImage()
                                  msg.attach(image2)
#                                  Get Gmail credentials securely
                                 gmail_user = ""
                                 gmail_password = ""

                                 # Connect to Gmail's SMTP server
                                 with smtplib.SMTP('smtp.gmail.com', 587) as server:
                                     server.starttls()  # Enable TLS encryption

                                     # Log in to your Gmail account
                                     server.login(gmail_user, gmail_password)

                                     # Send the email
                                     server.sendmail(sender_email, receiver_email, msg.as_string())

                                 print('Email sent successfully!')
                                 call = client.calls.create(
                                     twiml='<Response><Say>Smoke Smoke Smoke</Say></Response>',
                                     to="", 
                                     from_="",
                                 )
                 st.image(img)   
             except Exception as ex:
                 # st.write(ex)
                 st.write("No image is uploaded yet!")

 elif source_radio == settings.VIDEO:
     helper.play_stored_video(confidence, model, model_type)

if source_radio == settings.WEBCAM:
    helper.play_webcam(confidence, model, model_type)

elif source_radio == settings.RTSP:
    helper.play_rtsp_stream(confidence, model, model_type)

else:
    st.error("Please select a valid source type!")
