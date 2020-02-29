from abc import ABC, abstractmethod
from client.log import Log
from pqueue.queue_status import PassengerQueueStatus
from typing import List


class AbstractProcessor(ABC):
    def __init__(self, p_log: Log = None):
        self.log = p_log
        pass

    @abstractmethod
    def process(self, p_passengers: List[PassengerQueueStatus]):
        pass
