""" Abstract pusher factory module """
from abc import ABC, abstractmethod
from enum import Enum
from databus.client.log import Log
from databus.pusher.abstract_pusher import AbstractPusher


class PusherCreationError(Exception):
    """ Pusher creation exception class """

    class ErrorCode(Enum):
        """ Pusher creation error enum """
        cant_create_instance: 1
        parameter_missing: 2

    def __init__(self, p_error_code: ErrorCode, p_module: str = None):
        super().__init__()
        self.error_code = p_error_code

        if p_module is None:
            self.module = ""
        else:
            self.module = p_module

    @property
    def message(self) -> str:
        """ Error message as text """
        if self.error_code == PusherCreationError.ErrorCode.cant_create_instance:
            return "Can't create " + self.module + " pusher instance"
        if self.error_code == PusherCreationError.ErrorCode.parameter_missing:
            return "Parameters missing, can't create pusher instance"
        return "Pusher creation error"


class AbstractPusherFactory(ABC): # pylint: disable=R0903
    """ Abstract pusher factory class """
    @abstractmethod
    def create_pusher(self, p_module: str, p_log: Log) -> AbstractPusher:
        """ Creates a new pusher object """
