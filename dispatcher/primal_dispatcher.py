from client.client import Client
from client.client_passenger import ClientPassenger
from client.log import Log, LogEntry, MessageType
from config.constants import *
from datetime import datetime, timedelta
from dispatcher.abstract_dispatcher import AbstractDispatcher, DispatcherTicket
from driver.abstract_driver import BusTicket
from time import sleep
from typing import List


class ClientPassengerTickCount:
    def __init__(self):
        self._ticks = {}

    def collect(self, p_client_id: str, p_passenger_id: str):
        key = ClientPassengerTickCount._build_key(p_client_id, p_passenger_id)
        if key not in self._ticks:
            self._ticks[key] = 0

    def collect_clients(self, p_clients: List[Client]):
        for client in p_clients:
            for passenger in client.passengers:
                self.collect(client.id, passenger.name)

    def get_tick(self, p_client_id: str, p_passenger_id: str):
        self.collect(p_client_id, p_passenger_id)
        key = ClientPassengerTickCount._build_key(p_client_id, p_passenger_id)
        return self._ticks[key]

    def reset_tick(self, p_client_id: str, p_passenger_id: str):
        self.collect(p_client_id, p_passenger_id)
        key = ClientPassengerTickCount._build_key(p_client_id, p_passenger_id)
        self._ticks[key] = 0

    def tick(self):
        for t in self._ticks:
            self._ticks[t] += 1

    @staticmethod
    def _build_key(p_client_id: str, p_passenger_id: str):
        return p_client_id + ":-:" + p_passenger_id


class DispatchState:
    def __init__(self):
        self.clients = List[Client]


class PrimalDispatcher(AbstractDispatcher):
    def __init__(self, p_ticket: DispatcherTicket = None):
        super().__init__(p_ticket)
        self._dispatch_state = DispatchState()
        self._next_dispatch_time = datetime.now()
        self._tick_count = ClientPassengerTickCount()

    def start(self):
        while True:
            self._next_dispatch_time = self._next_dispatch_time + timedelta(0, 60)
            self._dispatch()
            self._sleep_until_next_dispatch_time()

    def _dispatch(self):
        self._dispatch_state = DispatchState()
        self._read_clients()
        self._drive_high_time_passengers()

    def _drive_high_time_passengers(self):
        for client in self._dispatch_state.clients:
            for client_passenger in client.passengers:
                try:
                    tick_count = self._tick_count.get_tick(client.id, client_passenger.name)
                    if tick_count < client_passenger.sync_frequency:
                        continue
                    self._tick_count.reset_tick(client.id, client_passenger.name)
                    self._drive_passenger(client, client_passenger)
                except Exception as e:
                    print(e.__doc__)

    def _drive_passenger(self, p_client: Client, p_client_passenger: ClientPassenger):
        log = Log()
        try:
            log.append_text("Dispatching client " +
                             p_client.id +
                             " passenger " +
                             p_client_passenger.name)

            log.append_text("Creating database " +
                            self.ticket.database_module)

            db = self.ticket.database_factory.create_database(
                p_passenger_factory=self.ticket.passenger_factory,
                p_client_id=p_client.id,
                p_module=self.ticket.database_module,
                p_log=log)

            log.append_text("Creating driver " + self.ticket.driver_module)

            driver = self.ticket.driver_factory.create_driver(
                self.ticket.driver_module,
                self.ticket.queue_factory,
                self.ticket.processor_factory,
                self.ticket.puller_factory,
                self.ticket.pusher_factory)

            log.append_text("Creating ticket")

            ticket = BusTicket(
                p_client_passenger=p_client_passenger,
                p_log=log,
                p_database=db)

            log.append_text("Driving")
            driver.drive(ticket)

        except Exception as e:
            if log is not None:
                log.append_entry(LogEntry(p_message=e.__doc__, p_type=MessageType.error))
        finally:
            self._tick_count.reset_tick(p_client.id, p_client_passenger.name)
            if db is not None:
                db.insert_log(log)
                db.delete_old_logs(p_client.log_expiry_date)

    def _read_clients(self):
        dummy_db = self.ticket.database_factory.create_database(
            p_log=Log(),
            p_module=self.ticket.database_module,
            p_client_id=DEMO_CLIENT,
            p_passenger_factory=self.ticket.passenger_factory)

        self._dispatch_state.clients = dummy_db.get_clients()
        self._tick_count.collect_clients(self._dispatch_state.clients)
        self._tick_count.tick()

    def _sleep_until_next_dispatch_time(self):
        now = datetime.now()
        if now >= self._next_dispatch_time:
            return
        seconds_to_sleep = (self._next_dispatch_time - now).seconds
        sleep(seconds_to_sleep)

