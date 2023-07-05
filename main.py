import os
import cv2
import numpy as np

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



while True:
    success, img = cap.read()

    imgBackground[162:162+480,55:55+640] = img
    imgBackground[44:44+633,808:808+414] = imgModeList[1]


    #cv2.imshow("Webcam", img)
    cv2.imshow("Face Attendance", imgBackground)
    if cv2.waitKey(1) & 0xFF == ord('q'):  # break loop on 'q' key press
        break

cap.release()
cv2.destroyAllWindows()


