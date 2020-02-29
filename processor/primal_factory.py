from client.log import Log
import inspect
from processor.abstract_factory import AbstractProcessorFactory, ProcessorCreationError
from processor.abstract_processor import AbstractProcessor


class PrimalProcessorFactory(AbstractProcessorFactory):
    def create_processor(self, p_module: str, p_log: Log) -> AbstractProcessor:
        if p_module == "" or p_module is None:
            raise ProcessorCreationError(ProcessorCreationError.ErrorCode.parameter_missing)

        module = __import__(p_module, fromlist=[""])
        for name, obj in inspect.getmembers(module, inspect.isclass):
            if name != "AbstractProcessor":
                try:
                    obj_instance = obj(p_log)
                    if isinstance(obj_instance, AbstractProcessor):
                        return obj_instance
                except:
                    pass

        raise ProcessorCreationError(ProcessorCreationError.ErrorCode.cant_create_instance, p_module=p_module)
