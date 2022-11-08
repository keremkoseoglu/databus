""" Module for SQL databases

Command to start docker module:
docker run  -d
            --name sql_server_demo
            -e 'ACCEPT_EULA=Y'
            -e 'SA_PASSWORD=reallyStrongPwd123'
            -p 1433:1433 microsoft/mssql-server-linux
Check creation_script.sql to create a new database
"""
from datetime import datetime
import json
from typing import List
from uuid import UUID
from databus.client.client import Client, ClientPassenger
from databus.client.log import Log
from databus.client.user import Credential, User, Role, str_to_role
from databus.client.customizing import ClientCustomizing
from databus.database.abstract_database import AbstractDatabase, LogListItem
from databus.passenger.abstract_factory import AbstractPassengerFactory
from databus.passenger.abstract_passenger import AbstractPassenger, Attachment
from databus.pqueue.queue_status import \
    QueueStatus, PassengerQueueStatus, ProcessorQueueStatus, PusherQueueStatus
from databus.database.sql_db.action_decider import ActionDecider
from databus.database.sql_db.insert_builder import InsertBuilder
from databus.database.sql_db.query_helper import QueryHelper
from databus.database.sql_db.sql_database_arguments import SqlDatabaseArguments
from databus.database.sql_db.update_builder import UpdateBuilder
from databus.database.sql_db.value_conversion import DatabusToSql, SqlToDatabus
from databus.database.sql_db.where_builder import WhereBuilder

ARGS_TEMPLATE = SqlDatabaseArguments.TEMPLATE

class ClientDataset:
    """ Defines a client dataset """
    def __init__(self, p_query_helper: QueryHelper):
        self._query_helper = p_query_helper
        self.client_list = []
        self.passenger_list = []
        self.puller_list = []
        self.processor_list = []
        self.pusher_list = []
        self.user_list = []

    def dump_as_client_list(self) -> List[Client]:
        """ Returns output as a client list """
        output = []

        for client_row in self.client_list:
            client = Client(p_id=client_row["client_id"],
                            p_log_life_span=client_row["log_life_span"])
            for passenger_row in self.passenger_list:
                if passenger_row["client_id"] != client_row["client_id"]:
                    continue

                client_passenger = ClientPassenger(
                    p_name=passenger_row["passenger_module"],
                    p_queue_module=passenger_row["queue_module"],
                    p_sync_frequency=passenger_row["sync_frequency"],
                    p_queue_life_span=passenger_row["queue_life_span"])

                for puller_row in self.puller_list:
                    if ClientDataset._module_belongs_to_passenger(puller_row, passenger_row):
                        client_passenger.puller_modules.append(puller_row["puller_module"])
                for processor_row in self.processor_list:
                    if ClientDataset._module_belongs_to_passenger(processor_row, passenger_row):
                        client_passenger.processor_modules.append(processor_row["processor_module"])
                for pusher_row in self.pusher_list:
                    if ClientDataset._module_belongs_to_passenger(pusher_row, passenger_row):
                        client_passenger.pusher_modules.append(pusher_row["pusher_module"])
                client.passengers.append(client_passenger)

            for user_row in self.user_list:
                credential = Credential(
                    username=user_row["username"],
                    password=user_row["password"],
                    token=user_row["token"])
                if "role" in user_row:
                    role = str_to_role(user_row["role"])
                else:
                    role = Role.UNDEFINED
                user = User(credential=credential, role=role)
                client.users.append(user)

            output.append(client)
        return output

    def dump_as_dict(self) -> dict:
        """ Returns a dict """
        output = {
            "client": self.client_list,
            "passenger": self.passenger_list,
            "puller": self.puller_list,
            "processor": self.processor_list,
            "pusher": self.pusher_list,
            "user": self.user_list
        }
        return output

    def dump_as_json_string(self) -> str:
        """ Returns a string """
        dict_output = self.dump_as_dict()
        return json.dumps(dict_output, indent=4, sort_keys=True)

    def read_for_all_clients(self):
        """ Fills the dataset for all clients """
        self.client_list = self._query_helper.select_all_no_where("client")
        self.passenger_list = self._query_helper.select_all_no_where("passenger", p_order_by="exe_order") # pylint: disable= C0301
        self.puller_list = self._query_helper.select_all_no_where("puller", p_order_by="exe_order")
        self.processor_list = self._query_helper.select_all_no_where("processor", p_order_by="exe_order") # pylint: disable= C0301
        self.pusher_list = self._query_helper.select_all_no_where("pusher", p_order_by="exe_order")
        self.user_list = self._query_helper.select_all_no_where("webuser")

    def read_for_client(self):
        """ Fills the dataset for a single client """
        self.client_list = self._query_helper.select_all("client")
        self.passenger_list = self._query_helper.select_all("passenger", p_order_fields=["exe_order"]) # pylint: disable= C0301
        self.puller_list = self._query_helper.select_all("puller", p_order_fields=["exe_order"])
        self.processor_list = self._query_helper.select_all("processor", p_order_fields=["exe_order"]) # pylint: disable= C0301
        self.pusher_list = self._query_helper.select_all("pusher", p_order_fields=["exe_order"])
        self.user_list = self._query_helper.select_all("webuser")

    @staticmethod
    def _module_belongs_to_passenger(p_module_row: dict, p_passenger_row: dict) -> bool:
        if p_module_row["client_id"] != p_passenger_row["client_id"]:
            return False
        if p_module_row["passenger_id"] != p_passenger_row["passenger_id"]:
            return False
        return True


class SqlDatabase(AbstractDatabase):
    """ Implementation class for SQL Server database
    Keys of p_arguments can be found in databus.database.sql_db.sql_database_arguments
    """

    _LOG_ID_SEPARATOR = " | "

    def __init__(self,
                 p_client_id: str,
                 p_log: Log,
                 p_passenger_factory: AbstractPassengerFactory,
                 p_arguments: dict):
        super().__init__(p_client_id, p_log, p_passenger_factory, p_arguments)
        self._query_helper = QueryHelper(p_arguments, p_client_id)
        if p_client_id is None:
            self.client = None
        else:
            self.client = self._get_client(p_client_id)

    @property
    def client_master_data(self) -> str:
        """ Returns the definition of all clients as a JSON string """
        client_list = self._query_helper.select_all_no_where("client", "client_id")
        output_dict = {"client": client_list}
        return json.dumps(output_dict, indent=4, sort_keys=True)

    @client_master_data.setter
    def client_master_data(self, p_definitions: str):
        """ Writes the customizing into the database
        See getter for sample JSON format
        """
        ActionDecider(self._query_helper).decide_and_execute(
            json.loads(p_definitions),
            json.loads(self.client_master_data))

    @property
    def customizing(self) -> str:
        """ Returns the client customizing as JSON """
        dataset = ClientDataset(self._query_helper)
        dataset.read_for_client()
        return dataset.dump_as_json_string()

    @property
    def customizing_dict(self) -> dict:
        """ Returns the client customizing as dict """
        dataset = ClientDataset(self._query_helper)
        dataset.read_for_client()
        return dataset.dump_as_dict()

    @customizing.setter
    def customizing(self, p_customizing: str):
        """ Writes the customizing into the database
        See getter for sample JSON format
        """
        ActionDecider(self._query_helper).decide_and_execute(
            json.loads(p_customizing),
            self.customizing_dict)

    def delete_old_logs(self, p_before: datetime):
        """ Deletes old logs from the database """
        self.log.append_text("Deleting logs before " + p_before.isoformat())
        where_cond = WhereBuilder.date_lt("created_on", p_before)
        log_heads = self._query_helper.select_all("log_head", p_where=where_cond)

        try:
            for log_head in log_heads:
                self._query_helper.delete("log_item", p_where="log_id = '" + log_head["log_id"] + "'") # pylint: disable= C0301
                self._query_helper.delete("log_head", p_where="log_id = '" + log_head["log_id"] + "'") # pylint: disable= C0301
            self._query_helper.commit()
        except Exception as error:
            self._query_helper.rollback()
            raise error

    def delete_passenger_queue(self, p_passengers: List[AbstractPassenger]):
        """ Deletes passenger from the database """
        self.log.append_text("Deleting passengers from queue")

        try:
            for passenger in p_passengers:
                cond = "queue_id = '" + str(passenger.internal_id) + "'"
                self._delete_from_queue(p_where=cond)
            self._query_helper.commit()
        except Exception as error:
            self._query_helper.rollback()
            raise error

    def ensure_schema_existence(self):
        """ Checks the schema for the client
        Creates / completes the schema if anything is missing
        """
        existing_client = self._query_helper.select_single("client")
        if len(existing_client) > 0:
            return
        self._insert_into_client(self.client_id, 1)
        self._query_helper.commit()

    def erase_passenger_queue(self):
        """ Deletes all passengers from the database """
        self.log.append_text("Erasing passenger queue from the database")
        try:
            self._delete_from_queue()
            self._query_helper.commit()
        except Exception as error:
            self._query_helper.rollback()
            raise error

    def get_clients(self) -> List[Client]:
        return self._select_from_client()

    def get_log_content(self, p_log_id: str) -> str:
        """ Returns the contents of the given log
        p_log_id is whatever you have returned in get_log_list.
        """
        output = ""
        log_id = p_log_id.split(SqlDatabase._LOG_ID_SEPARATOR)[1]
        cond = "log_id = '" + log_id + "'"
        log_entries = self._query_helper.select_all("log_item", cond)

        for log_entry in log_entries:
            if output != "":
                output += "\r\n"

            line = Log.build_entry_field_string(
                p_date=str(log_entry["message_on"]),
                p_source=log_entry["module"],
                p_type=SqlToDatabus.message_type(log_entry["message_type"]).name,
                p_message=log_entry["message"])
            output += line

        return output

    def get_log_list(self) -> List[LogListItem]:
        """ Returns log entries """
        output = []
        log_list = self._query_helper.select_all("log_head")

        worst_msg_types = self._query_helper.select_all("log_worst_message_type")

        for log_entry in log_list:
            output_item = LogListItem()
            output_item.log_id = str(log_entry["created_on"]) + SqlDatabase._LOG_ID_SEPARATOR + log_entry["log_id"] # pylint: disable= C0301

            for worst_msg_type in worst_msg_types:
                if worst_msg_type["log_id"] == output_item.log_id:
                    output_item.worst_message_type = worst_msg_type["worst_message_type"]
                    break

            output.append(output_item)
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

    def insert_client(self, p_client: Client):
        """ Inserts a new client """
        try:
            self._insert_into_client(p_client.id, p_client.log_life_span)

            exe_order = 0
            for passenger in p_client.passengers:
                insert = InsertBuilder(self._query_helper.args, p_client.id)
                insert.table = "passenger"
                insert.add_string("passenger_id", passenger.id)
                insert.add_string("passenger_module", passenger.module)
                insert.add_string("queue_module", passenger.queue_module)
                insert.add_int("sync_frequency", passenger.sync_frequency)
                insert.add_int("queue_life_span", passenger.queue_life_span)
                exe_order += 1
                insert.add_int("exe_order", exe_order)
                self._query_helper.execute_insert(insert)

            for user in p_client.users:
                insert = InsertBuilder(self._query_helper.args, p_client.id)
                insert.table = "webuser"
                insert.add_string("username", user.credential.username)
                insert.add_string("password", user.credential.password)
                insert.add_string("token", user.credential.token)
                self._query_helper.execute_insert(insert)

            self._query_helper.commit()
        except Exception as error:
            self._query_helper.rollback()
            raise error

    def insert_log(self, p_log: Log):
        """ Creates a new log file on the disk """
        self.log.append_text("Writing log to the database")
        insert = InsertBuilder(self._query_helper.args, self.client_id)
        insert.table = "log_head"
        insert.add_string("log_id", p_log.guid)
        insert.add_datetime("created_on", p_log.creation_datetime)
        self._query_helper.execute_insert(insert)
        item_no = 0

        try:
            for log_entry in p_log.entries:
                item_no += 1
                insert.table = "log_item"
                insert.add_string("log_id", p_log.guid)
                insert.add_int("item_no", item_no)
                insert.add_string("module", log_entry.source)
                insert.add_string("message_type", DatabusToSql.message_type(log_entry.type))
                insert.add_string("message", log_entry.message)
                self._query_helper.execute_insert(insert)

            self._query_helper.commit()
        except Exception as error:
            self._query_helper.rollback()
            raise error

    def insert_passenger_queue(self, p_passenger_status: PassengerQueueStatus):
        """ Writes new files to the database """
        self.log.append_text("Appending passenger " + p_passenger_status.passenger.id_text)
        try:
            insert = InsertBuilder(self._query_helper.args, self.client_id)
            insert.table = "queue"
            insert.add_string("queue_id", p_passenger_status.passenger.internal_id)
            insert.add_string("external_id", p_passenger_status.passenger.external_id)
            insert.add_string("source_system", p_passenger_status.passenger.source_system)
            insert.add_string("passenger_module", p_passenger_status.passenger.passenger_module)
            insert.add_string("puller_module", p_passenger_status.passenger.puller_module)
            insert.add_string("puller_notified", DatabusToSql.boolean(False))
            insert.add_string("pulled_on", DatabusToSql.date_time(p_passenger_status.passenger.pull_datetime)) # pylint: disable= C0301
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
                insert.add_string("pusher_module", pusher.pusher_module)
                insert.add_string("status", DatabusToSql.queue_status(pusher.status))
                insert.add_int("exe_order", pusher_exe_order)
                self._query_helper.execute_insert(insert)

            for attachment in p_passenger_status.passenger.attachments:
                table_path = self._query_helper.path_builder.get_table_path("insert_queue_attachment") # pylint: disable=C0301

                sql = "{call " + table_path + "(?, ?, ?, ?, ?, ?)}"
                values = (self.client_id,
                          p_passenger_status.passenger.internal_id,
                          attachment.name,
                          attachment.text_content,
                          attachment.binary_content,
                          DatabusToSql.attachment_format(attachment.format))
                self._query_helper.execute_stored_procedure(sql, values)

            self._insert_logs(p_passenger_status)
            self._query_helper.commit()
        except Exception as error:
            self._query_helper.rollback()
            raise error

    def update_queue_status(self, p_status: PassengerQueueStatus):
        """ Updates queue files on the database """
        self.log.append_text("Updating passenger " + p_status.passenger.id_text)

        try:
            where = WhereBuilder(p_client_id=self.client_id)
            where.add_and("queue_id = '" + p_status.passenger.internal_id + "'")

            update = UpdateBuilder(self._query_helper.args)
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

            self._insert_logs(p_status)
            self._query_helper.commit()

        except Exception as error:
            self._query_helper.rollback()
            raise error

    def convert_log_guid_to_id(self, p_guid: UUID) -> str:
        """ UUID to id conversion """
        guid_as_str = str(p_guid)
        log_ids = self.get_log_list()
        for log in log_ids:
            if guid_as_str in log.log_id:
                return log.log_id
        return ""

    def update_user_credential(self, p_credential: Credential):
        """ Updates the credential of the given user """
        where = WhereBuilder(p_client_id=self.client_id)
        where.add_and("username = '" + p_credential.username + "'")

        update = UpdateBuilder(self._query_helper.args)
        update.table = "webuser"
        update.add_string("password", p_credential.password)
        update.add_string("token", p_credential.token)
        update.where = where
        self._query_helper.execute_update(update)

    def backup_client_customizing(self, p_cc: ClientCustomizing):
        """ Backup customizing nodes """
        # will be implemented later

    def delete_old_client_customizing_backups(self, p_before: datetime, p_log: Log):
        """ Deletes overdue client customizing backups """
        # will be implemented later

    def _insert_logs(self, p_passenger_status: PassengerQueueStatus):
        del_where = "queue_id = '" + p_passenger_status.passenger.internal_id + "'"
        self._query_helper.delete("queue_log", p_where=del_where)

        insert = InsertBuilder(self._query_helper.args, self.client_id)
        for log in p_passenger_status.passenger.log_guids:
            insert.table = "queue_log"
            insert.add_string("queue_id", p_passenger_status.passenger.internal_id)
            insert.add_string("log_id", str(log))
            self._query_helper.execute_insert(insert)

    def _delete_from_queue(self, p_where: str = ""):
        self._query_helper.delete("queue_attachment", p_where)
        self._query_helper.delete("queue_processor", p_where)
        self._query_helper.delete("queue_pusher", p_where)
        self._query_helper.delete("queue_log", p_where)
        self._query_helper.delete("queue", p_where)

    def _get_client(self, p_id: str) -> Client:
        return self._select_from_client(p_id=p_id)[0]

    def _select_from_client(self, p_id: str = None) -> List[Client]: # pylint: disable=R0914
        client_dataset = ClientDataset(self._query_helper)
        if p_id is None:
            client_dataset.read_for_all_clients()
        else:
            client_dataset.read_for_client()
        return client_dataset.dump_as_client_list()

    def _select_from_queue(self, # pylint: disable=R0912, R0913, R0914, R0915
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
            where.add_and("puller_notified = " + str(DatabusToSql.boolean(p_puller_notified)))
        if p_pulled_before is not None:
            where.add_and_date_lt("pulled_on", p_pulled_before)

        where.set_order_by(["pulled_on"])
        queue_list = self._query_helper.select_all_where_builder("queue", where)

        for queue_row in queue_list:
            queue_row_is_eligible = True
            queue_where = "queue_id = '" + queue_row["queue_id"] + "'"

            processor_list = self._query_helper.select_all("queue_processor", queue_where, p_order_fields=["exe_order"]) # pylint: disable= C0301
            if p_processor_status is not None and len(processor_list) > 0:
                for processor_row in processor_list:
                    if SqlToDatabus.queue_status(processor_row["status"]) != p_processor_status:
                        queue_row_is_eligible = False
                        break
            if not queue_row_is_eligible:
                continue

            pusher_list = self._query_helper.select_all("queue_pusher", queue_where, p_order_fields=["exe_order"]) # pylint: disable= C0301
            if p_pusher_status is not None and len(pusher_list) > 0:
                for pusher_row in pusher_list:
                    if SqlToDatabus.queue_status(pusher_row["status"]) != p_pusher_status:
                        queue_row_is_eligible = False
                        break
            if not queue_row_is_eligible:
                continue

            passenger = self.passenger_factory.create_passenger(queue_row["passenger_module"]) # pylint: disable=C0301
            passenger.external_id = queue_row["external_id"]
            passenger.internal_id = queue_row["queue_id"]
            passenger.source_system = queue_row["source_system"]
            passenger.puller_module = queue_row["puller_module"]
            passenger.pull_datetime = SqlToDatabus.date_time(queue_row["pulled_on"])

            attachment_list = self._query_helper.select_all("queue_attachment", queue_where)
            for attachment_row in attachment_list:
                if attachment_row["bin_content"] is None:
                    bin_content = None
                else:
                    bin_content = attachment_row["bin_content"]

                if attachment_row["txt_content"] is None:
                    txt_content = None
                else:
                    txt_content = attachment_row["txt_content"]

                attachment = Attachment(
                    p_name=attachment_row["attachment_id"],
                    p_format=SqlToDatabus.attachment_format(attachment_row["file_format"]),
                    p_text_content=txt_content,
                    p_binary_content=bin_content)
                passenger.attachments.append(attachment)

            log_list = self._query_helper.select_all("queue_log", queue_where)
            for log in log_list:
                passenger.collect_log_guid(UUID(log["log_id"]))

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

    def _insert_into_client(self, p_client_id: str, p_log_life_span: int):
        insert = InsertBuilder(self._query_helper.args, p_client_id)
        insert.table = "client"
        insert.add_string("log_life_span", p_log_life_span)
        self._query_helper.execute_insert(insert)
