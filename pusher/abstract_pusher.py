from abc import ABC, abstractmethod
from client.log import Log
from passenger.abstract_passenger import AbstractPassenger
from typing import List


class AbstractPusher(ABC):
    def __init__(self):
        pass

    @abstractmethod
    def push(self, p_log: Log, p_passengers: List[AbstractPassenger]):
        pass
