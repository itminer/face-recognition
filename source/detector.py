import os
import cv2
import time
import datetime
import face_recognition
import source.database as db

# init data
EMPLOYEE_ATTENDENT = []
EMPLOYEE_NAMES = []
EMPLOYEE_FACE_ENCODINGS = []

# Function load data from db
def loadInfo():
    data = []
    data = db.getinfo()
    for item in data:
        EMPLOYEE_NAMES.append(item['name'])
        EMPLOYEE_FACE_ENCODINGS.append(item['encoding'])
    print(EMPLOYEE_NAMES, EMPLOYEE_FACE_ENCODINGS)

# Function load data from model folder
def loadInfo1(url):
    data = []
    for (dirpath, dirnames, filenames) in os.walk(url):
        data = filenames
    for item in data:
        image = face_recognition.load_image_file(os.path.join(url, item))
        encoding = face_recognition.face_encodings(image)
        if encoding:
            EMPLOYEE_NAMES.append(item)
            EMPLOYEE_FACE_ENCODINGS.append(encoding[0])
    print(EMPLOYEE_NAMES, EMPLOYEE_FACE_ENCODINGS)

# recognition face
def detector(frame, UnknownPath):
    rgb_frame = frame[:, :, ::-1]
    face_area = face_recognition.face_locations(rgb_frame)
    face_encodings = face_recognition.face_encodings(rgb_frame, face_area)
    face_names = []

    for face_encoding in face_encodings:
        # See if the face is a match for the known face(s)
        matches = face_recognition.compare_faces(EMPLOYEE_FACE_ENCODINGS, face_encoding)
        name = "Unknown"
        # If a match was found in known_face_encodings, just use the first one.
        if True in matches:
            match_index = matches.index(True)
            name = EMPLOYEE_NAMES[match_index]

        face_names.append(name)
        if not name in EMPLOYEE_ATTENDENT and name != 'Unknown':
            #EMPLOYEE_ATTENDENT.append(name)
            db.insert(name.replace('.jpg',''))
        elif name == 'Unknown':
            st = datetime.datetime.fromtimestamp(time.time()).strftime('%Y%m%d_%H_%M_%S')
            cv2.imwrite(UnknownPath+name+st+'.jpg', frame)

    # Display the results
    for (top, right, bottom, left), name in zip(face_area, face_names):
         # Draw a label with a name below the face
        if name == "Unknown":
            cv2.rectangle(frame, (left, top), (right, bottom), (255, 0, 0), 2)
        else:
            # Draw a box around the face
            cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)

        # Draw a label with a name below the face
        cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
        font = cv2.FONT_HERSHEY_DUPLEX
        cv2.putText(frame, name.replace('.jpg',''), (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)

    # return frame
