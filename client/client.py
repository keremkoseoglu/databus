from puller.abstract_puller import AbstractPuller
from puller.factory import PullerFactory
from typing import List


class Client:
    name: str
    pullers: List[AbstractPuller]
    sync_frequency: int

    def __init__(self,
                 p_name: str = "Undefined",
                 p_puller_modules: List[str] = [],
                 p_sync_frequency: int = 0):
        self.name = p_name
        self.sync_frequency = p_sync_frequency
        self.pullers = []

        for puller_module in p_puller_modules:
            puller_obj = PullerFactory.create_puller(puller_module)
            self.pullers.append(puller_obj)
