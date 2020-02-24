from client.log import Log, LogEntry, MessageType
from pqueue.queue_status import PassengerQueueStatus
from processor.abstract_processor import AbstractProcessor
from typing import List


class DemoProcessor1(AbstractProcessor):

    def hello_world(self):
        print("Demo processor 1 says hello world!")

    def process(self, p_log: Log, p_passengers: List[PassengerQueueStatus]):
        if len(p_passengers) > 1:
            p_log.append_text("Deleting the last passenger")
            p_passengers.pop()
            p_log.append_text("Remaining passengers: " + str(len(p_passengers)))
        else:
            return
