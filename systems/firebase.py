import pyrebase


class FireBase:
    CONFIG = {
        "apiKey": "AIzaSyDoBEoypPjsbvU-n3-b_30Xw_P2Z6x3rAU",
        "authDomain": "spyot-56f6e.firebaseapp.com",
        "databaseURL": "https://spyot-56f6e-default-rtdb.firebaseio.com",
        "projectId": "spyot-56f6e",
        "storageBucket": "spyot-56f6e.appspot.com",
        "messagingSenderId": "869272684117",
        "appId": "1:869272684117:web:4d4051a4b506f2f2eef6dc",
        "measurementId": "G-YW1WX5YERW"
    }

    def __init__(self):
        self.firebase = pyrebase.initialize_app(FireBase.CONFIG)
        self.auth = self.firebase.auth()
        self.db = self.firebase.database()
        self.user = None

    def upload_to_db(self, data):
        """
        Uploads data to firebase database
        :param
        data = {
                "id": Collection Report Name,
                    device_name: {
                        "ip": device_ip,
                        "mac": device_mac,
                        "status": secure
                        "ports": {
                                    "port23": state,
                                    "port80": state,
                                    "port2323": state,
                                }
                        }, ...
                }
        """
        print("Pushing data to database...")
        try:
            for device_name in {key for key in data.keys() if key != 'id'}:
                non_port_data = {key: data[device_name][key] for key in data[device_name].keys() if key != 'ports'}
                user_report_ref = self.db.child('users').child(self.user['userId']).child(data['id'])
                user_report_ref.child(device_name).set(non_port_data)
                port_data = {key: data[device_name]['ports'][key] for key in data[device_name]['ports']}
                user_report_ref = self.db.child('users').child(self.user['userId']).child(data['id'])
                user_report_ref.child(device_name).child('ports').set(port_data)
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
