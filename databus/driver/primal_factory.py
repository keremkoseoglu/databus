from databus.driver.abstract_driver import AbstractDriver
from databus.driver.abstract_factory import AbstractDriverFactory, DriverCreationError
from databus.pqueue.abstract_factory import AbstractQueueFactory
from databus.processor.abstract_factory import AbstractProcessorFactory
from databus.puller.abstract_factory import AbstractPullerFactory
from databus.pusher.abstract_factory import AbstractPusherFactory
import inspect


class PrimalDriverFactory(AbstractDriverFactory):
    def create_driver(self,
                      p_module: str,
                      p_queue_factory: AbstractQueueFactory,
                      p_processor_factory: AbstractProcessorFactory,
                      p_puller_factory: AbstractPullerFactory,
                      p_pusher_factory: AbstractPusherFactory
                      ) -> AbstractDriver:
        if p_module == "" or p_module is None:
            raise DriverCreationError(DriverCreationError.ErrorCode.parameter_missing)

        module = __import__(p_module, fromlist=[""])
        for name, obj in inspect.getmembers(module, inspect.isclass):
            if name != "AbstractDriver":
                try:
                    obj_instance = obj(p_queue_factory,
                                       p_processor_factory,
                                       p_puller_factory,
                                       p_pusher_factory)
                    if isinstance(obj_instance, AbstractDriver):
                        return obj_instance
                except:
                    pass

        raise DriverCreationError(DriverCreationError.ErrorCode.cant_create_instance, p_module=p_module)
