""" Abstract passenger factory module """
from abc import ABC, abstractmethod
from enum import Enum
from databus.passenger.abstract_passenger import AbstractPassenger


class PassengerCreationError(Exception):
    """ Passenger creation exception class """
    class ErrorCode(Enum):
        """ Passenger creation error codes """
        cant_create_instance: 1
        parameter_missing: 2

    def __init__(self, p_error_code: ErrorCode, p_module: str = ""):
        super().__init__()
        self.error_code = p_error_code

        if p_module is None:
            self.module = ""
        else:
            self.module = p_module

    @property
    def message(self) -> str:
        """ Passenger creation error message """
        if self.error_code == PassengerCreationError.ErrorCode.cant_create_instance:
            return "Can't create " + self.module + " passenger instance"
        if self.error_code == PassengerCreationError.ErrorCode.parameter_missing:
            return "Parameters missing, can't create passenger instance"
        return "Passenger creation error"


class AbstractPassengerFactory(ABC): # pylint: disable=R0903
    """ Abstract passenger factory class """
    @abstractmethod
    def create_passenger(self, p_module: str) -> AbstractPassenger:
        """ Abstract passenger factory """
