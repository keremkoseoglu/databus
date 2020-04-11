""" Abstract queue factory module """
from abc import abstractmethod
from enum import Enum
from databus.client.log import Log
from databus.database.abstract_database import AbstractDatabase
from databus.pqueue.abstract_queue import AbstractQueue


class QueueCreationError(Exception):
    """ Queue creation exception """

    class ErrorCode(Enum):
        """ Queue creation error code """
        cant_create_instance: 1
        parameter_missing: 2

    def __init__(self,
                 p_error_code: ErrorCode,
                 p_module: str = ""):

        super().__init__()
        self.error_code = p_error_code

        if p_module is None:
            self.module = ""
        else:
            self.module = p_module

    @property
    def message(self) -> str:
        """ Error message as text """
        if self.error_code == QueueCreationError.ErrorCode.cant_create_instance:
            return "Can't create " + self.module + " queue instance"
        if self.error_code == QueueCreationError.ErrorCode.parameter_missing:
            return "Parameters missing, can't create database instance"
        return "Database creation error"


class AbstractQueueFactory: # pylint: disable=R0903
    """ Abstract queue factory class """
    @abstractmethod
    def create_queue(self,
                     p_module: str,
                     p_database: AbstractDatabase,
                     p_log: Log) -> AbstractQueue:
        """ Queue factory """
