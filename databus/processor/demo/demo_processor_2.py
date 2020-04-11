""" Demo processor module """
from typing import List
from databus.client.log import LogEntry, MessageType
from databus.pqueue.queue_status import PassengerQueueStatus
from databus.processor.abstract_processor import AbstractProcessor


class DemoProcessor1(AbstractProcessor): # pylint: disable=R0903
    """ Demo processor class """

    def process(self, p_passengers: List[PassengerQueueStatus]):
        """ Demo process """

        self.log.entries.append(LogEntry(p_message="Doing nothing",
                                         p_type=MessageType.warning))
