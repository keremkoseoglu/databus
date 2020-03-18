from databus.client.log import Log
from databus.database.abstract_database import AbstractDatabase
from datetime import datetime
from databus.passenger.abstract_passenger import AbstractPassenger
from databus.pqueue.abstract_queue import AbstractQueue
from databus.pqueue.queue_status import QueueStatus, PassengerQueueStatus, QueueStatusFactory
from typing import List


class PrimalQueue(AbstractQueue):

    def __init__(self, p_database: AbstractDatabase, p_log: Log):
        super().__init__(p_database, p_log)

    def delete_completed_passengers(self, p_passenger_module: str, p_pulled_before: datetime):
        self.log.append_text("Deleting " +
                             p_passenger_module +
                             " passengers completed before " +
                             p_pulled_before.isoformat())

        deletable_queue_entries = self.database.get_passenger_queue_entries(
            p_passenger_module=p_passenger_module,
            p_processor_status=QueueStatus.complete,
            p_pusher_status=QueueStatus.complete,
            p_puller_notified=True,
            p_pulled_before=p_pulled_before)

        deletable_passengers = []

        for queue_entry in deletable_queue_entries:
            self.log.append("Initiating deletion for completed passenger " + queue_entry.passenger.id_text)
            deletable_passengers.append(queue_entry.passenger)

        self.database.delete_passenger_queue(deletable_passengers)

    def erase(self):
        self.database.erase_passsenger_queue()

    def insert(self, p_passengers: List[AbstractPassenger]):
        if len(p_passengers) <= 0:
            return

        for passenger in p_passengers:
            self.log.append_text("Inserting passenger into queue: " + passenger.id_text)
            client_passenger = self.database.client.get_client_passenger(passenger.__module__)
            pqs = QueueStatusFactory.get_passenger_queue_status(passenger, client_passenger)
            self.database.insert_passenger_queue(pqs)

    def get_deliverable_passengers(self, p_passenger_module: str) -> List[PassengerQueueStatus]:
        self.log.append_text("Reading deliverable passengers of type " + p_passenger_module)
        output = []

        candidates = self.database.get_passenger_queue_entries(
            p_passenger_module=p_passenger_module,
            p_pusher_status=QueueStatus.incomplete)

        for candidate in candidates:
            if candidate.all_processors_complete:
                output.append(candidate)

        return output

    def get_processable_passengers(self, p_passenger_module: str) -> List[PassengerQueueStatus]:
        self.log.append_text("Reading processable passengers of type " + p_passenger_module)
        return self.database.get_passenger_queue_entries(
            p_passenger_module=p_passenger_module,
            p_processor_status=QueueStatus.incomplete)

    def get_puller_notifiable_passengers(self) -> List[PassengerQueueStatus]:
        self.log.append_text("Reading puller notifiable passengers")
        return self.database.get_passenger_queue_entries(p_puller_notified=False)

    def update_passenger_status(self, p_status: PassengerQueueStatus):
        self.log.append_text("Updating passenger status for " + p_status.passenger.id_text)
        self.database.update_queue_status(p_status)
