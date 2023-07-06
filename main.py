import os
import cv2
import pickle
import numpy as np
import face_recognition
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
from firebase_admin import storage

cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://realtimefacerecognition-cf9b7-default-rtdb.europe-west1.firebasedatabase.app/',
    'storageBucket': 'realtimefacerecognition-cf9b7.appspot.com'
})

bucket = storage.bucket()

cap = cv2.VideoCapture(0)  # change the index if needed
cap.set(3, 640)
cap.set(4, 480)

imgBackground = cv2.imread('resources/background.png')

# Importing the mode images into a list
folderModePath = 'resources/modes'
modePathList = os.listdir(folderModePath)
imgModeList= []
for path in modePathList:
    imgModeList.append(cv2.imread(os.path.join(folderModePath, path)))


# Loading the encoded file containing the three encoded versions of the images
print('Loading Encoded File ...')
file = open('EncodeFile.p', 'rb')
encodeListKnownWithIds = pickle.load(file)
file.close()
encodeListKnown, studentIds = encodeListKnownWithIds
#print(studentIds)
print('Encoded File Loaded')

modeType = 0
counter = 0
id = -1
imgStudent = []


while True:
    success, img = cap.read()

    imgS = cv2.resize(img, (0, 0), None, 0.25, 0.25)  # resize to 1/4 of the original size
    imgS = cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB)  # convert to RGB

    faceCurFrame = face_recognition.face_locations(imgS)  # find the face in the current frame
    encodeCurFrame = face_recognition.face_encodings(imgS, faceCurFrame)  # encode the face in the current frame

    imgBackground[162:162+480,55:55+640] = img
    imgBackground[44:44+633,808:808+414] = imgModeList[modeType]

    for encodeFace, faceLoc in zip(encodeCurFrame, faceCurFrame):
        matches = face_recognition.compare_faces(encodeListKnown, encodeFace)  # compare the current face with the known faces
        faceDis = face_recognition.face_distance(encodeListKnown, encodeFace)  # calculate the distance between the current face and the known faces
        # print('matches', matches)
        # print('faceDis', faceDis)

        matchIndex = np.argmin(faceDis)  # find the index of the minimum distance
        # print('matchIndex', matchIndex)

        if matches[matchIndex]:
            # print("Known Face Detected")
            # print(studentIds[matchIndex])
            top, right, bottom, left = faceLoc
            top *= 4
            right *= 4
            bottom *= 4
            left *= 4
            bbox = 55 + left, 162 + top, right - left, bottom - top  # create a bounding box using cv2
            bbox_start = (bbox[0], bbox[1])
            bbox_end = (bbox[0]+bbox[2], bbox[1]+bbox[3])

            # Draw the rectangle on the image
            imgBackground = cv2.rectangle(imgBackground, bbox_start, bbox_end, (0, 0, 255), 2)
            id = studentIds[matchIndex]
            
            if counter == 0:
                counter = 1
                modeType = 1

    if counter != 0:

        if counter == 1:
            # Getting the data
            studentInfo = db.reference(f'Students/{id}').get()
            print(studentInfo)
            # Getting the image from the storage
            blob = bucket.get_blob(f'images/{id}.png')
            array = np.frombuffer(blob.download_as_string(), np.uint8)
            imgStudent = cv2.imdecode(array, cv2.COLOR_BGRA2BGR)

        # Displaying the student info on the screen

        cv2.putText(imgBackground, str(studentInfo['total_attendance']), (861, 125),
                    cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 1)
        
        cv2.putText(imgBackground, str(studentInfo['degree']), (1006, 550),
                    cv2.FONT_HERSHEY_COMPLEX, 0.5, (255, 255, 255), 1)
        
        cv2.putText(imgBackground, str(id), (1006, 493),
                    cv2.FONT_HERSHEY_COMPLEX, 0.5, (255, 255, 255), 1)
        
        cv2.putText(imgBackground, str(studentInfo['standing']), (910, 625),
                    cv2.FONT_HERSHEY_COMPLEX, 0.6, (100, 100, 100), 1)
        
        cv2.putText(imgBackground, str(studentInfo['year']), (1025, 625),
                    cv2.FONT_HERSHEY_COMPLEX, 0.6, (100, 100, 100), 1)
        
        cv2.putText(imgBackground, str(studentInfo['starting_year']), (1125, 625),
                    cv2.FONT_HERSHEY_COMPLEX, 0.6, (100, 100, 100), 1)
        

        # Adapting the name so that it centers on the screen automatically

        (w, h), _ = cv2.getTextSize(studentInfo['name'], cv2.FONT_HERSHEY_COMPLEX, 1, 1)
        offset = (414 - w) // 2
        cv2.putText(imgBackground, str(studentInfo['name']), (808+offset, 445),
                    cv2.FONT_HERSHEY_COMPLEX, 1, (50, 50, 50), 1)
        
        imgBackground[175:175+216,907:907+216] = imgStudent
        
        counter += 1

    cv2.imshow("Face Attendance", imgBackground)
    if cv2.waitKey(1) & 0xFF == ord('q'):  # break loop on 'q' key press
        break

cap.release()
cv2.destroyAllWindows()


