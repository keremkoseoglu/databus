""" Abstract puller module """
from abc import ABC, abstractmethod
from typing import List
from databus.client.log import Log
from databus.passenger.abstract_passenger import AbstractPassenger


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

    @abstractmethod
    def pull(self) -> List[AbstractPassenger]:
        """ Pulls passengers from the source system """
