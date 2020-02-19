from client.log import Log, LogEntry, MessageType
from passenger.abstract_passenger import AbstractPassenger
from processor.abstract_processor import AbstractProcessor
from typing import List


class DemoProcessor1(AbstractProcessor):

    def process(self, p_log: Log, p_passengers: List[AbstractPassenger]):
        p_log.entries.append(LogEntry(p_message="Processor 2 is doing nothing",
                                      p_type=MessageType.warning))
