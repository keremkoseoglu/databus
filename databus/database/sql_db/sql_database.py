""" Module for SQL databases
Credentials for development server:
databus-server.database.windows.net databus_db databus Honk+honk+2
"""
import binascii
from datetime import datetime
from typing import List
from databus.client.client import Client, ClientPassenger
from databus.client.log import Log
from databus.database.abstract_database import AbstractDatabase
from databus.passenger.abstract_factory import AbstractPassengerFactory
from databus.passenger.abstract_passenger import AbstractPassenger, Attachment
from databus.pqueue.queue_status import \
    QueueStatus, PassengerQueueStatus, ProcessorQueueStatus, PusherQueueStatus
from databus.database.sql_db.insert_builder import InsertBuilder
from databus.database.sql_db.query_helper import QueryHelper
from databus.database.sql_db.update_builder import UpdateBuilder
from databus.database.sql_db.value_conversion import DatabusToSql, SqlToDatabus
from databus.database.sql_db.where_builder import WhereBuilder


class SqlDatabase(AbstractDatabase):
    """ Implementation class for JSON database
    Keys of p_arguments can be found in databus.database.sql_db.sql_database_arguments
    """
    def __init__(self,
                 p_client_id: str,
                 p_log: Log,
                 p_passenger_factory: AbstractPassengerFactory,
                 p_arguments: dict):
        super().__init__(p_client_id, p_log, p_passenger_factory, p_arguments)
        self._query_helper = QueryHelper(p_arguments, p_client_id)

    def delete_old_logs(self, p_before: datetime):
        """ Deletes old logs from the database """
        self.log.append_text("Deleting logs before " + p_before.isoformat())
        where_cond = WhereBuilder.date_lt("created_on", p_before)
        log_heads = self._query_helper.select_all("log_head", p_where=where_cond)

        for log_head in log_heads:
            self._query_helper.delete("log_item", p_where="log_id = '" + log_head["log_id"] + "'")
            self._query_helper.delete("log_head", p_where="log_id = '" + log_head["log_id"] + "'")

    def delete_passenger_queue(self, p_passengers: List[AbstractPassenger]):
        """ Deletes passenger from the database """
        self.log.append_text("Deleting passengers from queue")
        for passenger in p_passengers:
            cond = "queue_id = '" + str(passenger.internal_id) + "'"
            self._delete_from_queue(p_where=cond)

    def erase_passenger_queue(self):
        """ Deletes all passengers from the database """
        self.log.append_text("Erasing passenger queue from the database")
        self._delete_from_queue()

    def get_clients(self) -> List[Client]:
        return self._select_from_client()

    def get_log_content(self, p_log_id: str) -> str:
        """ Returns the contents of the given log
        p_log_id is whatever you have returned in get_log_list.
        """
        output = ""
        cond = "log_id = '" + p_log_id + "'"
        log_entries = self._query_helper.select_all("log_item", cond)

        for log_entry in log_entries:
            if output != "":
                output += "\r\n"

            line = Log.build_entry_field_string(p_date=str(log_entry["message_on"]),
                                                p_source=log_entry["module"],
                                                p_type=SqlToDatabus.message_type(log_entry["message_type"]).value,
                                                p_message=log_entry["message"])
            output += line

        return output

    def get_log_list(self) -> List[str]:
        """ Returns log entries """
        output = []
        log_list = self._query_helper.select_all("log_head")
        for log_entry in log_list:
            output.append(log_entry["log_id"])
        return output

    def get_passenger_queue_entries(self, # pylint: disable=R0913
                                    p_passenger_module: str = None,
                                    p_processor_status: QueueStatus = None,
                                    p_pusher_status: QueueStatus = None,
                                    p_puller_notified: bool = None,
                                    p_pulled_before: datetime = None
                                    ) -> List[PassengerQueueStatus]:
        """ Reads the requested entries from the disk """
        self.log.append_text("Reading passenger queue entries")

        return self._select_from_queue(
            p_passenger_module=p_passenger_module,
            p_processor_status=p_processor_status,
            p_pusher_status=p_pusher_status,
            p_puller_notified=p_puller_notified,
            p_pulled_before=p_pulled_before
        )

    def get_passenger_queue_entry(self, # pylint: disable=R0913
                                  p_internal_id: str
                                 ) -> PassengerQueueStatus:

        """ Reads a single entry """
        self.log.append_text("Reading passenger queue entry " + p_internal_id)
        return self._select_from_queue(p_queue_id=p_internal_id)[0]

    def insert_log(self, p_log: Log):
        """ Creates a new log file on the disk """
        self.log.append_text("Writing log to the database")

        insert = InsertBuilder(self.client_id)
        insert.table = "log_head"
        insert.add_string("log_id", p_log.guid)
        insert.add_datetime("created_on", p_log.creation_datetime)
        self._query_helper.execute_insert(insert)

        item_no = 0
        for log_entry in p_log.entries:
            item_no += 1
            insert.table = "log_item"
            insert.add_string("log_id", p_log.guid)
            insert.add_int("item_no", item_no)
            insert.add_string("module", log_entry.source)
            insert.add_string("message_type", DatabusToSql.message_type(log_entry.type))
            insert.add_string("message", log_entry.message)
            self._query_helper.execute_insert(insert)

    def insert_passenger_queue(self, p_passenger_status: PassengerQueueStatus):
        """ Writes new files to the database """
        self.log.append_text("Appending passenger " + p_passenger_status.passenger.id_text)

        insert = InsertBuilder(self.client_id)
        insert.table = "queue"
        insert.add_string("queue_id", p_passenger_status.passenger.internal_id)
        insert.add_string("external_id", p_passenger_status.passenger.external_id)
        insert.add_string("source_system", p_passenger_status.passenger.source_system)
        insert.add_string("passenger_module", p_passenger_status.passenger.__module__)
        insert.add_string("puller_module", p_passenger_status.passenger.puller_module)
        insert.add_string("puller_notified", DatabusToSql.boolean(False))
        insert.add_string("puller_on", DatabusToSql.date_time(p_passenger_status.passenger.pull_datetime))
        self._query_helper.execute_insert(insert)

        processor_exe_order = 0
        for processor in p_passenger_status.processor_statuses:
            processor_exe_order += 1
            insert.table = "queue_processor"
            insert.add_string("queue_id", p_passenger_status.passenger.internal_id)
            insert.add_string("processor_module", processor.processor_module)
            insert.add_string("status", DatabusToSql.queue_status(processor.status))
            insert.add_int("exe_order", processor_exe_order)
            self._query_helper.execute_insert(insert)

        pusher_exe_order = 0
        for pusher in p_passenger_status.pusher_statuses:
            pusher_exe_order += 1
            insert.table = "queue_pusher"
            insert.add_string("queue_id", p_passenger_status.passenger.internal_id)
            insert.add_string("pusher_module", pusher.processor_module)
            insert.add_string("status", DatabusToSql.queue_status(pusher.status))
            insert.add_int("exe_order", pusher_exe_order)
            self._query_helper.execute_insert(insert)

        for attachment in p_passenger_status.passenger.attachments:
            insert.table = "queue_attachment"
            insert.add_string("queue_id", p_passenger_status.passenger.internal_id)
            insert.add_string("attachment_id", attachment.name)
            insert.add_string("txt_content", attachment.text_content)
            insert.add_binary("bin_content", attachment.bin_content)
            insert.add_string("file_format", DatabusToSql.attachment_format(attachment.format))
            self._query_helper.execute_insert(insert)

    def update_queue_status(self, p_status: PassengerQueueStatus):
        """ Updates queue files on the database """
        self.log.append_text("Updating passenger " + p_status.passenger.id_text)
        
        where = WhereBuilder(p_client_id = self.client_id)
        where.add_and("queue_id = '" + p_status.passenger.internal_id + "'")

        update = UpdateBuilder()
        update.table = "queue"
        update.add_int("puller_notified", DatabusToSql.boolean(p_status.puller_notified))
        update.where = where
        self._query_helper.execute_update(update)

        for processor_status in p_status.processor_statuses:
            update.table = "queue_processor"
            update.add_string("status", DatabusToSql.queue_status(processor_status.status))
            update.where = where
            self._query_helper.execute_update(update)

        for pusher_status in p_status.pusher_statuses:
            update.table = "queue_pusher"
            update.add_string("status", DatabusToSql.queue_status(pusher_status.status))
            update.where = where
            self._query_helper.execute_update(update)

    @staticmethod
    def _module_belongs_to_passenger(p_module_row: dict, p_passenger_row: dict) -> bool:
        if p_module_row["client_id"] != p_passenger_row["client_id"]:
            return False
        if p_module_row["passenger_id"] != p_passenger_row["passenger_id"]:
            return False
        return True

    def _delete_from_queue(self, p_where: str = ""):
        self._query_helper.delete("queue_attachment", p_where)
        self._query_helper.delete("queue_processor", p_where)
        self._query_helper.delete("queue_pusher", p_where)
        self._query_helper.delete("queue", p_where)

    def _get_client(self, p_id: str) -> Client:
        return self._select_from_client(p_id=p_id)[0]

    def _select_from_client(self, p_id: str = None) -> List[Client]:
        output = []

        if p_id is None:
            client_list = self._query_helper.select_all_no_where("client")
            passenger_list = self._query_helper.select_all_no_where("passenger", p_order_by="exe_order")
            puller_list = self._query_helper.select_all_no_where("puller", p_order_by="exe_order")
            processor_list = self._query_helper.select_all_no_where("processor", p_order_by="exe_order")
            pusher_list = self._query_helper.select_all_no_where("pusher", p_order_by="exe_order")
        else:
            client_list = self._query_helper.select_all("client")
            passenger_list = self._query_helper.select_all("passenger", p_order_fields=["exe_order"])
            puller_list = self._query_helper.select_all("puller", p_order_fields=["exe_order"])
            processor_list = self._query_helper.select_all("processor", p_order_fields=["exe_order"])
            pusher_list = self._query_helper.select_all("pusher", p_order_fields=["exe_order"])

        for client_row in client_list:
            client = Client(p_id=client_row["client_id"],
                            p_log_life_span=client_row["log_life_span"])
            for passenger_row in passenger_list:
                if passenger_row["client_id"] != client_row["client_id"]:
                    continue

                client_passenger = ClientPassenger(
                    p_name=passenger_row["passenger_module"],
                    p_queue_module=passenger_row["queue_module"],
                    p_sync_frequency=passenger_row["sync_frequency"],
                    p_queue_life_span=passenger_row["queue_life_span"])

                for puller_row in puller_list:
                    if SqlDatabase._module_belongs_to_passenger(puller_row, passenger_row):
                        client_passenger.puller_modules.append(puller_row["puller_module"])
                for processor_row in processor_list:
                    if SqlDatabase._module_belongs_to_passenger(processor_row, passenger_row):
                        client_passenger.processor_modules.append(processor_row["processor_module"])
                for pusher_row in pusher_list:
                    if SqlDatabase._module_belongs_to_passenger(pusher_row, passenger_row):
                        client_passenger.pusher_modules.append(pusher_row["pusher_module"])
                client.passengers.append(client_passenger)
            output.append(client)
        return output

    def _select_from_queue(self, # pylint: disable=R0913
                           p_passenger_module: str = None,
                           p_processor_status: QueueStatus = None,
                           p_pusher_status: QueueStatus = None,
                           p_puller_notified: bool = None,
                           p_pulled_before: datetime = None,
                           p_queue_id: str = None
                           ) -> List[PassengerQueueStatus]:
        output = []
        where = WhereBuilder(self.client_id)

        if p_queue_id is not None:
            where.add_and("queue_id = '" + p_queue_id + "'")
        if p_passenger_module is not None:
            where.add_and("passenger_module = '" + p_passenger_module + "'")
        if p_puller_notified is not None:
            where.add_and("puller_notified = " + DatabusToSql.boolean(p_puller_notified))
        if p_pulled_before is not None:
            where.add_and_date_lt("pulled_on", p_pulled_before)

        where.set_order_by(["pulled_on"])
        queue_list = self._query_helper.select_all_where_builder("queue", where)

        for queue_row in queue_list:
            queue_row_is_eligible = True
            queue_where = "queue_id = '" + queue_row["queue_id"] + "'"

            processor_list = self._query_helper.select_all("queue_processor", queue_where, p_order_fields=["exe_order"])
            if p_processor_status is not None:
                for processor_row in processor_list:
                    if SqlToDatabus.queue_status(processor_row["status"]) != p_processor_status:
                        queue_row_is_eligible = False
                        break
            if not queue_row_is_eligible:
                continue

            pusher_list = self._query_helper.select_all("queue_pusher", queue_where, p_order_fields=["exe_order"])
            if p_pusher_status is not None:
                for pusher_row in pusher_list:
                    if SqlToDatabus.queue_status(pusher_row["status"]) != p_pusher_status:
                        queue_row_is_eligible = False
                        break
            if not queue_row_is_eligible:
                continue

            passenger = AbstractPassenger(
                p_external_id=queue_row["external_id"],
                p_internal_id=queue_row["queue_id"],
                p_source_system=queue_row["source_system"],
                p_puller_module=queue_row["puller_module"],
                p_pull_datetime=SqlToDatabus(queue_row["pulled_on"])
            )

            attachment_list = self._query_helper.select_all("queue_attachment", queue_where)
            for attachment_row in attachment_list:
                filecontent_unhex = binascii.unhexlify(attachment_row["bin_content"])
                bin_content = filecontent_unhex[2:]

                attachment = Attachment(
                    p_name=attachment_row["attachment_id"],
                    p_format=SqlToDatabus.attachment_format(attachment_row["file_format"]),
                    p_text_content=attachment_row["txt_content"],
                    p_binary_content=bin_content)
                passenger.attachments.append(attachment)

            output_row = PassengerQueueStatus(
                p_passenger=passenger,
                p_puller_notified=SqlToDatabus.boolean(queue_row["puller_notified"])
            )

            for processor_row in processor_list:
                pqs = ProcessorQueueStatus(
                    processor_row["processor_module"],
                    SqlToDatabus.queue_status(processor_row["status"]))
                output_row.processor_statuses.append(pqs)

            for pusher_row in pusher_list:
                pqs = PusherQueueStatus(
                    pusher_row["pusher_module"],
                    SqlToDatabus.queue_status(pusher_row["status"]))
                output_row.pusher_statuses.append(pqs)

            output.append(output_row)

        return output


# todo
# - main içerisinde test et - bug'ları temizle
# - web sitesinin about kısmına veritabanını filan koy + diğer components bilgileri
# - binary dosya ile test et, düzgün okuyup yazabiliyor musun? buna ayrı demo puller gerekebilir dummy bin dosya okuyan + pusher bi yere indirsin
# - çoklu insert / update yapılan yerlerde commit / rollback
# - schema oluşturmak için yeni yordam? gittiğimiz yerlerde elle mi açacağız?
# -- abstract'e ekle
# -- json'da olsun (ama boş olsun)
# -- burada olsun
# - main'i eski haline getir
# - buradaki test connection silinecek
# - pylint
# - apply branch
# - versiyon yükselt
