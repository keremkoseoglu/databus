from processor.abstract_processor import AbstractProcessor
from processor.factory import ProcessorFactory
from puller.abstract_puller import AbstractPuller
from puller.factory import PullerFactory
from pusher.abstract_pusher import AbstractPusher
from pusher.factory import PusherFactory
from typing import List


class Client:
    name: str
    pullers: List[AbstractPuller]
    processors: List[AbstractProcessor]
    pushers: List[AbstractPusher]
    sync_frequency: int

    def __init__(self,
                 p_name: str = "Undefined",
                 p_puller_modules: List[str] = [],
                 p_processor_modules: List[str] = [],
                 p_pusher_modules: List[str] = [],
                 p_sync_frequency: int = 0):
        self.name = p_name
        self.pullers = []
        self.processors = []
        self.pushers = []
        self.sync_frequency = p_sync_frequency

        for puller_module in p_puller_modules:
            puller_obj = PullerFactory.create_puller(puller_module)
            self.pullers.append(puller_obj)

        for processor_module in p_processor_modules:
            processor_obj = ProcessorFactory.create_processor(processor_module)
            self.processors.append(processor_obj)

        for pusher_module in p_pusher_modules:
            pusher_obj = PusherFactory.create_pusher(pusher_module)
            self.pushers.append(pusher_obj)
