import cv2
from datetime import datetime
import numpy as np
import time
import os


face_classifier = cv2.CascadeClassifier('Haarcascades/haarcascade_frontalface_default.xml')
eye_classifier = cv2.CascadeClassifier('Haarcascades/haarcascade_eye.xml')


def face_detector(img, size=0.5):
    # Convert image to grayscale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = face_classifier.detectMultiScale(gray, 1.3, 5)
    print('Face value {}'.format(faces))
    if faces is ():
        print ('Driver is missing at {}'.format(datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
        os.system('say "Driver is missing"')
        return img

    for (x, y, w, h) in faces:
        x = x - 50
        w = w + 50
        y = y - 50
        h = h + 50
        cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)
        roi_gray = gray[y:y + h, x:x + w]
        roi_color = img[y:y + h, x:x + w]
        eyes = eye_classifier.detectMultiScale(roi_gray)
        if len(eyes) > 0:
            for (ex, ey, ew, eh) in eyes:
                cv2.rectangle(roi_color, (ex, ey), (ex + ew, ey + eh), (0, 0, 255), 2)
        else:
            print('Driver is sleeping at {}'.format(datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
            os.system('say "Driver is sleeping"')
            exit(0)

    roi_color = cv2.flip(roi_color, 1)
    return roi_color


cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    try:
        cv2.imshow('Driver detetection', face_detector(frame))
        if cv2.waitKey(1) == 13:  # 13 is the Enter Key
            break
    except:
        os.system('say "Fatal Exception"')

cap.release()
cv2.destroyAllWindows()