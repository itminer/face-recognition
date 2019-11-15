import os
import cv2
import win32api
import threading
import numpy as np
import face_recognition
import source.database as db
import source.detector as dt

# keycode
KeyEsc   = 27   # ESC 
KeySpace = 32   # Space 

# model path
ModelPath = os.path.dirname(os.path.abspath('__file__')) + '/model/employee'
UnknownPath = os.path.dirname(os.path.abspath('__file__')) + '/model/unknown/'

# Function to check whether file exist
def isExistFile(filename):
    return os.path.isfile(os.path.join(ModelPath, filename))

# Function to check whether folder exist
def isExistFolder(dirName):
    if not os.path.exists(dirName):
        os.mkdir(dirName)

# Function to check database connection
def isConnectDB():
    print("isConnectDB")
    if (db.connect()):
        print("DB connected")
    else:
        win32api.MessageBox(0,"DB connect failed.","Notice")
        return

# Function to open camera
def connectCam(index, cam):
    print("Start Thread" + str(index))
    cam.set(3, 320)
    cam.set(4, 240)
    # connect camera, alert message if no camera device.
    if cam.isOpened():
        isRun, frame = cam.read()
    else:
        isRun = False
        win32api.MessageBox(0,"Please connect camera.","Notice")
    # action onwhile the camera connected
    while isRun:
        isRun, frame = cam.read()
        dt.detector(frame, UnknownPath) 
        cv2.imshow("Face Recognition - camera" + str(index), frame)
        key = cv2.waitKey(20)
    
        if key == KeyEsc:  
            cam.release()
            isRun = False

    cv2.waitKey(0)
    cv2.destroyAllWindows()

def run():
    # if model folder not exist, make the folder
    isExistFolder(ModelPath)
    # check db connection
    isConnectDB()
    # load face data
    dt.loadInfo1(ModelPath)
    # connect camera
    ip = ''
    cam1 = cv2.VideoCapture(cv2.CAP_DSHOW)
    # cam2 = cv2.VideoCapture(1+cv2.CAP_DSHOW)
    # thread = [cam1, cam2]
    # index = 1
    # for cam in thread:
    #     tr = threading.Thread(target=connectCam, args=(index, cam, ))
    #     # tr.daemon = True
    #     tr.start()
    #     index += 1
    connectCam(1, cam1)


if __name__ == "__main__":
    run()