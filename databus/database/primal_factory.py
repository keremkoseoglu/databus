from databus.client.log import Log
from databus.database.abstract_database import AbstractDatabase
from databus.database.abstract_factory import AbstractDatabaseFactory, DatabaseCreationError
import inspect
from databus.passenger.abstract_factory import AbstractPassengerFactory


class PrimalDatabaseFactory(AbstractDatabaseFactory):
    def create_database(self,
                        p_module: str,
                        p_client_id: str,
                        p_log: Log,
                        p_passenger_factory: AbstractPassengerFactory
                        ) -> AbstractDatabase:
        if p_module == "" or p_module is None:
            raise DatabaseCreationError(DatabaseCreationError.ErrorCode.parameter_missing)

        module = __import__(p_module, fromlist=[""])
        for name, obj in inspect.getmembers(module, inspect.isclass):
            if name != "AbstractDatabase" and name != "datetime":
                try:
                    obj_instance = obj(p_client_id, p_log, p_passenger_factory)
                    if isinstance(obj_instance, AbstractDatabase):
                        return obj_instance
                except:
                    continue

        raise DatabaseCreationError(DatabaseCreationError.ErrorCode.cant_create_instance,
                                    p_module=p_module,
                                    p_client_id=p_client_id)


