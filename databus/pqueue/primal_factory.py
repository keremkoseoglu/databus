""" Default queue factory module """
import inspect
from databus.client.log import Log
from databus.database.abstract_database import AbstractDatabase
from databus.pqueue.abstract_factory import AbstractQueueFactory, QueueCreationError
from databus.pqueue.abstract_queue import AbstractQueue


class PrimalQueueFactory(AbstractQueueFactory): # pylint: disable=R0903
    """ Default queue factory class """

    def create_queue(self,
                     p_module: str,
                     p_database: AbstractDatabase,
                     p_log: Log) -> AbstractQueue:
        """ Queue factory """

        if p_module == "" or p_module is None or p_database is None or p_log is None:
            raise QueueCreationError(
                QueueCreationError.ErrorCode.parameter_missing,
                p_module=str(p_module))

        module = __import__(p_module, fromlist=[""])
        for name, obj in inspect.getmembers(module, inspect.isclass):
            if name[:8] != "Abstract":
                try:
                    obj_instance = obj(p_database, p_log)
                    if isinstance(obj_instance, AbstractQueue):
                        return obj_instance
                except Exception: # pylint: disable=W0703
                    continue

        raise QueueCreationError(
            QueueCreationError.ErrorCode.cant_create_instance,
            p_module=p_module)
