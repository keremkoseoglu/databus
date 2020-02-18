from processor.abstract_processor import AbstractProcessor
from processor.factory import ProcessorFactory
from puller.abstract_puller import AbstractPuller
from puller.factory import PullerFactory
from typing import List


class Client:
    name: str
    processors: List[AbstractProcessor]
    pullers: List[AbstractPuller]
    sync_frequency: int

    def __init__(self,
                 p_name: str = "Undefined",
                 p_processor_modules: List[str] = [],
                 p_puller_modules: List[str] = [],
                 p_sync_frequency: int = 0):
        self.name = p_name
        self.sync_frequency = p_sync_frequency
        self.processors = []
        self.pullers = []

        for processor_module in p_processor_modules:
            processor_obj = ProcessorFactory.create_processor(processor_module)
            self.processors.append(processor_obj)

        for puller_module in p_puller_modules:
            puller_obj = PullerFactory.create_puller(puller_module)
            self.pullers.append(puller_obj)
