""" Default passenger factory module """
from vibhaga.inspector import Inspector
from databus.passenger.abstract_passenger import AbstractPassenger
from databus.passenger.abstract_factory import AbstractPassengerFactory, PassengerCreationError


class PrimalPassengerFactory(AbstractPassengerFactory): # pylint: disable=R0903
    """ Default passenger factory class """

    def create_passenger(self, p_module: str) -> AbstractPassenger:
        """ Default passenger factory """
        if p_module == "" or p_module is None:
            raise PassengerCreationError(PassengerCreationError.ErrorCode.parameter_missing)

        candidates = Inspector.get_classes_in_module(p_module, exclude_classes=["AbstractPassenger"]) # pylint: disable=C0301
        for candidate in candidates:
            try:
                obj_instance = candidate(p_passenger_module=p_module)
                if obj_instance.__module__ != p_module:
                    continue
                if isinstance(obj_instance, AbstractPassenger):
                    return obj_instance
            except Exception: # pylint: disable=W0703
                pass

        raise PassengerCreationError(
            PassengerCreationError.ErrorCode.cant_create_instance,
            p_module=p_module)
