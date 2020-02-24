from abc import ABC, abstractmethod
from enum import Enum
from pusher.abstract_pusher import AbstractPusher


class PusherCreationError(Exception):
    class ErrorCode(Enum):
        cant_create_instance: 1
        parameter_missing: 2

    def __init__(self, p_error_code: ErrorCode, p_module: str = ""):
        self.error_code = p_error_code

        if p_module is None:
            self.module = ""
        else:
            self.module = p_module

    @property
    def message(self) -> str:
        if self.error_code == PusherCreationError.ErrorCode.cant_create_instance:
            return "Can't create " + self.module + " pusher instance"
        elif self.error_code == PusherCreationError.ErrorCode.parameter_missing:
            return "Parameters missing, can't create pusher instance"
        return "Pusher creation error"


class AbstractPusherFactory(ABC):
    @abstractmethod
    def create_pusher(self, p_module: str) -> AbstractPusher:
        pass
