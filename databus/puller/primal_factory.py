from databus.client.log import Log
import inspect
from databus.puller.abstract_factory import AbstractPullerFactory, PullerCreationError
from databus.puller.abstract_puller import AbstractPuller


class PrimalPullerFactory(AbstractPullerFactory):
    def create_puller(self, p_module: str, p_log: Log) -> AbstractPuller:
        if p_module == "" or p_module is None:
            raise PullerCreationError(PullerCreationError.ErrorCode.parameter_missing)

        module = __import__(p_module, fromlist=[""])
        for name, obj in inspect.getmembers(module, inspect.isclass):
            if name != "AbstractPuller":
                try:
                    obj_instance = obj(p_log)
                    if isinstance(obj_instance, AbstractPuller):
                        return obj_instance
                except:
                    continue

        raise PullerCreationError(PullerCreationError.ErrorCode.cant_create_instance, p_module=p_module)
