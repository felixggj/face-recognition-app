# Face Recognition Attendance System | Felix GG

This project presents a real-time face recognition system using OpenCV and Firebase as the database. Faces are detected and recognized in real-time and attendance is tracked and updated in the database. The system uses Firebase for real-time data tracking, storage, and retrieval. This repository is complete with a `.yml` file to easily set up a new environment.

## Features

- Real-time face detection and recognition using `face_recognition` and `cv2`
- Attendance is tracked and updated in real-time on Firebase
- Student information and image are retrieved from Firebase

## How it works

The system captures images from the webcam, detects faces, and recognizes them. If the recognized face matches a known student, their attendance information is retrieved and updated in the Firebase database.

It will also show a live feed of the webcam with the recognized faces highlighted and labeled, with all their respective information displayed along with customized background graphics.

## Setup

- Firstly, clone the repository to your local machine:
  `https://github.com/felixggj/face-recognition-app.git`

- To create a new environment using the `.yml` file, navigate to the directory where the `environment.yml` file is located and use the following command:

```conda env create -f environment.yml````

- Activate the environment using:

`conda activate face-recognition`

Before running the project, you will need to replace `serviceAccountKey.json` with your own Firebase project's service account key file and replace the databaseURL and storageBucket in the Firebase configuration.

## Run the project

To run the main script, navigate to the project's directory and use the following command:

`python main.py`
