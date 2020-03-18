from databus.client.log import LogEntry, MessageType
from databus.pqueue.queue_status import PassengerQueueStatus
from databus.processor.abstract_processor import AbstractProcessor
from typing import List


class DemoProcessor1(AbstractProcessor):

    def process(self, p_passengers: List[PassengerQueueStatus]):
        self.log.entries.append(LogEntry(p_message="Doing nothing",
                                         p_type=MessageType.warning))
