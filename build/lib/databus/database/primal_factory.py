""" Default database factory module """
from typing import List
from vibhaga.inspector import Inspector
from databus.client.log import Log
from databus.database.abstract_database import AbstractDatabase
from databus.database.abstract_factory import AbstractDatabaseFactory, DatabaseCreationError
from databus.database.json_db.json_database import JsonDatabase # pylint: disable=W0611
from databus.database.sql_db.sql_database import SqlDatabase # pylint: disable=W0611
from databus.passenger.abstract_factory import AbstractPassengerFactory


class PrimalDatabaseFactory(AbstractDatabaseFactory): # pylint: disable=R0903
    """ Default database factory class """
    def create_database(self, # pylint: disable=R0913
                        p_module: str,
                        p_client_id: str,
                        p_log: Log,
                        p_passenger_factory: AbstractPassengerFactory,
                        p_arguments: dict
                        ) -> AbstractDatabase:
        """ Default method for database creation """
        if p_module == "" or p_module is None:
            raise DatabaseCreationError(DatabaseCreationError.ErrorCode.parameter_missing)

        if p_client_id is None:
            client_id = ""
        else:
            client_id = p_client_id

        candidates = Inspector.get_classes_in_module(
            p_module,
            exclude_classes=["AbstractDatabase", "datetime"])

        for candidate in candidates:
            try:
                obj_instance = candidate(client_id, p_log, p_passenger_factory, p_arguments)
                if isinstance(obj_instance, AbstractDatabase):
                    return obj_instance
            except Exception: # pylint: disable=W0703
                continue

        raise DatabaseCreationError(DatabaseCreationError.ErrorCode.cant_create_instance,
                                    p_module=p_module,
                                    p_client_id=p_client_id)

    @property
    def database_modules(self) -> List[str]:
        """ Returns a list of database modules in the system """
        output = []
        for subclass in AbstractDatabase.__subclasses__():
            output.append(subclass.__module__)
        return output

    @property
    def database_classes(self) -> List[str]:
        """ Returns a list of database classes in the system """
        return ["JsonDatabase", "SqlDatabase"]
