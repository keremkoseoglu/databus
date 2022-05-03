""" Abstract puller factory module """
from enum import Enum
from typing import Protocol
from databus.client.log import Log
from databus.puller.abstract_puller import AbstractPuller

class PullerCreationError(Exception):
    """ Puller creation exception class """

    class ErrorCode(Enum):
        """ Puller creation error code """
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
        """ Puller creation error message """
        if self.error_code == PullerCreationError.ErrorCode.cant_create_instance:
            return f"Can't create {self.module} puller instance"
        if self.error_code == PullerCreationError.ErrorCode.parameter_missing:
            return "Parameters missing, can't create puller instance"
        return "Puller creation error"


class AbstractPullerFactory(Protocol): # pylint: disable=R0903
    """ Abstract puller factory class """
    def create_puller(self, p_module: str, p_log: Log) -> AbstractPuller:
        """ Puller factory """
