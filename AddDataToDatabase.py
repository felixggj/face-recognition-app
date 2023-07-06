import firebase_admin
from firebase_admin import credentials
from firebase_admin import db

cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://realtimefacerecognition-cf9b7-default-rtdb.europe-west1.firebasedatabase.app/'
})

ref = db.reference('Students') # creates a reference to the database

data = {
    '321654':
        {
            'name': 'Felix GG',
            'degree': 'CS & AI',
            'starting_year': 2021,
            'total_attendance': 11,
            'standing': 'G',
            'year': 3,
            'last_attendance_time': '2023-05-27 10:12:02',

        },

    '852741':
        {
            'name': 'Emily Blunt',
            'degree': 'Economics',
            'starting_year': 2020,
            'total_attendance': 2,
            'standing': 'B',
            'year': 4,
            'last_attendance_time': '2023-04-02 09:04:01',

        },

    '963852':
        {
            'name': 'Elon Musk',
            'degree': 'Physics',
            'starting_year': 2019,
            'total_attendance': 6,
            'standing': 'G',
            'year': 5,
            'last_attendance_time': '2023-06-17 13:17:00',

        },
}

for key, value in data.items():
    ref.child(key).set(value) # sets the value of the key to the value

print("Data added to database")