""" Abstract factory module """
from abc import ABC, abstractmethod
from enum import Enum
from databus.dispatcher.abstract_dispatcher import AbstractDispatcher, DispatcherTicket



class DispatcherCreationError(Exception):
    """ Dispatcher creation exception """

    class ErrorCode(Enum):
        """ Error code """
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
        """ Error message """
        if self.error_code == DispatcherCreationError.ErrorCode.cant_create_instance:
            return "Can't create " + self.module + " dispatcher instance"
        return "Dispatcher creation error"


class AbstractDispatcherFactory(ABC): # pylint: disable=R0903
    """ Abstract dispatcher factory class """
    @abstractmethod
    def create_dispatcher(self, p_module: str, p_ticket: DispatcherTicket) -> AbstractDispatcher:
        """ Creates a new dispatcher """
