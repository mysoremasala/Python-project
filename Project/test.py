import pyrebase
from config import firebaseConfig

firebase = pyrebase.initialize_app(config=firebaseConfig)
auth = firebase.auth()
db = firebase.database()
data = {
            "name": "",
            "department": "",
            "position": "",
            "email": "",
            "id": ""
        }

db.child("employee").child("wew22432").set(data)