""" Abstract driver factory module """
from abc import ABC, abstractmethod
from enum import Enum
from databus.driver.abstract_driver import AbstractDriver
from databus.processor.abstract_factory import AbstractProcessorFactory
from databus.pqueue.abstract_factory import AbstractQueueFactory
from databus.puller.abstract_factory import AbstractPullerFactory
from databus.pusher.abstract_factory import AbstractPusherFactory


class DriverCreationError(Exception):
    """ Driver creation exception """

    class ErrorCode(Enum):
        """ Driver creation error code """
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
        """ Error message as string """
        if self.error_code == DriverCreationError.ErrorCode.cant_create_instance:
            return "Can't create " + self.module + " driver instance"
        return "Driver creation error"


class AbstractDriverFactory(ABC): # pylint: disable=R0903
    """ Abstract driver factory class """
    @abstractmethod
    def create_driver(self, # pylint: disable=R0913
                      p_module: str,
                      p_queue_factory: AbstractQueueFactory,
                      p_processor_factory: AbstractProcessorFactory,
                      p_puller_factory: AbstractPullerFactory,
                      p_pusher_factory: AbstractPusherFactory
                      ) -> AbstractDriver:
        """ Driver creation """
