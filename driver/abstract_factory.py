from abc import ABC, abstractmethod
from driver.abstract_driver import AbstractDriver
from enum import Enum
from processor.abstract_factory import AbstractProcessorFactory
from pqueue.abstract_factory import AbstractQueueFactory
from puller.abstract_factory import AbstractPullerFactory
from pusher.abstract_factory import AbstractPusherFactory


class DriverCreationError(Exception):
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
        if self.error_code == DriverCreationError.ErrorCode.cant_create_instance:
            return "Can't create " + self.module + " driver instance"
        return "Driver creation error"


class AbstractDriverFactory(ABC):
    @abstractmethod
    def create_driver(self,
                      p_module: str,
                      p_queue_factory: AbstractQueueFactory,
                      p_processor_factory: AbstractProcessorFactory,
                      p_puller_factory: AbstractPullerFactory,
                      p_pusher_factory: AbstractPusherFactory
                      ) -> AbstractDriver:
        pass
