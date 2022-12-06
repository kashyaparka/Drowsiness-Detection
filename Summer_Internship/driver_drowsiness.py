#Importing OpenCV Library for basic image processing functions
import cv2
# Numpy for array related functions
import numpy as np
# Dlib for deep learning based Modules and face landmark detection
import dlib
import winsound
#face_utils for basic operations of conversion
from imutils import face_utils


#Initializing the camera and taking the instance
cap = cv2.VideoCapture(0)
freq = 440
duration = 1000
#Initializing the face detector and landmark detector
detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")

#user_status marking for current state
sleepy_state = 0
drowsy_state = 0
active_state = 0
user_status=""
color=(0,0,0)

def blinked_eye(a,b,c,d,e,f):
    vertical = compute(b,d) + compute(c,e)
    horizontal = compute(a,f)
    ratio = vertical/(2.0*horizontal)

    #Checking if it is blinked_eye
    if(ratio>0.25):
        return 2
    elif(ratio>0.21 and ratio<=0.25):
        return 1
    else:
        return 0


def compute(ptA,ptB):
    distance = np.linalg.norm(ptA - ptB)
    return distance

while True:
    _, frame = cap.read()
    face_frame = frame.copy()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    description = "National Institute of Technology SIlchar"
    faces = detector(gray)
    #detected face in faces array
    for face in faces:
        x_coordinate = face.left()
        y_coordinate = face.top()
        x_coordinate_2 = face.right()
        y_coordinate_2 = face.bottom()

        face_frame = frame.copy()
        cv2.rectangle(face_frame, (x_coordinate, y_coordinate), (x_coordinate_2, y_coordinate_2), (0, 255, 0), 2)

        landmarks = predictor(gray, face)
        landmarks = face_utils.shape_to_np(landmarks)

        #The numbers are actually the landmarks which will show eye
        left_eye_blink = blinked_eye(landmarks[36],landmarks[37], 
            landmarks[38], landmarks[41], landmarks[40], landmarks[39])
        right_eye_blink = blinked_eye(landmarks[42],landmarks[43], 
            landmarks[44], landmarks[47], landmarks[46], landmarks[45])
        
        #Now judge what to do for the eye blinks
        if(left_eye_blink==0 or right_eye_blink==0):
            sleepy_state+=1
            drowsy_state=0
            active_state=0
            if(sleepy_state>6):
                user_status="sleepy_stateING !!!"
                color = (255,0,0)
                winsound.Beep(freq,duration)

        elif(left_eye_blink==1 or right_eye_blink==1):
            sleepy_state=0
            active_state=0
            drowsy_state+=1
            if(drowsy_state>6):
                user_status="drowsy_state !"
                color = (0,0,255)

        else:
            drowsy_state=0
            sleepy_state=0
            active_state+=1
            if(active_state>6):
                user_status="active_state :)"
                color = (0,255,0)
            
        cv2.putText(frame, user_status, (450,450), cv2.FONT_HERSHEY_SIMPLEX, 1.2, color,3)

        for n in range(0, 68):
            (x,y) = landmarks[n]
            cv2.circle(face_frame, (x, y), 1, (255, 255, 255), -1)
    cv2.putText(frame, "Driver Drowsiness Detection", (30,30), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (255,255,255),1)
    cv2.putText(frame, "Electrical Engineering Department", (30,50), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (255,255,255),1)
    cv2.putText(frame, description, (30,70), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (255,255,255),1)
    cv2.putText(frame, "Under the supervision of the Dr. Risha Mal,Asist. Prof", (30,450), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (255,255,255),1)
    cv2.imshow("Frame", frame)
    cv2.imshow("Result of detector", face_frame)
    key = cv2.waitKey(1)
    if key == 27:
          break