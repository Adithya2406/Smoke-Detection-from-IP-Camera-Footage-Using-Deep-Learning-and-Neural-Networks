from twilio.rest import Client
import smtplib
from ultralytics import YOLO
import time
import streamlit as st
import cv2
from pytube import YouTube
import tempfile

from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart

import settings

from PIL import Image

import winsound
frequency = 2000
duration = 2000

account_sid = ''
auth_token = ''
client = Client(account_sid, auth_token)


def load_model(model_path):
    model = YOLO(model_path)
    return model


def display_tracker_options():
    display_tracker = 'Yes'
    # display_tracker = st.radio("Display Tracker", ('Yes', 'No'))
    is_display_tracker = True if display_tracker == 'Yes' else False
    if is_display_tracker:
        tracker_type = 'bytetrack.yaml'
        # tracker_type = st.radio("Tracker", ("bytetrack.yaml", "botsort.yaml"))
        return is_display_tracker, tracker_type
    return is_display_tracker, None
    
def play_rtsp_stream(conf, model,model_type):
    source_rtsp = st.sidebar.text_input("rtsp stream url:")
    st.sidebar.caption('Example URL: rtsp://admin:12345@192.168.1.210:554/Streaming/Channels/101')
    is_display_tracker, tracker = display_tracker_options()
    if st.sidebar.button('Detect Objects'):
        try:
            vid_cap = cv2.VideoCapture(source_rtsp)
            st_frame = st.empty()
            while (vid_cap.isOpened()):
                success, image = vid_cap.read()
                if success:

                    a=_display_detected_frames(conf,
                                             model,
                                             st_frame,
                                             image,
                                             model_type
                                             )
                    if a == False:
                        time.sleep(10)

                else:
                    vid_cap.release()
                    # vid_cap = cv2.VideoCapture(source_rtsp)
                    # time.sleep(0.1)
                    # continue
                    break
        except Exception as e:
            vid_cap.release()
            st.sidebar.error("Error loading RTSP stream: " + str(e))


def play_webcam(conf, model, model_type):
    source_webcam = settings.WEBCAM_PATH
    is_display_tracker, tracker = display_tracker_options()
    if st.sidebar.button('Detect Objects'):
        try:
            vid_cap = cv2.VideoCapture(source_webcam)
            st_frame = st.empty()
            while (vid_cap.isOpened()):
                success, image = vid_cap.read()
                if success:
                    a = _display_detected_frames(conf,
                                            model,
                                            st_frame,
                                            image,
                                            model_type
                                            )
                    if a == False:
                        time.sleep(10)
                        break
                else:
                    vid_cap.release()
                    break
        except Exception as e:
            st.sidebar.error("Error loading video:"+str(e))


def _display_detected_frames(conf, model, st_frame, image, model_type):
    # Resize the image to a standard size
    image = cv2.resize(image, (720, int(720 * (9 / 16))))

    # Predict the objects in the image using YOLOv8 model
    res = model.predict(image, conf=conf)

    boxes = res[0].boxes
    res_plotted = res[0].plot()[:, :, ::-1]
    st.image(res_plotted, caption='Detected Image',
                use_column_width=True)
    try:
        with st.expander("Detection Results"):
            for box in boxes:
                #st.write(box.data)
                box_no_data = box.cls
                st.write(box_no_data.item())
                if box_no_data.item() == 0.0:
                    class_name = "Smoker"
                    st.write(class_name)
                    is_success, im_buf_arr = cv2.imencode(".jpg", res_plotted)
                    byte_im = im_buf_arr.tobytes()

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
                    image2 = MIMEImage(byte_im, name="Smoker.jpg")
                    msg.attach(image2)

                    # Get Gmail credentials securely
                    gmail_user = ""
                    gmail_password = ""

                    # Connect to Gmail's SMTP server
                    with smtplib.SMTP('smtp.gmail.com', 587) as server:
                        server.starttls()  # Enable TLS encryption

                        # Log in to your Gmail account
                        server.login(gmail_user, gmail_password)

                        # Send the email
                        server.sendmail(sender_email, receiver_email, msg.as_string())

                    print('Email sent successfully!')

                    winsound.Beep(frequency,duration)

                    if model_type=='Smoke Detection':
                        call = client.calls.create(
                                        twiml='<Response><Say>Alert, Smoke or Fire detected in your premises!</Say></Response>',
                                        to="", 
    					                from_="",
                                    )
                    return False
                    img = st.image(res_plotted, caption='Detected Image',use_column_width=True)
                      
    except Exception as ex:
                    # st.write(ex)
                    st.write("No image is uploaded yet!")

    # Plot the detected objects on the video frame
    res_plotted = res[0].plot()
    # st.write(res_plotted.item())
    st_frame.image(res_plotted,
                   caption='Detected Video',
                   channels="BGR",
                   use_column_width=True
                   )

# def play_stored_video(conf, model,model_type):
#     source_vid = st.sidebar.selectbox(
#         "Choose a video...", settings.VIDEOS_DICT.keys())

#     is_display_tracker, tracker = display_tracker_options()

#     with open(settings.VIDEOS_DICT.get(source_vid), 'rb') as video_file:
#         video_bytes = video_file.read()
#     if video_bytes:
#         st.video(video_bytes)

#     if st.sidebar.button('Detect Video Objects'):
#         try:
#             vid_cap = cv2.VideoCapture(
#                 str(settings.VIDEOS_DICT.get(source_vid)))
#             st_frame = st.empty()
#             while (vid_cap.isOpened()):
#                 success, image = vid_cap.read()
#                 # cv2.imshow(image, "image")
#                 if success:  
#                     a = _display_detected_frames(conf,
#                                             model,
#                                             st_frame,
#                                             image,
#                                             model_type
#                                             )
#                     if a == False:
#                         time.sleep(10)
#                         vid_cap.set(cv2.CAP_PROP_POS_FRAMES, vid_cap.get(cv2.CAP_PROP_POS_FRAMES)+50)
#                         continue
#                 else:
#                     vid_cap.release()
#                     break
#         except Exception as e:
#             st.sidebar.error("Error loading video:"+str(e))