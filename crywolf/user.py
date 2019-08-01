from flask_login.mixins import UserMixin

class User(UserMixin):
    def __init__(self, fName = None, lName = None):
        self.fName = fName
        self.lName = lName
