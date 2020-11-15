""" Default puller factory module """
from vibhaga.inspector import Inspector
from databus.client.log import Log
from databus.puller.abstract_factory import AbstractPullerFactory, PullerCreationError
from databus.puller.abstract_puller import AbstractPuller, AbstractPullerError


class PrimalPullerFactory(AbstractPullerFactory):  # pylint: disable=R0903
    """ Default puller factory class """

    def create_puller(self, p_module: str, p_log: Log) -> AbstractPuller:
        """ Puller factory """
        if p_module == "" or p_module is None:
            raise PullerCreationError(PullerCreationError.ErrorCode.parameter_missing)

        candidates = Inspector.get_classes_in_module(p_module, exclude_classes=["AbstractPuller"])

        for candidate in candidates:
            try:
                obj_instance = candidate(p_log)
                if isinstance(obj_instance, AbstractPuller) and obj_instance.__module__ == p_module:
                    return obj_instance
            except AbstractPullerError as puller_error:
                raise puller_error
            except Exception: # pylint: disable=W0703
                continue

        raise PullerCreationError(
            PullerCreationError.ErrorCode.cant_create_instance,
            p_module=p_module)
