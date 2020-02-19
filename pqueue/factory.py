import inspect
from pqueue.abstract_queue import AbstractQueue


class QueueFactory:
    @staticmethod
    def create_queue(p_module: str) -> AbstractQueue:
        module = __import__(p_module, fromlist=[""])
        for name, obj in inspect.getmembers(module, inspect.isclass):
            if name[:8] != "Abstract":
                obj_instance = obj()
                if isinstance(obj_instance, AbstractQueue):
                    return obj_instance

