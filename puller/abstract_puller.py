from abc import ABC, abstractmethod
from client.log import Log
from passenger.abstract_passenger import AbstractPassenger
from typing import List


class AbstractPuller(ABC):
    def __init__(self, p_log: Log = None):
        self.log = p_log
        pass

    @abstractmethod
    def notify_passengers_seated(self, p_seated_passengers: List[AbstractPassenger]):
        pass

    @abstractmethod
    def pull(self) -> List[AbstractPassenger]:
        pass
