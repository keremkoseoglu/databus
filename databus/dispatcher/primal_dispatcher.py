""" Default dispatcher module """
from datetime import datetime, timedelta
from threading import Thread
from time import sleep
from typing import List
import os
from databus.client.client import Client
from databus.client.client_passenger import ClientPassenger
from databus.client.log import Log, LogEntry, MessageType
from databus.dispatcher.abstract_dispatcher import AbstractDispatcher, DispatcherTicket
from databus.driver.abstract_driver import BusTicket
from databus.web import app


class ClientPassengerTickCount:
    """ Keeps track of passenger ticks """
    _INFINITE_TICK = 999999999

    def __init__(self):
        self._ticks = {}

    def collect(self, p_client_id: str, p_passenger_id: str):
        """ Inserts the client & passenger if they weren't before """
        key = ClientPassengerTickCount._build_key(p_client_id, p_passenger_id)
        if key not in self._ticks:
            self._ticks[key] = 0

    def collect_clients(self, p_clients: List[Client]):
        """ Inserts missing clients """
        for client in p_clients:
            for passenger in client.passengers:
                self.collect(client.id, passenger.name)

    def expedite_client_passenger(self, p_client_id: str, p_passenger_id: str):
        """ Prioritizes the passenger in the next cycle """
        key = ClientPassengerTickCount._build_key(p_client_id, p_passenger_id)
        if key not in self._ticks:
            return
        self._ticks[key] = ClientPassengerTickCount._INFINITE_TICK

    def get_tick(self, p_client_id: str, p_passenger_id: str):
        """ Returns the current tick count """
        self.collect(p_client_id, p_passenger_id)
        key = ClientPassengerTickCount._build_key(p_client_id, p_passenger_id)
        return self._ticks[key]

    def reset_tick(self, p_client_id: str, p_passenger_id: str):
        """ Resets tick """
        self.collect(p_client_id, p_passenger_id)
        key = ClientPassengerTickCount._build_key(p_client_id, p_passenger_id)
        self._ticks[key] = 0

    def tick(self):
        """ Increases tick counts for all client passengers """
        for self_tick in self._ticks:
            self._ticks[self_tick] += 1

    @staticmethod
    def _build_key(p_client_id: str, p_passenger_id: str):
        return p_client_id + ":-:" + p_passenger_id


class DispatchState: # pylint: disable=R0903
    """ State of the dispatcher """
    def __init__(self):
        self.clients = List[Client]


class DispatcherStatus:
    """ Status of the dispatcher """
    def __init__(self):
        self.pausing = False
        self.paused = False
        self.dispatching = False
        self.exporting = False
        self.shutting_down = False


class PrimalDispatcher(AbstractDispatcher): # pylint: disable=R0903
    """ Default dispatcher implementation """

    def __init__(self, p_ticket: DispatcherTicket = None):
        super().__init__(p_ticket)
        self._dispatch_state = DispatchState()
        self._next_dispatch_time = datetime.now()
        self._tick_count = ClientPassengerTickCount()
        self._status = DispatcherStatus()

    @property
    def dispatching(self) -> bool:
        """ Is the dispatcher active or not """
        return self._status.dispatching

    @property
    def paused(self) -> bool:
        """ Is the dispatcher paused or not """
        return self._status.pausing or self._status.paused

    @property
    def exporting(self) -> bool:
        """ Is export active or not """
        return self._status.exporting

    @property
    def shutting_down(self) -> bool:
        """ Is shutdown active or not """
        return self._status.shutting_down

    def expedite_client_passenger(self, p_client_id: str, p_passenger_module: str):
        """ Prioritizes the passenger in the next cycle """
        self._tick_count.expedite_client_passenger(p_client_id, p_passenger_module)

    def export_data_begin(self):
        """ Indicates that data export is starting """
        self.request_pause()
        self._wait_until_paused()
        self._status.exporting = True

    def export_data_end(self):
        """ Indicates that data export is ending """
        self._status.exporting = False
        self.resume()

    def start(self):
        """ Starts the dispatcher timer and web server """
        if self.ticket.run_web_server:
            Thread(target=self._start_web_server, daemon=True).start()
        self._start_dispatch_timer()

    def request_shutdown(self):
        """ Dispatcher shutdown """
        self._status.shutting_down = True
        Thread(target=self._shutdown_when_safely_possible, daemon=True).start()

    def request_pause(self):
        """ Pauses dispatcher
        This is the antonym of resume
        """
        if self.paused:
            return
        if self._status.shutting_down:
            raise Exception("Can't pause while shutting down")

        self._status.pausing = True
        self._status.paused = False
        Thread(target=self._pause_when_safely_possible, daemon=True).start()

    def resume(self):
        """ Resumes the dispatcher
        This is the antonym of pause
        """
        if self._status.pausing:
            raise Exception("Pause in progress, can't resume yet")
        self._status.pausing = False
        self._status.paused = False

    def _dispatch(self):
        try:
            if self.paused or self._status.shutting_down:
                return
            self._status.dispatching = True
            self._dispatch_state = DispatchState()
            self._read_clients()
            self._drive_high_time_passengers()
        finally:
            self._status.dispatching = False

    def _drive_high_time_passengers(self):
        for client in self._dispatch_state.clients:
            for client_passenger in client.passengers:
                try:
                    tick_count = self._tick_count.get_tick(client.id, client_passenger.name)
                    if tick_count < client_passenger.sync_frequency:
                        continue
                    self._tick_count.reset_tick(client.id, client_passenger.name)
                    self._drive_passenger(client, client_passenger)
                except Exception as drive_error: # pylint: disable=W0703
                    print(str(drive_error))

    def _drive_passenger(self, p_client: Client, p_client_passenger: ClientPassenger):
        if self.paused or self._status.shutting_down:
            return
        log = Log()
        db = None # pylint: disable=C0103
        driver = None
        try:
            log.append_text("Dispatching client " +
                            p_client.id +
                            " passenger " +
                            p_client_passenger.name)

            log.append_text("Creating database " + self.ticket.database_module)
            db = self.get_client_database(p_client.id, log) # pylint: disable=C0103
            log.append_text("Checking schema")
            db.ensure_schema_existence()
            log.append_text("Creating driver " + self.ticket.driver_module)
            driver = self.get_driver()
            log.append_text("Creating ticket")

            ticket = BusTicket(
                p_client_passenger=p_client_passenger,
                p_log=log,
                p_database=db)

            log.append_text("Driving")
            driver.drive(ticket)

        except Exception as drive_error: # pylint: disable=W0703
            if log is not None:
                log.append_entry(LogEntry(p_message=str(drive_error), p_type=MessageType.error))
        finally:
            self._tick_count.reset_tick(p_client.id, p_client_passenger.name)
            if self.ticket.dispatcher_observer is not None and log is not None:
                self.ticket.dispatcher_observer.drive_passenger_complete(p_client,
                                                                         p_client_passenger,
                                                                         log)
            if db is not None:
                db.insert_log(log)
                db.delete_old_logs(p_client.log_expiry_date)
            if driver is not None:
                driver.queue.delete_completed_passengers(
                    p_client_passenger.name,
                    p_client_passenger.queue_expiry_date)

    def _read_clients(self):
        self._dispatch_state.clients = self.all_clients
        self._tick_count.collect_clients(self._dispatch_state.clients)
        self._tick_count.tick()

    def _sleep_until_next_dispatch_time(self):
        now = datetime.now()
        if now >= self._next_dispatch_time:
            return
        seconds_to_sleep = (self._next_dispatch_time - now).seconds
        sleep(seconds_to_sleep)

    def _start_dispatch_timer(self):
        while True:
            self._next_dispatch_time = self._next_dispatch_time + timedelta(0, 60)
            self._dispatch()
            if self._status.shutting_down:
                return
            self._sleep_until_next_dispatch_time()

    def _start_web_server(self):
        app.run_web_server(self)

    def _pause_when_safely_possible(self):
        while True:
            if not self._status.dispatching:
                self._status.pausing = False
                self._status.paused = True
                return
            sleep(1)

    def _wait_until_paused(self):
        while True:
            if self.paused:
                return
            if (not self._status.pausing) and (not self._status.paused):
                raise Exception("Pause failed")
            sleep(1)

    def _shutdown_when_safely_possible(self):
        while True:
            if not self._status.dispatching and not self._status.exporting:
                os._exit(0) # pylint: disable=W0212
                return
            sleep(1)
