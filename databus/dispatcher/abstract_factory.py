from abc import ABC, abstractmethod
from databus.dispatcher.abstract_dispatcher import AbstractDispatcher, DispatcherTicket
from enum import Enum


class DispatcherCreationError(Exception):
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
        if self.error_code == DispatcherCreationError.ErrorCode.cant_create_instance:
            return "Can't create " + self.module + " dispatcher instance"
        return "Dispatcher creation error"


class AbstractDispatcherFactory(ABC):
    @abstractmethod
    def create_dispatcher(self, p_module: str, p_ticket: DispatcherTicket) -> AbstractDispatcher:
        pass
