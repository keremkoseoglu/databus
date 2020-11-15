""" Abstract puller module """
from abc import ABC, abstractmethod
from typing import List
from databus.client.log import Log
from databus.passenger.abstract_passenger import AbstractPassenger


class AbstractPullerError(Exception):
    """ Abstract puller exception """

    def __init__(self,
                 p_error_description: str):
        super().__init__()
        self.error_description = p_error_description

    def __str__(self):
        return self.error_description


class AbstractPuller(ABC):
    """ Abstract puller class """
    def __init__(self, p_log: Log = None):
        self.log = p_log

    @abstractmethod
    def notify_passengers_seated(self, p_seated_passengers: List[AbstractPassenger]):
        """ Called after a passenger is properly queued.
        You would typically write a code here to ensure that the passenger is not
        returned any more when the puller works again.
        """

    def peek(self) -> List[AbstractPassenger]:
        """ Peeks into the "inbox" of the source system
        and returns whatever awaits to be pulled.
        Normally, this method would simply pull and return
        whatever is in the inbox. However; if your source system
        needs to behave differently in peek / pull situations,
        you can override this method in your subclass.
        """
        return self.pull()

    @abstractmethod
    def pull(self) -> List[AbstractPassenger]:
        """ Pulls passengers from the source system """
