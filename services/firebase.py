import pyrebase

class Firebase:
    def __init__(self):
        config = {
            "apiKey": "AIzaSyCmgIMegl9Qg_wKEw0-ZE3FiZ8kxnLiaII",
            "authDomain": "alivenevada.firebaseapp.com",
            "databaseURL": "https://alivenevada-default-rtdb.firebaseio.com",
            "storageBucket": "alivenevada.appspot.com"
        }

        self.firebase = pyrebase.initialize_app(config)

    def login(self, email, password):
        self.auth = self.firebase.auth()
        self.user = self.auth.sign_in_with_email_and_password(email, password)
        self.db = self.firebase.database()
    
    def register(self, email, password):
        self.auth = self.firebase.auth()
        self.user = self.auth.create_user_with_email_and_password(email, password)
        self.db = self.firebase.database()

    def login_token(self, token):
        self.auth = self.firebase.auth()
        self.user = self.auth.refresh(token)
        self.db = self.firebase.database()

