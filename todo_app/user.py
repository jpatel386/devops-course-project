import flask_login

class User(flask_login.UserMixin):

    def __init__(self, id):
        self.id = id
        self.role = "reader"
        # By default everybody is a reader unless the github ID is mine - Could turn this into an env var/array/DB we read from
        if id == "18398852": 
            self.role = "writer"
        
