""" Default driver module """
from databus.client.log import Log, LogEntry, MessageType
from databus.driver.abstract_driver import AbstractDriver, BusTicket
from databus.pqueue.abstract_queue import AbstractQueue
from databus.pqueue.abstract_factory import AbstractQueueFactory
from databus.pqueue.queue_status import QueueStatus
from databus.processor.abstract_factory import AbstractProcessorFactory
from databus.puller.abstract_factory import AbstractPullerFactory
from databus.pusher.abstract_factory import AbstractPusherFactory


class Bus: # pylint: disable=R0903
    """ Bus object """
    def __init__(self,
                 p_ticket: BusTicket = BusTicket(),
                 p_queue: AbstractQueue = None):
        self.ticket = p_ticket
        self.new_passengers = []
        self.deliverable_passengers = []
        self.processable_passengers = []
        self.queue = p_queue


class PrimalDriver(AbstractDriver):
    """ Default driver class """

    def __init__(self,
                 p_queue_factory: AbstractQueueFactory,
                 p_processor_factory: AbstractProcessorFactory,
                 p_puller_factory: AbstractPullerFactory,
                 p_pusher_factory: AbstractPusherFactory):
        super().__init__(p_queue_factory, p_processor_factory, p_puller_factory, p_pusher_factory)
        self._bus = Bus()

    def drive(self, p_bus_ticket: BusTicket):
        """ Pulls passengers from source systems and pushes them to target systems """
        p_bus_ticket.log.append_text("Driving...")
        self._bus.ticket = p_bus_ticket

        try:
            queue = self.queue_factory.create_queue(
                p_bus_ticket.client_passenger.queue_module,
                p_bus_ticket.database,
                p_bus_ticket.log)
        except Exception as queue_error: # pylint: disable=W0703
            self._log_exception(queue_error, p_log=p_bus_ticket.log)
            return

        self._bus = Bus(p_ticket=p_bus_ticket, p_queue=queue)
        self._delete_old_log_files()
        self._pull_new_passengers()
        self._seat_passengers()
        self._notify_pullers_about_seated_passengers()
        self._read_processable_passengers()
        self._process_passengers()
        self._read_deliverable_passengers()
        self._push_passengers()

        p_bus_ticket.log.append_text("Drive complete")

    @property
    def queue(self) -> AbstractQueue:
        """ Queue object """
        return self._bus.queue

    def _delete_old_log_files(self):
        try:
            self._bus.ticket.log.append_text("Deleting old log files")
            log_expiry_date = self._bus.ticket.database.client.log_expiry_date
            self._bus.ticket.database.delete_old_logs(log_expiry_date)
        except Exception as del_error: # pylint: disable=W0703
            self._log_exception(del_error)

    def _log_exception(self, p_exception: Exception, p_log: Log = None):
        if p_log is None:
            log = self._bus.ticket.log
        else:
            log = p_log

        log.append_entry(LogEntry(p_message="Driver error: " + str(p_exception),
                                  p_type=MessageType.error))

    def _notify_pullers_about_seated_passengers(self):
        self._bus.ticket.log.append_text("Notifying pullers about seated passengers")
        try:
            for npass in self._bus.queue.get_puller_notifiable_passengers():
                try:
                    self._bus.ticket.log.append_text("Notifying " +
                                                     npass.passenger.puller_module +
                                                     " about " +
                                                     npass.passenger.id_text)

                    puller_obj = self.puller_factory.create_puller(
                        npass.passenger.puller_module,
                        self._bus.ticket.log)

                    puller_obj.notify_passengers_seated([npass.passenger])
                    npass.puller_notified = True
                    self._bus.queue.update_passenger_status(npass)
                except Exception as notif_error: # pylint: disable=W0703
                    self._log_exception(notif_error)
        except Exception as notif_error: # pylint: disable=W0703
            self._log_exception(notif_error)

    def _process_passengers(self):
        try:
            self._bus.ticket.log.append_text("Processing unprocessed passengers")

            for processable_passenger in self._bus.processable_passengers:
                self._bus.ticket.log.append_text(
                    "Processing " + processable_passenger.passenger.id_text)

                for processor_status in processable_passenger.processor_statuses:
                    if processor_status.status == QueueStatus.complete:
                        continue
                    self._bus.ticket.log.append_text("Processing " +
                                                     processable_passenger.passenger.id_text +
                                                     " via " +
                                                     processor_status.processor_module)
                    try:
                        processor_obj = self.processor_factory.create_processor(
                            processor_status.processor_module,
                            self._bus.ticket.log)
                        processor_obj.process([processable_passenger])
                        processor_status.status = QueueStatus.complete
                        self._bus.queue.update_passenger_status(processable_passenger)
                    except Exception as process_error: # pylint: disable=W0703
                        self._log_exception(process_error)
        except Exception as process_error: # pylint: disable=W0703
            self._log_exception(process_error)

    def _pull_new_passengers(self):
        try:
            self._bus.ticket.log.append_text("Pulling new passengers")
            for puller_module in self._bus.ticket.client_passenger.puller_modules:
                self._bus.ticket.log.append_text("Pulling via " + puller_module)

                new_passengers = self.pull_passengers_from_module(
                    puller_module,
                    p_log=self._bus.ticket.log)

                for new_passenger in new_passengers:
                    self._bus.new_passengers.append(new_passenger)
                    self._bus.ticket.log.append_text("Got new passenger: " + new_passenger.id_text)
        except Exception as pull_error: # pylint: disable=W0703
            self._log_exception(pull_error)

    def _push_passengers(self):
        try:
            self._bus.ticket.log.append_text("Pushing deliverable passengers")

            for deliverable_passenger in self._bus.deliverable_passengers:
                self._bus.ticket.log.append_text(
                    "Delivering " + deliverable_passenger.passenger.id_text)

                for pusher_status in deliverable_passenger.pusher_statuses:
                    if pusher_status.status == QueueStatus.complete:
                        continue
                    self._bus.ticket.log.append_text("Delivering " +
                                                     deliverable_passenger.passenger.id_text +
                                                     " via " +
                                                     pusher_status.pusher_module)
                    try:
                        pusher_obj = self.pusher_factory.create_pusher(pusher_status.pusher_module,
                                                                       self._bus.ticket.log)
                        pusher_obj.push(deliverable_passenger)
                        pusher_status.status = QueueStatus.complete
                        self._bus.queue.update_passenger_status(deliverable_passenger)
                    except Exception as push_error: # pylint: disable=W0703
                        self._log_exception(push_error)
        except Exception as push_error: #pylint: disable=W0703
            self._log_exception(push_error)

    def _read_deliverable_passengers(self):
        try:
            self._bus.ticket.log.append_text("Reading deliverable passengers from queue")

            self._bus.deliverable_passengers = self._bus.queue.get_deliverable_passengers(
                self._bus.ticket.client_passenger.name)

            for undelivered_passenger in self._bus.deliverable_passengers:
                self._bus.ticket.log.append_text(
                    "Undelivered passenger: " + undelivered_passenger.passenger.id_text)
        except Exception as read_error: # pylint: disable=W0703
            self._log_exception(read_error)

    def _read_processable_passengers(self):
        try:
            self._bus.ticket.log.append_text("Reading processable passengers from queue")

            self._bus.processable_passengers = self._bus.queue.get_processable_passengers(
                self._bus.ticket.client_passenger.name)

            for unprocessed_passenger in self._bus.processable_passengers:
                self._bus.ticket.log.append_text(
                    "Unprocessed passenger: " + unprocessed_passenger.passenger.id_text)
        except Exception as read_error: # pylint: disable=W0703
            self._log_exception(read_error)

    def _seat_passengers(self):
        try:
            self._bus.ticket.log.append_text("Writing new passengers to queue")

            if len(self._bus.new_passengers) <= 0:
                return

            self._bus.queue.insert(self._bus.new_passengers)
        except Exception as seat_error: # pylint: disable=W0703
            self._log_exception(seat_error)
