from config.constants import *
from typing import List


class ClientPassenger:
    name: str
    puller_modules: List[str]
    queue_module: str
    processor_module: List[str]
    pusher_modules: List[str]
    sync_frequency: int

    def __init__(self,
                 p_name: str = "Undefined",
                 p_puller_modules: List[str] = [],
                 p_queue_module: str = "",
                 p_processor_modules: List[str] = [],
                 p_pusher_modules: List[str] = [],
                 p_sync_frequency: int = 0):

        self.name = p_name
        self.puller_modules = p_puller_modules
        self.queue_module = p_queue_module
        self.processor_modules = p_processor_modules
        self.pusher_modules = p_pusher_modules
        self.sync_frequency = p_sync_frequency


class Client:
    id: str
    passengers: List[ClientPassenger]

    def __init__(self,
                 p_id: str = "Undefined",
                 p_passengers: List[ClientPassenger] = []):
        self.id = p_id
        self.passengers = p_passengers

    def get_client_passenger(self, p_name: str) -> ClientPassenger:
        for passenger in self.passengers:
            if passenger.name == p_name:
                return passenger
        return None


