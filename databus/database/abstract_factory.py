""" Abstract database factory """
from enum import Enum
from typing import List, Protocol
from databus.client.log import Log
from databus.database.abstract_database import AbstractDatabase
from databus.passenger.abstract_factory import AbstractPassengerFactory

class DatabaseCreationError(Exception):
    """ Central database creation exception class """

    class ErrorCode(Enum):
        """ Error code enum """
        cant_create_instance: 1
        parameter_missing: 2

    def __init__(self,
                 p_error_code: ErrorCode,
                 p_module: str = None,
                 p_client_id: str = None):
        super().__init__()
        self.error_code = p_error_code

        if p_module is None:
            self.module = ""
        else:
            self.module = p_module

        if p_client_id is None:
            self.client_id = ""
        else:
            self.client_id = p_client_id

    @property
    def message(self) -> str:
        """ Long text of the error """
        if self.error_code == DatabaseCreationError.ErrorCode.cant_create_instance:
            return f"Can't create {self.module} instance for client {self.client_id}"
        if self.error_code == DatabaseCreationError.ErrorCode.parameter_missing:
            return "Parameters missing, can't create database instance"
        return "Database creation error"


class AbstractDatabaseFactory(Protocol): # pylint: disable=R0903
    """ Abstract database factory """
    def create_database(self, # pylint: disable=R0913
                        p_module: str,
                        p_client_id: str,
                        p_log: Log,
                        p_passenger_factory: AbstractPassengerFactory,
                        p_arguments: dict
                        ) -> AbstractDatabase:
        """ Abstract method for database creation """

    @property
    def database_modules(self) -> List[str]:
        """ Returns a list of database modules in the system """

    @property
    def database_classes(self) -> List[str]:
        """ Returns a list of database classes in the system """
