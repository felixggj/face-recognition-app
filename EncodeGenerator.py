import os
import cv2
import face_recognition
import pickle
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
from firebase_admin import storage

cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://realtimefacerecognition-cf9b7-default-rtdb.europe-west1.firebasedatabase.app/',
    'storageBucket': 'realtimefacerecognition-cf9b7.appspot.com'
})


# Import student images
folderPath = 'images'
pathList = os.listdir(folderPath)
print(pathList)
imgList= []
studentIds = []
for path in pathList:
    imgList.append(cv2.imread(os.path.join(folderPath, path)))
    studentIds.append(os.path.splitext(path)[0]) # separates ending format from path in order to keep only the name

    # Create a folder called images in the storage bucket inside firebase and upload all images there
    fileName = os.path.join(folderPath, path) 
    bucket = storage.bucket()
    blob = bucket.blob(fileName)
    blob.upload_from_filename(fileName)

    # print(os.path.splitext(path))
    # print(os.path.splitext(path))
print(studentIds)

# Encoding all images at once
def findEncodings(imagesList):
    encodeList = []
    for img in imgList:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB) # convert to RGB
        encode = face_recognition.face_encodings(img)[0] # encode the first face found
        encodeList.append(encode)
    return encodeList

print('Encoding Started ...')
encodeListKnown = findEncodings(imgList)
encodeListKnownWithIds = [encodeListKnown,studentIds]
print('Encoding Complete')

file = open('EncodeFile.p', 'wb')
pickle.dump(encodeListKnownWithIds, file)
file.close()
print('File Saved')