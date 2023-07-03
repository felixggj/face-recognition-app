import cv2
import numpy as np

cap = cv2.VideoCapture(0)  # change the index if needed
cap.set(3, 1280)
cap.set(4, 720)

while True:
    success, img = cap.read()
    if not success:
        break
    cv2.imshow("Face Attendance", img)
    if cv2.waitKey(1) & 0xFF == ord('q'):  # break loop on 'q' key press
        break

cap.release()
cv2.destroyAllWindows()


