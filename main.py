from datetime import datetime
import cv2
import numpy as np
import face_recognition as fr
import os
import time
import twilio
from datetime import datetime
import time
import pandas as pd
from twilio.rest import Client


images = []
classNames = []
def addImage():
    global images
    global classNames
    path = 'Favourite_Visitors'
    myList = os.listdir(path)
    for cl in myList:
        currentImg = cv2.imread(f'{path}/{cl}')
        images.append(currentImg)
        classNames.append(os.path.splitext(cl)[0])   
    findEncodings(images)

def endCapture():
    cap.release()
    cv2.destroyAllWindows()

def findEncodings(images):
    imageEncodeList = []

    for img in images:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        encode = fr.face_encodings(img)[0]
        imageEncodeList.append(encode)
    detectFace(imageEncodeList)

def addtoLog(name, timetaken):
    line_number = 0
    now = datetime.now()
    date = datetime.now().date()
    inTime = now.strftime('%H:%M')
    temp_file = open('sample.txt', 'a')
    temp_file.write(f'\n{name},{inTime},{date}')
    temp_file.close()
    with open('sample.txt', 'r') as f:
        unique_lines = set(f.readlines())  
        notEmpty = (len(unique_lines) != 0)
        if notEmpty:
            findUnique(unique_lines,name)            
    addForTesting(name,timetaken,inTime,date)
     
def addForTesting(name,timetaken,date,inTime):
    with open('Testing.csv', 'a') as f: 
            f.writelines(f'\n{name},{inTime},{date},{timetaken}')

def findUnique(unique_liness,name):
    with open('Visitors.txt', 'w') as f:
        f.writelines(unique_liness)
        f.writelines("\n") 
    sendSMS(name)  

def sendSMS(name):
    Accnt_sid = "********************************" 
    Auth_token = "*******************************"
    Twilioclient = Client(Accnt_sid,Auth_token)

    message = Twilioclient.messages \
                .create(
                    body={name + " has arrived at your house"},
                    from_='+18647148223',
                    to='+353894076129'
                )

def detectFace(encodingList):
    global cap
    cap = cv2.VideoCapture(0)

    while True:
        
        success, img = cap.read()
        begin = time.time()
        imgS = cv2.resize(img, (0, 0), None, 0.25, 0.25)
        imgS = cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB)

        currentFaceFrame = fr.face_locations(imgS)
        currentFaceFrameEncoded = fr.face_encodings(imgS, currentFaceFrame)

        for encodeFace, faceLoc in zip(currentFaceFrameEncoded, currentFaceFrame):
            matchings = fr.compare_faces(encodingList, encodeFace)
            distance = fr.face_distance(encodingList, encodeFace)
 
            matchIndex = np.argmin(distance)

            if matchings[matchIndex]:
                name = classNames[matchIndex].upper()
            else:
                name = "UNKNOWN FACE"
            y1, x2, y2, x1 = faceLoc
            y1, x2, y2, x1 = y1 * 4, x2 * 4, y2 * 4, x1 * 4
            cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)
            cv2.rectangle(img, (x1, y2 - 35), (x2, y2), (0, 255, 0), cv2.FILLED)
            cv2.putText(img, name, (x1 + 6, y2 - 6), cv2.FONT_HERSHEY_TRIPLEX, 1, (255, 255, 255), 2)
            end = time.time()
            timetaken = end-begin
            addtoLog(name,timetaken)

        cv2.imshow('Webcam', img)
        cv2.waitKey(1)
