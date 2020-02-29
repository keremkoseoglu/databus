from client.log import Log, LogEntry, MessageType
from pqueue.queue_status import PassengerQueueStatus, QueueStatus
from processor.abstract_processor import AbstractProcessor
from typing import List


class DemoProcessor1(AbstractProcessor):

    def hello_world(self):
        print("Demo processor 1 says hello world!")

    def process(self, p_passengers: List[PassengerQueueStatus]):
        if len(p_passengers) > 1:
            self.log.append_text("Marking last passenger as processed & pushed")
            last_passenger = p_passengers[len(p_passengers)-1]
            last_passenger.set_all_processor_statuses(QueueStatus.complete)
            last_passenger.set_all_pusher_statuses(QueueStatus.complete)
            self.log.append_text("Remaining passengers: " + str(len(p_passengers)))
        else:
            return
