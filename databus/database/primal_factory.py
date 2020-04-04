""" Default database factory module """
import inspect
from databus.client.log import Log
from databus.database.abstract_database import AbstractDatabase
from databus.database.abstract_factory import AbstractDatabaseFactory, DatabaseCreationError
from databus.passenger.abstract_factory import AbstractPassengerFactory


class PrimalDatabaseFactory(AbstractDatabaseFactory):
    """ Default database factory class """
    def create_database(self,
                        p_module: str,
                        p_client_id: str,
                        p_log: Log,
                        p_passenger_factory: AbstractPassengerFactory,
                        p_arguments: dict
                        ) -> AbstractDatabase:
        """ Default method for database creation """
        if p_module == "" or p_module is None:
            raise DatabaseCreationError(DatabaseCreationError.ErrorCode.parameter_missing)

        module = __import__(p_module, fromlist=[""])
        for name, obj in inspect.getmembers(module, inspect.isclass):
            if name not in ("AbstractDatabase", "datetime"):
                try:
                    obj_instance = obj(p_client_id, p_log, p_passenger_factory, p_arguments)
                    if isinstance(obj_instance, AbstractDatabase):
                        return obj_instance
                except Exception:
                    continue

        raise DatabaseCreationError(DatabaseCreationError.ErrorCode.cant_create_instance,
                                    p_module=p_module,
                                    p_client_id=p_client_id)
