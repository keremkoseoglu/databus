from client.log import Log, LogEntry, MessageType
from passenger.abstract_passenger import AbstractPassenger
from processor.abstract_processor import AbstractProcessor
from typing import List


class DemoProcessor1(AbstractProcessor):

    def hello_world(self):
        print("Demo processor 1 says hello world!")

    def process(self, p_log: Log, p_passengers: List[AbstractPassenger]):
        if len(p_passengers) > 1:
            p_log.append("Processor 1 is deleting the last passenger")
            p_passengers.pop()
            p_log.append("Remaining passengers: " + str(len(p_passengers)))
        else:
            p_log.entries.append(LogEntry(p_message="Processor 1 is doing nothing",
                                          p_type=MessageType.warning))
