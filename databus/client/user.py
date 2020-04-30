""" Module for web users """
import uuid


class Credential: # pylint: disable=R0903
    """ Class defining a user credential """
    def __init__(self, username: str = "Guest", password: str = "", token: str = ""):
        self.username = username
        self.password = password
        self.token = token

    def generate_token(self):
        """ Generates and assigns a new token """
        self.token = str(uuid.uuid1())


class User: # pylint: disable=R0903
    """ Class defining a web user """
    def __init__(self, credential: Credential = None):
        if credential is None:
            self.credential = Credential()
        else:
            self.credential = credential

    def authenticate(self, credential: Credential) -> bool:
        """ Checks if the user & password matches """
        if credential.username != self.credential.username:
            return False
        if credential.password != "" and credential.password == self.credential.password:
            return True
        if credential.token != "" and credential.token == self.credential.token:
            return True
        return False
