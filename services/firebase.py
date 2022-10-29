import pyrebase
import os

class Firebase:
    def __init__(self):
        config = {
            "apiKey": os.environ['FIREBASE_API_KEY'],
            "authDomain": "alivenevada.firebaseapp.com",
            "databaseURL": "https://alivenevada-default-rtdb.firebaseio.com",
            "storageBucket": "alivenevada.appspot.com"
        }

        self.firebase = pyrebase.initialize_app(config)

    def login(self, email, password):
        self.auth = self.firebase.auth()
        self.user = self.auth.sign_in_with_email_and_password(email, password)
        self.db = self.firebase.database()
        self.storage = self.firebase.storage()
    
    def register(self, email, password):
        self.auth = self.firebase.auth()
        self.user = self.auth.create_user_with_email_and_password(email, password)
        self.db = self.firebase.database()
        self.storage = self.firebase.storage()

    def login_token(self, token):
        self.auth = self.firebase.auth()
        self.user = self.auth.refresh(token)
        self.db = self.firebase.database()
        self.storage = self.firebase.storage()
