from client.log import Log, LogEntry, MessageType
from config.constants import *
from datetime import datetime
from enum import Enum
import json
from os import mkdir, path, remove, scandir
from passenger.abstract_passenger import AbstractPassenger
from passenger.attachment import Attachment, AttachmentFormat
from passenger.abstract_factory import AbstractPassengerFactory
from pqueue.queue_status import QueueStatus, PassengerQueueStatus, ProcessorQueueStatus, PusherQueueStatus
import shutil
from typing import List


class PassengerError(Exception):
    class ErrorCode(Enum):
        internal_id_missing = 1

    def __init__(self, p_error_code: ErrorCode, p_passenger_id: str = ""):
        self.error_code = p_error_code

        if p_passenger_id is None:
            self.passenger_id = ""
        else:
            self.passenger_id = p_passenger_id

    @property
    def message(self) -> str:
        if self.error_code == PassengerError.ErrorCode.internal_id_missing:
            return "Passenger " + self.passenger_id + " is missing internal ID"
        return "Passenger error"


class JsonQueue:
    class DataOperation(Enum):
        insert = 1
        update = 2

    client_id: str

    @staticmethod
    def _validate_passenger_status(p_passenger_status: PassengerQueueStatus, p_operation: DataOperation):
        if str(p_passenger_status.passenger.internal_id) == "":
            raise PassengerError(PassengerError.ErrorCode.internal_id_missing,
                                 p_passenger_id=p_passenger_status.passenger.id_text)

        # todo
        # başka kritik alan eksikse hata döndür
        # ismi aynı attachment'lar varsa hata üret
        # attachment format validasyonu

        if p_operation == JsonQueue.DataOperation.insert:
            # todo
            # böyle bir klasör zaten varsa exception döndür
            # pass sil
            pass

    def __init__(self, p_client_id: str, p_log: Log, p_passenger_factory: AbstractPassengerFactory):
        self.client_id = p_client_id
        self._log = p_log
        self._passenger_factory = p_passenger_factory

    def delete_passengers(self, p_passengers: List[AbstractPassenger]):
        all_passenger_directories = self._get_passenger_directories()
        for passenger in p_passengers:
            if passenger.internal_id in all_passenger_directories:
                self._log.append_text("Deleting passenger directory " + passenger.internal_id)
                passenger_dir_path = self._get_passenger_directory_path(passenger.internal_id)
                shutil.rmtree(passenger_dir_path)

    def erase_passenger_queue(self):
        all_passenger_directories = self._get_passenger_directories()
        for passenger_directory in all_passenger_directories:
            self._log.append_text("Deleting passenger directory " + passenger_directory)
            passenger_dir_path = self._get_passenger_directory_path(passenger_directory)
            shutil.rmtree(passenger_dir_path)

    def get_passengers(self,
                       p_passenger_module: str = None,
                       p_processor_status: QueueStatus = None,
                       p_pusher_status: QueueStatus = None,
                       p_puller_notified: bool = None,
                       p_pulled_before: datetime = None
                       ) -> List[PassengerQueueStatus]:
        output = []

        # todo
        # processor status valide edecek yordam yazıp çağır
        # pusher status valide edecek yordamı yazıp çağır

        for passenger_directory in self._get_passenger_directories():
            passenger_json = self._get_passenger_file_as_json(passenger_directory)

            if p_pusher_status is not None:
                a_pusher_found = False
                for pusher_status in passenger_json["pusher_statuses"]:
                    if pusher_status["status"] == p_pusher_status.name:
                        a_pusher_found = True
                        break
                if not a_pusher_found:
                    continue

            if p_processor_status is not None:
                a_processor_found = False
                for processor_status in passenger_json["processor_statuses"]:
                    if processor_status["status"] == p_processor_status.name:
                        a_processor_found = True
                        break
                if not a_processor_found:
                    continue

            if p_passenger_module is not None and passenger_json["passenger_module"] != p_passenger_module:
                continue

            if p_puller_notified is not None and passenger_json["puller_notified"] != p_puller_notified:
                continue

            if p_pulled_before is not None and passenger_json["pull_datetime"] > p_pulled_before:
                continue

            passenger_obj = self._passenger_factory.create_passenger(passenger_json["passenger_module"])
            passenger_obj.internal_id = passenger_json["internal_id"]
            passenger_obj.external_id = passenger_json["external_id"]
            passenger_obj.source_system = passenger_json["source_system"]
            passenger_obj.puller_module = passenger_json["puller_module"]
            passenger_obj.pull_datetime = datetime.strptime(passenger_json["pull_datetime"], '%Y-%m-%dT%H:%M:%S.%f')
            self._log.append_text("Found passenger " + passenger_obj.id_text)

            for attachment_json in passenger_json["attachments"]:
                # todo burada attachment içeriklerini de okuyup koymalısın
                attachment_obj = Attachment(p_name=attachment_json["name"],
                                            p_format=AttachmentFormat[attachment_json["format"]])
                passenger_obj.attachments.append(attachment_obj)

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
        self._log.append_text("Adding passenger " + p_passenger_status.passenger.id_text + " to queue")
        JsonQueue._validate_passenger_status(p_passenger_status, JsonQueue.DataOperation.insert)

        passenger_dict = {
            "external_id": p_passenger_status.passenger.external_id,
            "internal_id": str(p_passenger_status.passenger.internal_id),
            "source_system": p_passenger_status.passenger.source_system,
            "passenger_module": p_passenger_status.passenger.__module__,
            "puller_module": p_passenger_status.passenger.puller_module,
            "puller_notified": p_passenger_status.puller_notified,
            "pull_datetime": p_passenger_status.passenger.pull_datetime.isoformat(),
            "attachments": [],
            "processor_statuses": [],
            "pusher_statuses": []
        }

        mkdir(self._get_passenger_directory_path(passenger_dict["internal_id"]))
        mkdir(self._get_attachment_directory_path(passenger_dict["internal_id"]))

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
                assert False  # Bu daha önce kontrol edilmiş olmalı

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

        self._log.append_text("Setting status " +
                              p_status.name +
                              " for passenger " +
                              p_passenger.id_text +
                              " processor " +
                              p_processor_module)

        # todo
        # processor module valide edecek yordam yazıp çağır
        # status valide edecek yordam yazıp çağır

        passenger_json = self._get_passenger_file_as_json(p_passenger.internal_id)

        for processor_status in passenger_json["processor_statuses"]:
            if processor_status["processor_module"] == p_processor_module:
                processor_status["status"] = p_status.name

        self._write_passenger_json_into_file(passenger_json)

    def set_pusher_status(self,
                          p_passenger: AbstractPassenger,
                          p_pusher_module: str,
                          p_status: QueueStatus):

        # todo
        # pusher module valide edecek yordam yazıp çağır
        # status valide edecek yordam yazıp çağır

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
        self._log.append_text("Updating passenger " + p_passenger_status.passenger.id_text)
        JsonQueue._validate_passenger_status(p_passenger_status, JsonQueue.DataOperation.update)
        self.delete_passengers([p_passenger_status.passenger])
        self.insert_passenger(p_passenger_status)

    def _delete_attachment_file(self, p_file_name: str, p_internal_id: str):
        self._log.append_text("Deleting attachment " + p_file_name)

        full_path = self._get_attachment_file_path(p_file_name, p_internal_id)
        if not path.exists(full_path):
            self._log.append_entry(LogEntry(p_message="File not found", p_type=MessageType.warning))
            return
        remove(full_path)

    def _get_attachment_file_path(self, p_file_name: str, p_internal_id: str) -> str:
        return path.join(self._get_attachment_directory_path(p_internal_id), p_file_name)

    def _get_attachment_directory_path(self, p_internal_id: str) -> str:
        return path.join(self._get_queue_root_path(), p_internal_id, JSON_DB_QUEUE_ATTACHMENT_DIR)

    def _get_passenger_file_as_json(self, p_internal_id: str) -> dict:
        passenger_file_path = self._get_passenger_file_path(p_internal_id)
        self._log.append_text("Reading passenger file " + passenger_file_path)
        with open(passenger_file_path) as json_file:
            passengers_json = json.load(json_file)
        return passengers_json

    def _get_passenger_file_path(self, p_internal_id: str) -> str:
        return path.join(self._get_queue_root_path(), p_internal_id, JSON_DB_QUEUE_PASSENGER)

    def _get_passenger_directories(self) -> List[str]:
        return [f.name for f in scandir(self._get_queue_root_path()) if f.is_dir()]

    def _get_passenger_directory_path(self, p_internal_id: str) -> str:
        return path.join(self._get_queue_root_path(), p_internal_id)

    def _get_queue_root_path(self) -> str:
        return path.join(JSON_DB_DATABASE_DIR,
                         JSON_DB_CLIENT_DIR,
                         self.client_id,
                         JSON_DB_QUEUE_DIR)

    def _write_attachment_file_text(self, p_file_name: str, p_file_content: str, p_internal_id: str):
        full_path = self._get_attachment_file_path(p_file_name, p_internal_id)
        self._log.append_text("Writing text attachment to disk: " + full_path)
        with open(full_path, "w") as text_file:
            text_file.write(p_file_content)

    def _write_attachment_file_bin(self, p_file_name: str, p_file_content: bytearray, p_internal_id: str):
        full_path = self._get_attachment_file_path(p_file_name, p_internal_id)
        self._log.append_text("Writing binary attachment to disk: " + full_path)
        with open(full_path, "wb") as bin_file:
            bin_file.write(p_file_content)

    def _write_passenger_json_into_file(self, p_json: dict):
        passenger_file_path = self._get_passenger_file_path(p_json["internal_id"])
        self._log.append_text("Writing passenger file to disk: " + passenger_file_path)
        with open(passenger_file_path, "w") as json_file:
            json.dump(p_json, json_file)


