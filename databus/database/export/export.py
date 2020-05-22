""" Module for data export operations """
from enum import Enum
from threading import Thread
from databus.client.log import Log, LogEntry, MessageType
from databus.database.abstract_database import AbstractDatabase
from databus.database.export.export_package import ExportPackage
from databus.database.export.export_request import ExportRequest


class ExportStatus(Enum):
    """ Defines an export status """
    IDLE = 1
    BUSY = 2


class Exporter:
    """ Executes an export request """

    def __init__(self, p_request: ExportRequest = None):
        self.request = p_request
        self._status = ExportStatus.IDLE

    @property
    def status(self) -> ExportStatus:
        """ Returns the status of the exporter """
        return self._status

    def execute(self, p_request: ExportRequest = None):
        """ Executes the export operation """
        self._prepare_before_execute(p_request)

        try:
            self._status = ExportStatus.BUSY
            log = Log()
            log.append_text("Starting data export")
            self.request.dispatcher.export_data_begin()
            source_db = self.request.dispatcher.get_client_database(self.request.client)
            package = Exporter._pull(source_db)
            Exporter._push(package, self.request.target_db)
        except Exception as error: # pylint: disable=W0703
            error_entry = LogEntry(
                str(error),
                p_type=MessageType.error)
            log.append_entry(error_entry)
        finally:
            self.request.dispatcher.export_data_end()
            log.append_text("Data export finished")
            try:
                self.request.target_db.insert_log(log)
            except Exception: # pylint: disable=W0703
                pass
            self._status = ExportStatus.IDLE
            print("Export complete")

    def execute_async(self, p_request: ExportRequest = None):
        """ Executes the export operation async """
        self._prepare_before_execute(p_request)
        Thread(target=self.execute(p_request), daemon=True).start()

    @staticmethod
    def _pull(p_database: AbstractDatabase) -> ExportPackage:
        output = ExportPackage(
            p_client=p_database.client,
            p_queues=p_database.get_passenger_queue_entries()
        )
        return output

    @staticmethod
    def _push(p_package: ExportPackage, p_database: AbstractDatabase):
        p_database.insert_client(p_package.client)

        for queue in p_package.queues:
            p_database.insert_passenger_queue(queue)

    def _prepare_before_execute(self, p_request: ExportRequest = None):
        if self._status == ExportStatus.BUSY:
            raise Exception("Exporter is busy, try later")
        if p_request is not None:
            self.request = p_request
        if self.request is None:
            raise Exception("No request provided")


class ExporterFactory: # pylint: disable=R0903
    """ Factory class for singleton Exporter instance """
    _SINGLETON = Exporter()

    @staticmethod
    def get_singleton() -> Exporter:
        """ Returns a singleton instance """
        return ExporterFactory._SINGLETON
