""" Abstract processor factory module """
from abc import ABC, abstractmethod
from enum import Enum
from databus.client.log import Log
from databus.processor.abstract_processor import AbstractProcessor


class ProcessorCreationError(Exception):
    """ Abstract processor creation exception """
    class ErrorCode(Enum):
        """ Error code enum """
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
        if self.error_code == ProcessorCreationError.ErrorCode.cant_create_instance:
            return "Can't create " + self.module + " processor instance"
        if self.error_code == ProcessorCreationError.ErrorCode.parameter_missing:
            return "Parameters missing, can't create processor instance"
        return "Processor creation error"


class AbstractProcessorFactory(ABC): # pylint: disable=R0903
    """ Abstract processor factory """
    @abstractmethod
    def create_processor(self, p_module: str, p_log: Log) -> AbstractProcessor:
        """ Processor factory """
