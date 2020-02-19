import inspect
from puller.abstract_puller import AbstractPuller


class PullerFactory:
    @staticmethod
    def create_puller(p_module: str) -> AbstractPuller:
        module = __import__(p_module, fromlist=[""])
        for name, obj in inspect.getmembers(module, inspect.isclass):
            if name != "AbstractPuller":
                try:
                    obj_instance = obj()
                    if isinstance(obj_instance, AbstractPuller):
                        return obj_instance
                except:
                    continue
