import inspect
from passenger.abstract_passenger import AbstractPassenger
from passenger.abstract_factory import AbstractPassengerFactory, PassengerCreationError


class PrimalPassengerFactory(AbstractPassengerFactory):
    def create_passenger(self, p_module: str) -> AbstractPassenger:
        if p_module == "" or p_module is None:
            raise PassengerCreationError(PassengerCreationError.ErrorCode.parameter_missing)

        module = __import__(p_module, fromlist=[""])
        for name, obj in inspect.getmembers(module, inspect.isclass):
            if name != "AbstractPassenger":
                obj_instance = obj()
                if isinstance(obj_instance, AbstractPassenger):
                    return obj_instance

        raise PassengerCreationError(PassengerCreationError.ErrorCode.cant_create_instance, p_module=p_module)
