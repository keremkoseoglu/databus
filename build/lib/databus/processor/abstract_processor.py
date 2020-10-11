""" Abstract processor module """
from abc import ABC, abstractmethod
from typing import List
from databus.client.log import Log
from databus.pqueue.queue_status import PassengerQueueStatus


class AbstractProcessor(ABC): # pylint: disable=R0903
    """ Abstract processor class """
    def __init__(self, p_log: Log = None):
        self.log = p_log

    @abstractmethod
    def process(self, p_passengers: List[PassengerQueueStatus]):
        """ Processes the given passengers """
