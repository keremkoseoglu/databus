from client.log import Log, LogEntry, MessageType
from pqueue.queue_status import PassengerQueueStatus
from processor.abstract_processor import AbstractProcessor
from typing import List


class DemoProcessor1(AbstractProcessor):

    def process(self, p_log: Log, p_passengers: List[PassengerQueueStatus]):
        p_log.entries.append(LogEntry(p_message="Doing nothing",
                                      p_type=MessageType.warning))