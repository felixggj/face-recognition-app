import os
import cv2
import pickle
import numpy as np
import face_recognition

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


while True:
    success, img = cap.read()

    imgS = cv2.resize(img, (0, 0), None, 0.25, 0.25)  # resize to 1/4 of the original size
    imgS = cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB)  # convert to RGB

    faceCurFrame = face_recognition.face_locations(imgS)  # find the face in the current frame
    encodeCurFrame = face_recognition.face_encodings(imgS, faceCurFrame)  # encode the face in the current frame

    imgBackground[162:162+480,55:55+640] = img
    imgBackground[44:44+633,808:808+414] = imgModeList[1]

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
            bbox = 55 + left, 162 + top, right - left, bottom - top  # create a bounding box
            bbox_start = (bbox[0], bbox[1])
            bbox_end = (bbox[0]+bbox[2], bbox[1]+bbox[3])

            # Draw the rectangle on the image
            imgBackground = cv2.rectangle(imgBackground, bbox_start, bbox_end, (0, 0, 255), 2)
            

    #cv2.imshow("Webcam", img)
    cv2.imshow("Face Attendance", imgBackground)
    if cv2.waitKey(1) & 0xFF == ord('q'):  # break loop on 'q' key press
        break

cap.release()
cv2.destroyAllWindows()


