""" Module for web users """
import uuid
from enum import Enum


class Credential: # pylint: disable=R0903
    """ Class defining a user credential """
    def __init__(self, username: str = "Guest", password: str = "", token: str = ""):
        self.username = username
        self.password = password
        self.token = token

    def generate_token(self):
        """ Generates and assigns a new token """
        self.token = str(uuid.uuid1())


class Role(Enum):
    """ Defines the role of the user within the system """
    UNDEFINED = 0
    OPERATOR = 1
    ADMINISTRATOR = 2


def str_to_role(role: str) -> Role:
    """ Converts a text based role value to role enum """
    up_role = role.upper()
    for role_enum in Role:
        if role_enum.name == up_role:
            return role_enum
    return Role.UNDEFINED


class User: # pylint: disable=R0903
    """ Class defining a web user """
    def __init__(self, credential: Credential = None, role: Role = Role.OPERATOR):
        if credential is None:
            self.credential = Credential()
        else:
            self.credential = credential

        if role == Role.UNDEFINED:
            self.role = Role.OPERATOR
        else:
            self.role = role

    def authenticate(self, credential: Credential) -> bool:
        """ Checks if the user & password matches """
        if credential.username != self.credential.username:
            return False
        if credential.password != "" and credential.password == self.credential.password:
            return True
        if credential.token != "" and credential.token == self.credential.token:
            return True
        return False
