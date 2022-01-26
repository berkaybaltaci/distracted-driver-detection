import cv2
import time
import numpy as np
from keras.preprocessing import image
from keras.models import load_model
import tensorflow as tf
import pyrebase

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders

from threading import Thread
from time import sleep
import os

from send_mail import send_mail

from dotenv import load_dotenv

load_dotenv()

config = {
    "apiKey": os.getenv('apiKey'),
    "authDomain": os.getenv('authDomain'),
    "databaseURL": os.getenv('databaseURL'),
    "projectId": os.getenv('projectId'),
    "storageBucket": os.getenv('storageBucket'),
    "messagingSenderId": os.getenv('messagingSenderId'),
    "appId": os.getenv('appId'),
    "measurementId": os.getenv('measurementId')
}

firebase = pyrebase.initialize_app(config)
db = firebase.database()

model = load_model('320x240_50epochs_fivelayers_fiveclasses_increasedfilters_grafikicin.h5')

temp_obj = {'flag' : False}

def start_mail_thread():
    if (temp_obj["flag"] == False):
        thread = Thread(target=send_mail, args=(temp_obj, ))
        thread.start()

def predict(frame):

    frame = image.img_to_array(frame)

    frame = np.expand_dims(frame, axis=0)
    frame = frame/255

    prediction_prob = model.predict(frame)
    max_indice = np.argmax(prediction_prob)

    temp = ''
    fontColor = (0,0,0)

    if max_indice == 0:
        db.child("myData").update({"guvenlikDurumu": "SAFE DRIVING"})
        temp = (f'SAFE DRIVING {int(prediction_prob[0][max_indice] * 100)}%')
        fontColor = (0,255,0)
            
    elif max_indice == 1:
        db.child("myData").update({"guvenlikDurumu": "TALKING ON THE PHONE (RIGHT HAND) DETECTED"})
        temp = (f'TALKING ON THE PHONE (RIGHT HAND) {int(prediction_prob[0][max_indice] * 100)}%')
        fontColor = (0,0,255)
        start_mail_thread()
    elif max_indice == 2:
        db.child("myData").update({"guvenlikDurumu": "TEXTING (RIGHT HAND) DETECTED"})
        temp = (f'TEXTING (RIGHT HAND) {int(prediction_prob[0][max_indice] * 100)}%')
        fontColor = (0,0,255)
        start_mail_thread()
    elif max_indice == 3:
        db.child("myData").update({"guvenlikDurumu": "TALKING ON THE PHONE (LEFT HAND) DETECTED"})
        temp = (f'TALKING ON THE PHONE (LEFT HAND) {int(prediction_prob[0][max_indice] * 100)}%')
        fontColor = (0,0,255)
        start_mail_thread()
    elif max_indice == 4:
        db.child("myData").update({"guvenlikDurumu": "TEXTING (RIGHT HAND) DETECTED"})
        temp = (f'TEXTING (LEFT HAND) {int(prediction_prob[0][max_indice] * 100)}%')
        fontColor = (0,0,255)
        start_mail_thread()

    print(prediction_prob)
    return (temp, fontColor)

###############################################################################################

# img_name = 'img_58380.jpg'

# dog_file = img_name
# frame = image.load_img(dog_file, target_size=(320, 240))

# (temp, fontColor) = predict(frame)

# img = cv2.imread(img_name)
# cv2.putText(img, text=temp, org=(10, 30), fontFace=cv2.FONT_HERSHEY_SIMPLEX,
#                  fontScale=0.5, color=fontColor, thickness=3, lineType=cv2.LINE_AA)
# cv2.imshow('Ornek Senaryolarin Gerceklenmesi', img)
# cv2.waitKey()


####################################################################################################

cap = cv2.VideoCapture('input_video_orj.mp4')
# cap = cv2.VideoCapture(0)

if (cap.isOpened() == False):
    print('FILE NOT FOUND OR WRONG CODEC USED')


start_time = time.perf_counter()

while cap.isOpened():

    if (time.perf_counter() - start_time > 40):
        os._exit(1)

    print("time ------------")
    print(time.perf_counter())
    print("time ------------")


    ret, frame = cap.read()
    if ret:
        cv2.imwrite('sample.png', frame)
        resized = image.load_img('sample.png', target_size=(320, 240))

        (predictionText, fontColor) = predict(resized)

        cv2.putText(frame, text=predictionText, org=(10, 30), fontFace=cv2.FONT_HERSHEY_SIMPLEX,
                    fontScale=1, color=fontColor, thickness=3, lineType=cv2.LINE_AA)
        cv2.imshow('Testing on a sample video', frame)

        # hit q to exit
        if cv2.waitKey(1) & 0xFF == ord('q'):
            os._exit(1)
    else:
        break

