from client.log import Log
from config.constants import *
import json
from os import path, remove
from passenger.abstract_passenger import AbstractPassenger
from passenger.attachment import Attachment, AttachmentFormat
from passenger.factory import PassengerFactory
from pqueue.queue_status import QueueStatus
from typing import List


class JsonQueue:
    client_id: str

    def __init__(self, p_client_id: str):
        # todo: ilgili yordamlarda log tut
        self.client_id = p_client_id

    def delete_passengers(self, p_passengers: List[AbstractPassenger], p_log: Log):
        passengers_json = self._get_passenger_file_as_json()
        deletable_indices = []
        json_index = -1
        for passenger_json in passengers_json:
            json_index += 1
            for passenger in p_passengers:
                if passenger_json["internal_id"] == passenger.internal_id:
                    deletable_indices.append(json_index)

        sorted(deletable_indices, reverse=True)

        for json_index in deletable_indices:
            deletable_json = passengers_json.pop(json_index)
            for attachment in deletable_json["attachments"]:
                self._delete_attachment_file(attachment["file_name"])

        self._write_passenger_json_into_file(passengers_json)

    def get_passengers(self,
                       p_status: QueueStatus,
                       p_passenger_module: str,
                       p_log: Log) -> List[AbstractPassenger]:
        output = []
        passengers_json = self._get_passenger_file_as_json()

        for passenger_json in passengers_json:
            if passenger_json["passenger_module"] == p_passenger_module and passenger_json["status"] == p_status.name:
                passenger_obj = PassengerFactory.create_passenger(passenger_json["passenger_module"])
                passenger_obj.internal_id = passenger_json["internal_id"]
                passenger_obj.external_id = passenger_json["external_id"]
                passenger_obj.source_system = passenger_json["source_system"]

                for attachment_json in passenger_json["attachments"]:
                    attachment_obj = Attachment(p_name=attachment_json["name"],
                                                p_format=AttachmentFormat[attachment_json["format"]])
                    passenger_obj.attachments.append(attachment_obj)

                output.append(passenger_obj)
        return output

    def insert_passengers(self, p_passengers: List[AbstractPassenger], p_log: Log):
        passengers_json = self._get_passenger_file_as_json()
        for passenger in p_passengers:
            passenger_dict = {
                "external_id": passenger.external_id,
                "internal_id": str(passenger.internal_id),
                "source_system": passenger.source_system,
                "passenger_module": passenger.__module__,
                "status": QueueStatus.undelivered.name,
                "attachments": []
            }

            for attachment in passenger.attachments:
                # todo: attachment bir başka dosyayı ezmemeli, dosya adında internal ID olmasını sağla
                attachment_dict = {
                    "format": attachment.format.name,
                    "name": attachment.name
                }

                passenger_dict["attachments"].append(attachment_dict)

                if attachment.format == AttachmentFormat.binary:
                    self._write_attachment_file_bin(
                        p_file_name=attachment_dict["name"],
                        p_file_content=attachment.binary_content)
                elif attachment.format == AttachmentFormat.text:
                    self._write_attachment_file_text(
                        p_file_name=attachment_dict["name"],
                        p_file_content=attachment.text_content)
                else:
                    # todo: exception ve pass sil
                    pass

            passengers_json.append(passenger_dict)

        self._write_passenger_json_into_file(passengers_json)

    def set_passenger_status(self, p_passengers: List[AbstractPassenger], p_status: QueueStatus, p_log: Log):
        passengers_json = self._get_passenger_file_as_json()

        for passenger_json in passengers_json:
            for passenger in p_passengers:
                if passenger_json["internal_id"] == passenger.internal_id:
                    passenger_json["status"] = p_status.name

        self._write_passenger_json_into_file(passengers_json)

    def _delete_attachment_file(self, p_file_name: str):

        full_path = self._get_attachment_file_path(p_file_name)
        if not path.exists(full_path):
            return
        remove(full_path)

    def _get_attachment_file_path(self, p_file_name: str) -> str:
        return path.join(self._get_queue_file_path(),
                         p_file_name)

    def get_passenger_file_path(self) -> str:
        return path.join(self._get_queue_file_path(), JSON_DB_QUEUE_PASSENGER)

    def _get_passenger_file_as_json(self) -> list:
        passenger_file_path = self.get_passenger_file_path()
        with open(passenger_file_path) as json_file:
            passengers_json = json.load(json_file)
        return passengers_json

    def _get_queue_file_path(self) -> str:
        return path.join(JSON_DB_DATABASE_DIR,
                         JSON_DB_CLIENT_DIR,
                         self.client_id,
                         JSON_DB_QUEUE_DIR)

    def _write_attachment_file_text(self, p_file_name: str, p_file_content: str):
        full_path = self._get_attachment_file_path(p_file_name)
        with open(full_path, "w") as text_file:
            text_file.write(p_file_content)

    def _write_attachment_file_bin(self, p_file_name: str, p_file_content: bytearray):
        full_path = self._get_attachment_file_path(p_file_name)
        with open(full_path, "wb") as bin_file:
            bin_file.write(p_file_content)

    def _write_passenger_json_into_file(self, p_json: list):
        passenger_file_path = self.get_passenger_file_path()
        with open(passenger_file_path, "w") as json_file:
            json.dump(p_json, json_file)


