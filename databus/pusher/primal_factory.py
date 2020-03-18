from databus.client.log import Log
import inspect
from databus.pusher.abstract_factory import AbstractPusherFactory, PusherCreationError
from databus.pusher.abstract_pusher import AbstractPusher


class PrimalPusherFactory(AbstractPusherFactory):
    def create_pusher(self, p_module: str, p_log: Log) -> AbstractPusher:
        if p_module == "" or p_module is None:
            raise PusherCreationError(PusherCreationError.ErrorCode.parameter_missing)

        module = __import__(p_module, fromlist=[""])
        for name, obj in inspect.getmembers(module, inspect.isclass):
            if name != "AbstractPusher":
                try:
                    obj_instance = obj(p_log)
                    if isinstance(obj_instance, AbstractPusher):
                        return obj_instance
                except:
                    pass

        raise PusherCreationError(PusherCreationError.ErrorCode.cant_create_instance, p_module=p_module)

