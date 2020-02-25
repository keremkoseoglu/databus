from dispatcher.abstract_dispatcher import AbstractDispatcher, DispatcherTicket
from dispatcher.abstract_factory import AbstractDispatcherFactory, DispatcherCreationError
import inspect


class PrimalDispatcherFactory(AbstractDispatcherFactory):
    def create_dispatcher(self,
                          p_module: str,
                          p_ticket: DispatcherTicket
                          ) -> AbstractDispatcher:
        if p_module == "" or p_module is None:
            raise DispatcherCreationError(DispatcherCreationError.ErrorCode.parameter_missing)

        module = __import__(p_module, fromlist=[""])
        for name, obj in inspect.getmembers(module, inspect.isclass):
            if name != "AbstractDispatcher":
                try:
                    obj_instance = obj(p_ticket)
                    if isinstance(obj_instance, AbstractDispatcher):
                        return obj_instance
                except:
                    pass

        raise DispatcherCreationError(DispatcherCreationError.ErrorCode.cant_create_instance, p_module=p_module)
