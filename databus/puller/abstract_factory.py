from abc import ABC, abstractmethod
from databus.client.log import Log
from enum import Enum
from databus.puller.abstract_puller import AbstractPuller


class PullerCreationError(Exception):
    class ErrorCode(Enum):
        cant_create_instance: 1
        parameter_missing: 2

    def __init__(self, p_error_code: ErrorCode, p_module: str = None):
        self.error_code = p_error_code

        if p_module is None:
            self.module = ""
        else:
            self.module = p_module

    @property
    def message(self) -> str:
        if self.error_code == PullerCreationError.ErrorCode.cant_create_instance:
            return "Can't create " + self.module + " puller instance"
        elif self.error_code == PullerCreationError.ErrorCode.parameter_missing:
            return "Parameters missing, can't create puller instance"
        return "Puller creation error"


class AbstractPullerFactory(ABC):
    @abstractmethod
    def create_puller(self, p_module: str, p_log: Log) -> AbstractPuller:
        pass
