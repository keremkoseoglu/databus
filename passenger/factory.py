import inspect
from passenger.abstract_passenger import AbstractPassenger


class PassengerFactory:
    @staticmethod
    def create_passenger(p_module: str) -> AbstractPassenger:
        module = __import__(p_module, fromlist=[""])
        for name, obj in inspect.getmembers(module, inspect.isclass):
            if name != "AbstractPassenger":
                obj_instance = obj()
                if isinstance(obj_instance, AbstractPassenger):
                    return obj_instance
