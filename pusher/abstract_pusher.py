from abc import ABC, abstractmethod
from client.log import Log
from pqueue.queue_status import PassengerQueueStatus


class AbstractPusher(ABC):
    def __init__(self):
        pass

    @abstractmethod
    def push(self, p_log: Log, p_passenger: PassengerQueueStatus):
        pass
