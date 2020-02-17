from abc import ABC, abstractmethod
from client.log import Log
from passenger.abstract_passenger import AbstractPassenger
from typing import List


class AbstractPuller(ABC):
    def __init__(self):
        pass

    @abstractmethod
    def pull(self, p_log: Log) -> List[AbstractPassenger]:
        pass
