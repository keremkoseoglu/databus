""" Default queue module """
from datetime import datetime
from typing import List
from databus.client.log import LogEntry, MessageType
from databus.passenger.abstract_passenger import AbstractPassenger
from databus.pqueue.abstract_queue import AbstractQueue
from databus.pqueue.queue_status import QueueStatus, PassengerQueueStatus, QueueStatusFactory


class PrimalQueue(AbstractQueue):
    """ Default queue class """

    def delete_completed_passengers(self, p_passenger_module: str, p_pulled_before: datetime):
        """ Deletes completed passengers from the database,
        which were pulled before p_pulled_before and queued, processed, puller-notified, pushed
        """
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
            self.log.append_text(
                f"Initiating deletion for completed passenger {queue_entry.passenger.id_text}")
            deletable_passengers.append(queue_entry.passenger)

        self.database.delete_passenger_queue(deletable_passengers)

    def erase(self):
        """ Deletes all passengers from the database """
        self.database.erase_passenger_queue()

    def insert(self, p_passengers: List[AbstractPassenger]):
        """ Adds a new passenger to the database """
        if len(p_passengers) <= 0:
            return

        existing_passengers = self.database.get_passenger_queue_entries()

        for passenger in p_passengers:
            passenger.collect_log_guid(self.log.guid)
            self.log.append_text("Inserting passenger into queue: " + passenger.id_text)

            already_exists = False
            for existing_passenger in existing_passengers:
                if all([existing_passenger.passenger.source_system == passenger.source_system,
                        existing_passenger.passenger.external_id == passenger.external_id]):
                    already_exists = True
                    break

            if already_exists:
                self.log.append_entry(LogEntry(
                    p_message="Passenger already in queue, skipping",
                    p_type=MessageType.warning))
                continue

            client_passenger = self.database.client.get_client_passenger(passenger.passenger_module)
            pqs = QueueStatusFactory.get_passenger_queue_status(passenger, client_passenger)
            self.database.insert_passenger_queue(pqs)

    def get_deliverable_passengers(self, p_passenger_module: str) -> List[PassengerQueueStatus]:
        """ Returns passengers which can be pushed
        Passengers returned here are pulled, queued, processed and puller-notified,
        but not delivered
        """
        self.log.append_text(f"Reading deliverable passengers of type {p_passenger_module}")
        output = []

        candidates = self.database.get_passenger_queue_entries(
            p_passenger_module=p_passenger_module,
            p_pusher_status=QueueStatus.incomplete)

        for candidate in candidates:
            if candidate.all_processors_complete:
                output.append(candidate)

        return output

    def get_processable_passengers(self, p_passenger_module: str) -> List[PassengerQueueStatus]:
        """ Returns passengers which can be processed
        Passengers returned here are pulled, queued and puller-notified,
        but not processed
        """
        self.log.append_text(f"Reading processable passengers of type {p_passenger_module}")
        return self.database.get_passenger_queue_entries(
            p_passenger_module=p_passenger_module,
            p_processor_status=QueueStatus.incomplete)

    def get_puller_notifiable_passengers(self) -> List[PassengerQueueStatus]:
        """ Returns passengers which have been queued
        Passengers returned here are pulled, queued,
        but not puller-notified
        """
        self.log.append_text("Reading puller notifiable passengers")
        return self.database.get_passenger_queue_entries(p_puller_notified=False)

    def update_passenger_status(self, p_status: PassengerQueueStatus):
        """ Updates passenger status """
        p_status.passenger.collect_log_guid(self.log.guid)
        self.log.append_text(f"Updating passenger status for {p_status.passenger.id_text}")
        self.database.update_queue_status(p_status)
