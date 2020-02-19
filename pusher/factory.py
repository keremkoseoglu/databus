import inspect
from pusher.abstract_pusher import AbstractPusher


class PusherFactory:
    @staticmethod
    def create_pusher(p_module: str) -> AbstractPusher:
        module = __import__(p_module, fromlist=[""])
        for name, obj in inspect.getmembers(module, inspect.isclass):
            if name != "AbstractPusher":
                obj_instance = obj()
                if isinstance(obj_instance, AbstractPusher):
                    return obj_instance

