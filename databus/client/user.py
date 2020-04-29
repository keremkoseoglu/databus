""" Module for web users """


class Credential: # pylint: disable=R0903
    """ Class defining a user credential """
    def __init__(self, username: str = "Guest", password: str = ""):
        self.username = username
        self.password = password


class User: # pylint: disable=R0903
    """ Class defining a web user """
    def __init__(self, credential: Credential = None):
        if credential is None:
            self.credential = Credential()
        else:
            self.credential = credential

    def authenticate(self, credential: Credential) -> bool:
        """ Checks if the user & password matches """
        return \
            credential.username == self.credential.username and \
            credential.password == self.credential.password
