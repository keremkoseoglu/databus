""" Default passenger factory module """
import inspect
from databus.passenger.abstract_passenger import AbstractPassenger
from databus.passenger.abstract_factory import AbstractPassengerFactory, PassengerCreationError


class PrimalPassengerFactory(AbstractPassengerFactory): # pylint: disable=R0903
    """ Default passenger factory class """

    def create_passenger(self, p_module: str) -> AbstractPassenger:
        """ Default passenger factory """
        if p_module == "" or p_module is None:
            raise PassengerCreationError(PassengerCreationError.ErrorCode.parameter_missing)

        module = __import__(p_module, fromlist=[""])
        for name, obj in inspect.getmembers(module, inspect.isclass):
            if name != "AbstractPassenger":
                try:
                    obj_instance = obj()
                    if isinstance(obj_instance, AbstractPassenger):
                        return obj_instance
                except Exception: # pylint: disable=W0703
                    pass

        raise PassengerCreationError(
            PassengerCreationError.ErrorCode.cant_create_instance,
            p_module=p_module)