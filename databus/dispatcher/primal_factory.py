""" Default dispatcher factory module """
from vibhaga.inspector import Inspector
from databus.dispatcher.abstract_dispatcher import AbstractDispatcher, DispatcherTicket
from databus.dispatcher.abstract_factory import \
    AbstractDispatcherFactory, DispatcherCreationError


class PrimalDispatcherFactory(AbstractDispatcherFactory): # pylint: disable=R0903
    """ Default dispatcher factory class """
    _DEFAULT_DISPATCHER = "databus.dispatcher.primal_dispatcher"

    def create_dispatcher(self,
                          p_module: str = None,
                          p_ticket: DispatcherTicket = None) -> AbstractDispatcher:
        """ Dispatcher factory """

        if p_module == "" or p_module is None:
            dispatcher_module = PrimalDispatcherFactory._DEFAULT_DISPATCHER
        else:
            dispatcher_module = p_module

        if p_ticket is None:
            dispatcher_ticket = DispatcherTicket()
        else:
            dispatcher_ticket = p_ticket

        candidates = Inspector.get_classes_in_module(
            dispatcher_module,
            exclude_classes=["AbstractDispatcher"])

        for candidate in candidates:
            try:
                obj_instance = candidate(dispatcher_ticket)
                if isinstance(obj_instance, AbstractDispatcher):
                    return obj_instance
            except Exception: # pylint: disable=W0703
                pass

        raise DispatcherCreationError(
            DispatcherCreationError.ErrorCode.cant_create_instance,
            p_module=dispatcher_module)
