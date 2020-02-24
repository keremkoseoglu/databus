from client.client_passenger import ClientPassenger
import datetime
from enum import Enum
from typing import List


class ClientError(Exception):
    class ErrorCode(Enum):
        client_not_found = 1
        parameter_missing = 2

    def __init__(self, p_error_code: ErrorCode, p_client_id: str = ""):
        self.error_code = p_error_code

        if p_client_id is None:
            self.client_id = ""
        else:
            self.client_id = p_client_id

    @property
    def message(self) -> str:
        if self.error_code == ClientError.ErrorCode.client_not_found:
            return "Client " + self.client_id + " not found"
        if self.error_code == ClientError.ErrorCode.parameter_missing:
            return "Parameter missing, can't find client"
        return "Client error"


class ClientPassengerError(Exception):
    class ErrorCode(Enum):
        passenger_not_found = 1

    def __init__(self, p_error_code: ErrorCode, p_client_id: str = "", p_passenger_name: str = ""):
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
        if self.error_code == ClientPassengerError.ErrorCode.passenger_not_found:
            return self.client_id + " doesn't contain passenger " + self.passenger_name
        return "Client passenger error: " + self.client_id + " " + self.passenger_name


class Client:
    def __init__(self,
                 p_id: str = "Undefined",
                 p_passengers: List[ClientPassenger] = [],
                 p_log_life_span: int = 0):
        self.id = p_id
        self.passengers = p_passengers
        self.log_life_span = p_log_life_span

    @property
    def log_expiry_date(self) -> datetime.datetime:
        return datetime.datetime.now() - datetime.timedelta(self.log_life_span)

    def get_client_passenger(self, p_name: str) -> ClientPassenger:
        for passenger in self.passengers:
            if passenger.name == p_name:
                return passenger
        raise ClientPassengerError(self.id, ClientPassengerError.ErrorCode.passenger_not_found, p_name=p_name)

