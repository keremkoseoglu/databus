""" Queue module for JSON database """
from datetime import datetime
from enum import Enum
import json
from os import mkdir, path, remove
import shutil
from typing import List
import uuid
from databus.client.log import Log, LogEntry, MessageType
from databus.database.json_db.json_database_arguments import JsonDatabaseArguments
from databus.database.json_db.json_path_builder import JsonPathBuilder
from databus.database.json_db.json_toolkit import JsonToolkit
from databus.passenger.abstract_passenger import AbstractPassenger
from databus.passenger.attachment import Attachment, AttachmentError, AttachmentFormat
from databus.passenger.attachment import Validator as AttachmentValidator
from databus.passenger.abstract_factory import AbstractPassengerFactory
from databus.pqueue.queue_status import \
    QueueStatus, PassengerQueueStatus, ProcessorQueueStatus, PusherQueueStatus
from databus.pqueue.queue_status import Validator as QueueStatusValidator



class PassengerError(Exception):
    """ Base exception class for passenger errors """
    class ErrorCode(Enum):
        """ Error code enum """
        internal_id_missing = 1
        puller_module_missing = 2
        already_exists = 3

    def __init__(self, p_error_code: ErrorCode, p_passenger_id: str = None):
        super().__init__()
        self.error_code = p_error_code

        if p_passenger_id is None:
            self.passenger_id = ""
        else:
            self.passenger_id = p_passenger_id

    @property
    def message(self) -> str:
        """ Returns error message as text """
        if self.error_code == PassengerError.ErrorCode.internal_id_missing:
            return "Passenger " + self.passenger_id + " is missing internal ID"
        if self.error_code == PassengerError.ErrorCode.puller_module_missing:
            return "Passenger " + self.passenger_id + " is missing puller module"
        if self.error_code == PassengerError.ErrorCode.already_exists:
            return "Passenger " + self.passenger_id + " exists already"
        return "Passenger error"


class JsonQueue:
    """ Queue implementation for JSON database """
    class DataOperation(Enum):
        """ Data operation enum """
        insert = 1
        update = 2

    def __init__(self,
                 p_client_id: str,
                 p_log: Log,
                 p_passenger_factory: AbstractPassengerFactory,
                 p_args: JsonDatabaseArguments):
        self.client_id = p_client_id
        self._log = p_log
        self._passenger_factory = p_passenger_factory
        self._args = p_args
        self._path = JsonPathBuilder(self.client_id, self._args)

    def delete_passengers(self, p_passengers: List[AbstractPassenger]):
        """ Deletes the given passengers from the disk """
        all_passenger_directories = self._path.passenger_directories
        for passenger in p_passengers:
            if passenger.internal_id in all_passenger_directories:
                self._log.append_text("Deleting passenger directory " + passenger.internal_id)
                passenger_dir_path = self._path.get_passenger_directory_path(passenger.internal_id)
                shutil.rmtree(passenger_dir_path)

    def erase_passenger_queue(self):
        """ Deletes all passengers from the disk """
        all_passenger_directories = self._path.passenger_directories
        for passenger_directory in all_passenger_directories:
            self._log.append_text("Deleting passenger directory " + passenger_directory)
            passenger_dir_path = self._path.get_passenger_directory_path(passenger_directory)
            shutil.rmtree(passenger_dir_path)

    def get_passengers(self, # pylint: disable=R0912, R0913, R0914
                       p_passenger_module: str = None,
                       p_processor_status: QueueStatus = None,
                       p_pusher_status: QueueStatus = None,
                       p_puller_notified: bool = None,
                       p_pulled_before: datetime = None,
                       p_internal_id: str = None
                       ) -> List[PassengerQueueStatus]:
        """ Returns passengers """
        output = []

        for passenger_directory in self._path.passenger_directories:
            if p_internal_id is not None and passenger_directory != p_internal_id:
                continue

            passenger_json = self._get_passenger_file_as_json(passenger_directory)
            pull_datetime = JsonToolkit.convert_json_date_to_datetime(passenger_json["pull_datetime"]) # pylint: disable=C0301

            if p_pusher_status is not None and len(passenger_json["pusher_statuses"]) > 0:
                a_pusher_found = False
                for pusher_status in passenger_json["pusher_statuses"]:
                    if pusher_status["status"] == p_pusher_status.name:
                        a_pusher_found = True
                        break
                if not a_pusher_found:
                    continue

            if p_processor_status is not None and len(passenger_json["processor_statuses"]) > 0:
                a_processor_found = False
                for processor_status in passenger_json["processor_statuses"]:
                    if processor_status["status"] == p_processor_status.name:
                        a_processor_found = True
                        break
                if not a_processor_found:
                    continue

            if p_passenger_module is not None and passenger_json["passenger_module"] != p_passenger_module: # pylint: disable=C0301
                continue

            if p_puller_notified is not None and passenger_json["puller_notified"] != p_puller_notified: # pylint: disable=C0301
                continue

            if p_pulled_before is not None and pull_datetime > p_pulled_before:
                continue

            passenger_obj = self._passenger_factory.create_passenger(passenger_json["passenger_module"]) # pylint: disable=C0301
            passenger_obj.internal_id = passenger_json["internal_id"]
            passenger_obj.external_id = passenger_json["external_id"]
            passenger_obj.source_system = passenger_json["source_system"]
            passenger_obj.puller_module = passenger_json["puller_module"]
            passenger_obj.pull_datetime = pull_datetime
            self._log.append_text("Found passenger " + passenger_obj.id_text)

            for attachment_json in passenger_json["attachments"]:
                attachment_obj = self._get_attachment_obj(passenger_obj.internal_id,
                                                          attachment_json)
                passenger_obj.attachments.append(attachment_obj)

            if "log_guids" in passenger_json:
                for log_guid in passenger_json["log_guids"]:
                    passenger_obj.collect_log_guid(uuid.UUID(log_guid))

            paqs = PassengerQueueStatus(p_passenger=passenger_obj,
                                        p_pusher_statuses=[],
                                        p_processor_statuses=[])

            paqs.puller_notified = passenger_json["puller_notified"]

            for processor_status in passenger_json["processor_statuses"]:
                paqs.processor_statuses.append(ProcessorQueueStatus(
                    p_processor_module=processor_status["processor_module"],
                    p_status=QueueStatus[processor_status["status"]]))

            for pusher_status in passenger_json["pusher_statuses"]:
                paqs.pusher_statuses.append(PusherQueueStatus(
                    p_pusher_module=pusher_status["pusher_module"],
                    p_status=QueueStatus[pusher_status["status"]]))

            output.append(paqs)
        return output

    def insert_passenger(self, p_passenger_status: PassengerQueueStatus):
        """ Creates a new folder & puts files within """
        self._log.append_text("Adding passenger " + p_passenger_status.passenger.id_text + " to queue") # pylint: disable=C0301
        self._validate_passenger_status(p_passenger_status, JsonQueue.DataOperation.insert)

        passenger_dict = {
            "external_id": p_passenger_status.passenger.external_id,
            "internal_id": str(p_passenger_status.passenger.internal_id),
            "source_system": p_passenger_status.passenger.source_system,
            "passenger_module": p_passenger_status.passenger.passenger_module,
            "puller_module": p_passenger_status.passenger.puller_module,
            "puller_notified": p_passenger_status.puller_notified,
            "pull_datetime": p_passenger_status.passenger.pull_datetime.isoformat(),
            "attachments": [],
            "log_guids": [],
            "processor_statuses": [],
            "pusher_statuses": []
        }

        mkdir(self._path.get_passenger_directory_path(passenger_dict["internal_id"]))
        mkdir(self._path.get_attachment_directory_path(passenger_dict["internal_id"]))

        for attachment in p_passenger_status.passenger.attachments:
            attachment_dict = {
                "format": attachment.format.name,
                "name": attachment.name
            }
            passenger_dict["attachments"].append(attachment_dict)

            if attachment.format == AttachmentFormat.binary:
                self._write_attachment_file_bin(attachment_dict["name"],
                                                attachment.binary_content,
                                                passenger_dict["internal_id"])
            elif attachment.format == AttachmentFormat.text:
                self._write_attachment_file_text(attachment_dict["name"],
                                                 attachment.text_content,
                                                 passenger_dict["internal_id"])
            else:
                raise AttachmentError(AttachmentError.ErrorCode.invalid_format, attachment.format)

        for guid in p_passenger_status.passenger.log_guids:
            passenger_dict["log_guids"].append(str(guid))

        for processor_status in p_passenger_status.processor_statuses:
            processor_status_dict = {
                "processor_module": processor_status.processor_module,
                "status": processor_status.status.name
            }
            passenger_dict["processor_statuses"].append(processor_status_dict)

        for pusher_status in p_passenger_status.pusher_statuses:
            pusher_status_dict = {
                "pusher_module": pusher_status.pusher_module,
                "status": pusher_status.status.name
            }
            passenger_dict["pusher_statuses"].append(pusher_status_dict)

        self._write_passenger_json_into_file(passenger_dict)

    def set_processor_status(self,
                             p_passenger: AbstractPassenger,
                             p_processor_module: str,
                             p_status: QueueStatus):
        """ Updates processor status within the JSON file """

        self._log.append_text("Setting status " +
                              p_status.name +
                              " for passenger " +
                              p_passenger.id_text +
                              " processor " +
                              p_processor_module)

        passenger_json = self._get_passenger_file_as_json(p_passenger.internal_id)

        for processor_status in passenger_json["processor_statuses"]:
            if processor_status["processor_module"] == p_processor_module:
                processor_status["status"] = p_status.name

        self._write_passenger_json_into_file(passenger_json)

    def set_pusher_status(self,
                          p_passenger: AbstractPassenger,
                          p_pusher_module: str,
                          p_status: QueueStatus):
        """ Updates pusher status within the JSON file """
        self._log.append_text("Setting status " +
                              p_status.name +
                              " for passenger " +
                              p_passenger.id_text +
                              " pusher " +
                              p_pusher_module)

        passenger_json = self._get_passenger_file_as_json(p_passenger.internal_id)

        for pusher_status in passenger_json["pusher_statuses"]:
            if pusher_status["pusher_module"] == p_pusher_module:
                pusher_status["status"] = p_status.name

        self._write_passenger_json_into_file(passenger_json)

    def update_passenger(self, p_passenger_status: PassengerQueueStatus):
        """ Updates passenger """
        self._log.append_text("Updating passenger " + p_passenger_status.passenger.id_text)
        self._validate_passenger_status(p_passenger_status, JsonQueue.DataOperation.update)
        self.delete_passengers([p_passenger_status.passenger])
        self.insert_passenger(p_passenger_status)

    def _delete_attachment_file(self, p_file_name: str, p_internal_id: str):
        self._log.append_text("Deleting attachment " + p_file_name)

        full_path = self._path.get_attachment_file_path(p_internal_id, p_file_name)
        if not path.exists(full_path):
            self._log.append_entry(LogEntry(p_message="File not found", p_type=MessageType.warning))
            return
        remove(full_path)

    def _get_attachment_obj(self, p_internal_id: str, p_attachment_json: {}) -> Attachment:
        output = Attachment(p_name=p_attachment_json["name"],
                            p_format=AttachmentFormat[p_attachment_json["format"]])

        full_path = self._path.get_attachment_file_path(p_internal_id, output.name)
        self._log.append_text("Reading attachment from disk: " + full_path)

        if output.format == AttachmentFormat.text:
            with open(full_path, "r") as text_file:
                output.text_content = text_file.read()
        elif output.format == AttachmentFormat.binary:
            with open(full_path, "rb") as bin_file:
                output.binary_content = bin_file.read()
        else:
            raise AttachmentError(AttachmentError.ErrorCode.invalid_format, output.format)

        return output

    def _get_passenger_file_as_json(self, p_internal_id: str) -> dict:
        try:
            passenger_file_path = self._path.get_passenger_file_path(p_internal_id)
            self._log.append_text("Reading passenger file " + passenger_file_path)
            with open(passenger_file_path) as json_file:
                passengers_json = json.load(json_file)
            return passengers_json
        except Exception as error: # pylint: disable=W0703
            print(str(error))
            return {}

    def _validate_passenger_status(self,
                                   p_passenger_status: PassengerQueueStatus,
                                   p_operation: DataOperation):
        self._log.append_text("Validating passenger status for " + p_passenger_status.passenger.id_text) # pylint: disable=C0301

        if str(p_passenger_status.passenger.internal_id) == "":
            raise PassengerError(PassengerError.ErrorCode.internal_id_missing,
                                 p_passenger_id=p_passenger_status.passenger.id_text)

        QueueStatusValidator.validate_queue_module(
            "Puller",
            p_passenger_status.passenger.id_text,
            p_passenger_status.passenger.puller_module)

        for processor_status in p_passenger_status.processor_statuses:
            QueueStatusValidator.validate_queue_module(
                "Processor",
                p_passenger_status.passenger.id_text,
                processor_status.processor_module)

        for pusher_status in p_passenger_status.pusher_statuses:
            QueueStatusValidator.validate_queue_module(
                "Pusher",
                p_passenger_status.passenger.id_text,
                pusher_status.pusher_module)

        AttachmentValidator.validate_attachments(p_passenger_status.passenger.attachments)

        if p_operation == JsonQueue.DataOperation.insert and \
                p_passenger_status.passenger.internal_id in self._path.passenger_directories:
            raise PassengerError(PassengerError.ErrorCode.already_exists,
                                 p_passenger_status.passenger.id_text)

    def _write_attachment_file_text(self,
                                    p_file_name: str,
                                    p_file_content: str,
                                    p_internal_id: str):
        full_path = self._path.get_attachment_file_path(p_internal_id, p_file_name)
        self._log.append_text("Writing text attachment to disk: " + full_path)
        with open(full_path, "w") as text_file:
            text_file.write(p_file_content)

    def _write_attachment_file_bin(self,
                                   p_file_name: str,
                                   p_file_content: bytearray,
                                   p_internal_id: str):
        full_path = self._path.get_attachment_file_path(p_internal_id, p_file_name)
        self._log.append_text("Writing binary attachment to disk: " + full_path)
        with open(full_path, "wb") as bin_file:
            bin_file.write(p_file_content)

    def _write_passenger_json_into_file(self, p_json: dict):
        passenger_file_path = self._path.get_passenger_file_path(p_json["internal_id"])
        self._log.append_text("Writing passenger file to disk: " + passenger_file_path)
        with open(passenger_file_path, "w") as json_file:
            json.dump(p_json, json_file)
