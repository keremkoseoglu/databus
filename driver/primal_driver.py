from client.log import Log, LogEntry, MessageType
from driver.abstract_driver import AbstractDriver, BusTicket
from pqueue.abstract_queue import AbstractQueue
from pqueue.abstract_factory import AbstractQueueFactory
from pqueue.queue_status import QueueStatus
from processor.abstract_factory import AbstractProcessorFactory
from puller.abstract_factory import AbstractPullerFactory
from pusher.abstract_factory import AbstractPusherFactory


class Bus:
    def __init__(self,
                 p_ticket: BusTicket = BusTicket(),
                 p_queue: AbstractQueue = None):
        self.ticket = p_ticket
        self.new_passengers = []
        self.deliverable_passengers = []
        self.processable_passengers = []
        self.queue = p_queue


class PrimalDriver(AbstractDriver):

    def __init__(self,
                 p_queue_factory: AbstractQueueFactory,
                 p_processor_factory: AbstractProcessorFactory,
                 p_puller_factory: AbstractPullerFactory,
                 p_pusher_factory: AbstractPusherFactory):
        super().__init__(p_queue_factory, p_processor_factory, p_puller_factory, p_pusher_factory)
        self.__bus = Bus()

    def drive(self, p_bus_ticket: BusTicket):
        p_bus_ticket.log.append_text("Driving...")
        self.__bus.ticket = p_bus_ticket

        try:
            queue = self.queue_factory.create_queue(
                p_bus_ticket.client_passenger.queue_module,
                p_bus_ticket.database,
                p_bus_ticket.log)
        except Exception as e:
            self._log_exception(e, p_log=p_bus_ticket.log)
            return

        self.__bus = Bus(p_ticket=p_bus_ticket, p_queue=queue)
        self._delete_old_log_files()
        self._pull_new_passengers()
        self._seat_passengers()
        self._notify_pullers_about_seated_passengers()
        self._read_processable_passengers()
        self._process_passengers()
        self._read_deliverable_passengers()
        self._push_passengers()

        p_bus_ticket.log.append_text("Drive complete")

    def _delete_old_log_files(self):
        try:
            self.__bus.ticket.log.append_text("Deleting old log files")
            log_expiry_date = self.__bus.ticket.database.client.log_expiry_date
            self.__bus.ticket.database.delete_old_logs(log_expiry_date)
        except Exception as e:
            self._log_exception(e)

    def _log_exception(self, p_exception: Exception, p_log: Log = None):
        if p_log is None:
            log = self.__bus.ticket.log
        else:
            log = p_log

        log.append_entry(LogEntry(p_message="Driver error: " + p_exception.__doc__,
                                  p_type=MessageType.error))

    def _notify_pullers_about_seated_passengers(self):
        self.__bus.ticket.log.append_text("Notifying pullers about seated passengers")
        try:
            for np in self.__bus.queue.get_puller_notifiable_passengers():
                try:
                    self.__bus.ticket.log.append_text("Notifying " +
                                                      np.passenger.puller_module +
                                                 " about " +
                                                      np.passenger.id_text)

                    puller_obj = self.puller_factory.create_puller(np.passenger.puller_module)
                    puller_obj.notify_passengers_seated([np.passenger], self.__bus.ticket.log)
                    np.puller_notified = True
                    self.__bus.queue.update_passenger_status(np)
                except Exception as e:
                    self._log_exception(e)
        except Exception as e:
            self._log_exception(e)

    def _process_passengers(self):
        try:
            self.__bus.ticket.log.append_text("Processing unprocessed passengers")

            for processable_passenger in self.__bus.processable_passengers:
                self.__bus.ticket.log.append_text("Processing " + processable_passenger.passenger.id_text)
                for processor_status in processable_passenger.processor_statuses:
                    if processor_status.status == QueueStatus.complete:
                        continue
                    self.__bus.ticket.log.append_text("Processing " +
                                                      processable_passenger.passenger.id_text +
                                                      " via " +
                                                      processor_status.processor_module)
                    try:
                        processor_obj = self.processor_factory.create_processor(processor_status.processor_module)
                        processor_obj.process(self.__bus.ticket.log, [processable_passenger.passenger])
                        processor_status.status = QueueStatus.complete
                        self.__bus.queue.update_passenger_status(processable_passenger)
                    except Exception as e:
                        self._log_exception(e)
        except Exception as e:
            self._log_exception(e)

    def _pull_new_passengers(self):
        try:
            self.__bus.ticket.log.append_text("Pulling new passengers")

            for puller_module in self.__bus.ticket.client_passenger.puller_modules:
                self.__bus.ticket.log.append_text("Pulling via " + puller_module)
                puller_obj = self.puller_factory.create_puller(puller_module)
                new_passengers = puller_obj.pull(self.__bus.ticket.log)
                for new_passenger in new_passengers:
                    self.__bus.new_passengers.append(new_passenger)
                    self.__bus.ticket.log.append_text("Got new passenger: " + new_passenger.id_text)
        except Exception as e:
            self._log_exception(e)

    def _push_passengers(self):
        try:
            self.__bus.ticket.log.append_text("Pushing deliverable passengers")

            for deliverable_passenger in self.__bus.deliverable_passengers:
                self.__bus.ticket.log.append_text("Delivering " + deliverable_passenger.passenger.id_text)
                for pusher_status in deliverable_passenger.pusher_statuses:
                    if pusher_status.status == QueueStatus.complete:
                        continue
                    self.__bus.ticket.log.append_text("Delivering " +
                                                      deliverable_passenger.passenger.id_text +
                                                      " via " +
                                                      pusher_status.pusher_module)
                    try:
                        pusher_obj = self.pusher_factory.create_pusher(pusher_status.pusher_module)
                        pusher_obj.push(self.__bus.ticket.log, deliverable_passenger)
                        pusher_status.status = QueueStatus.complete
                        self.__bus.queue.update_passenger_status(deliverable_passenger)
                    except Exception as e:
                        self._log_exception(e)
        except Exception as e:
            self._log_exception(e)

    def _read_deliverable_passengers(self):
        try:
            self.__bus.ticket.log.append_text("Reading deliverable passengers from queue")

            self.__bus.deliverable_passengers = self.__bus.queue.get_deliverable_passengers(
                self.__bus.ticket.client_passenger.name)

            for undelivered_passenger in self.__bus.deliverable_passengers:
                self.__bus.ticket.log.append_text("Undelivered passenger: " + undelivered_passenger.passenger.id_text)
        except Exception as e:
            self._log_exception(e)

    def _read_processable_passengers(self):
        try:
            self.__bus.ticket.log.append_text("Reading processable passengers from queue")

            self.__bus.processable_passengers = self.__bus.queue.get_processable_passengers(
                self.__bus.ticket.client_passenger.name)

            for unprocessed_passenger in self.__bus.processable_passengers:
                self.__bus.ticket.log.append_text("Unprocessed passenger: " + unprocessed_passenger.passenger.id_text)
        except Exception as e:
            self._log_exception(e)

    def _seat_passengers(self):
        try:
            self.__bus.ticket.log.append_text("Writing new passengers to queue")

            if len(self.__bus.new_passengers) <= 0:
                return

            self.__bus.queue.insert(self.__bus.new_passengers)
        except Exception as e:
            self._log_exception(e)
