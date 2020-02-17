from passenger.abstract_passenger import AbstractPassenger
from passenger.factory import PassengerFactory
from typing import List


class ClientPassenger:
    module: str
    passenger: AbstractPassenger
    sync_frequency: int

    def __init__(self,
                 p_module: str = "",
                 p_sync_frequency: int = 0):
        self.module = p_module
        self.sync_frequency = p_sync_frequency

        if self.module == "":
            self.passenger = None
        else:
            self.passenger = PassengerFactory.create_passenger(self.module)


class Client:
    name: str
    passengers: List[ClientPassenger]

    def __init__(self,
                 p_name: str = "Undefined",
                 p_passengers: List[ClientPassenger] = []):
        self.name = p_name
        self.passengers = p_passengers
