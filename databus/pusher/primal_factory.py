""" Default pusher factory module """
from vibhaga.inspector import Inspector
from databus.client.log import Log
from databus.pusher.abstract_factory import AbstractPusherFactory, PusherCreationError
from databus.pusher.abstract_pusher import AbstractPusher


class PrimalPusherFactory(AbstractPusherFactory): # pylint: disable=R0903
    """ Default pusher factory class """

    def create_pusher(self, p_module: str, p_log: Log) -> AbstractPusher:
        """ Creates a new pusher object """
        if p_module == "" or p_module is None:
            raise PusherCreationError(PusherCreationError.ErrorCode.parameter_missing)

        candidates = Inspector.get_classes_in_module(p_module, exclude_classes=["AbstractPusher"])
        for candidate in candidates:
            try:
                obj_instance = candidate(p_log)
                if isinstance(obj_instance, AbstractPusher):
                    return obj_instance
            except Exception: # pylint: disable=W0703
                pass

        raise PusherCreationError(
            PusherCreationError.ErrorCode.cant_create_instance,
            p_module=p_module)
