import pyrebase


class FireBase:
    CONFIG = {
        "apiKey": "AIzaSyAJicw_QoLjfGwxRCHIFppokntxxah2u8o",
        "authDomain": "temp-e485a.firebaseapp.com",
        "projectId": "temp-e485a",
        "databaseURL": "https://temp-e485a-default-rtdb.firebaseio.com",
        "storageBucket": "temp-e485a.appspot.com",
        "messagingSenderId": "442853741112",
        "appId": "1:442853741112:web:96a2d2d05c8c9281ad0ccd",
        "measurementId": "G-RL4F9V6RSP"
    }

    def __init__(self):
        self.firebase = pyrebase.initialize_app(FireBase.CONFIG)
        self.auth = self.firebase.auth()
        self.db = self.firebase.database()
        self.user = None

    def upload_to_db(self, data):
        """
        Uploads data to firebase database
        :param data = {
                        "id": Collection Report Name,
                        "devices": {
                            device_name : device_status
                            }
                        }
        """
        print("Pushing data to database...")
        try:
            self.db.child('reports')\
                .child(self.user['userId'])\
                .child(data['id'])\
                .set(data['devices'])
            return True
        except Exception as e:
            print(e)
            print(data)
            return False

    def create_user(self, email, password):
        print("Creating User with email: " + email + " and password: " + password)
        try:
            self.auth.create_user_with_email_and_password(email, password)
            return True
        except Exception as e:
            print(e)
            return False

    def signin_user(self, email, password):
        print("Signing in User with email: " + email + " and password: " + password)
        try:
            self.auth.sign_in_with_email_and_password(email, password)
            self.user = self.auth.current_user
            return True
        except Exception as e:
            print(e)
            return False

    def signout_user(self):
        print("Signing out User")
        try:
            self.auth.current_user = None
            self.user = None
            return True
        except Exception as e:
            print(e)
            return False

    def get_user(self):
        return self.user

    def refresh_session(self):
        print("Refreshing session...")
        try:
            self.user = self.auth.refresh(self.user['refreshToken'])
            return True
        except Exception as e:
            print(e)
            return False
