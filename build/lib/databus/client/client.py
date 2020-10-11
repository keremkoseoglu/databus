""" Client module """
import datetime
from enum import Enum
from typing import List
from databus.client.client_passenger import ClientPassenger
from databus.client.user import Credential, User


class ClientError(Exception):
    """ Client exception class """

    class ErrorCode(Enum):
        """ Client error code """
        client_not_found = 1
        parameter_missing = 2
        authentication_error = 3

    def __init__(self, p_error_code: ErrorCode, p_client_id: str = None):
        super().__init__()
        self.error_code = p_error_code

        if p_client_id is None:
            self.client_id = ""
        else:
            self.client_id = p_client_id

    @property
    def message(self) -> str:
        """ Client error message """
        if self.error_code == ClientError.ErrorCode.client_not_found:
            return "Client " + self.client_id + " not found"
        if self.error_code == ClientError.ErrorCode.parameter_missing:
            return "Parameter missing, can't find client"
        if self.error_code == ClientError.ErrorCode.authentication_error:
            return "Invalid username or password"
        return "Client error"


class ClientPassengerError(Exception):
    """ Client passenger exception """

    class ErrorCode(Enum):
        """ Client passenger error code """
        passenger_not_found = 1

    def __init__(self,
                 p_error_code: ErrorCode,
                 p_client_id: str = None,
                 p_passenger_name: str = None):
        super().__init__()
        self.error_code = p_error_code

        if p_client_id is None:
            self.client_id = ""
        else:
            self.client_id = p_client_id

        if p_passenger_name is None:
            self.passenger_name = ""
        else:
            self.passenger_name = p_passenger_name

    @property
    def message(self) -> str:
        """ Client passenger error text """
        if self.error_code == ClientPassengerError.ErrorCode.passenger_not_found:
            return self.client_id + " doesn't contain passenger " + self.passenger_name
        return "Client passenger error: " + self.client_id + " " + self.passenger_name


class Client:
    """ Client class """

    ROOT = "root"

    def __init__(self,
                 p_id: str = "Undefined",
                 p_passengers: List[ClientPassenger] = None,
                 p_log_life_span: int = 0,
                 p_users: List[User] = None):
        self.id = p_id  # pylint: disable=C0103
        self.log_life_span = p_log_life_span

        if p_passengers is None:
            self.passengers = []
        else:
            self.passengers = p_passengers

        if p_users is None:
            self.users = []
        else:
            self.users = p_users

    @property
    def authorization_active(self) -> bool:
        """ Is authorization active or not? """
        return len(self.users) > 0

    @property
    def log_expiry_date(self) -> datetime.datetime:
        """ Log expiry date """
        return datetime.datetime.now() - datetime.timedelta(self.log_life_span)

    def authenticate(self, credential: Credential) -> User:
        """ Authenticates a user """
        if not self.authorization_active:
            return User()
        for user in self.users:
            if user.authenticate(credential):
                return user
        raise ClientPassengerError(
            ClientError.ErrorCode.authentication_error,
            self.id)

    def get_client_passenger(self, p_name: str) -> ClientPassenger:
        """ Returns the requested client passenger """
        for passenger in self.passengers:
            if passenger.name == p_name:
                return passenger

        raise ClientPassengerError(
            ClientPassengerError.ErrorCode.passenger_not_found,
            self.id,
            p_name)
