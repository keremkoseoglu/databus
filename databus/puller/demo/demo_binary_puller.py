""" Demo puller module returning binary attachments """
from os import path
from typing import List
from databus.passenger.abstract_passenger import AbstractPassenger
from databus.passenger.demo.demo_binary_passenger import DemoBinaryPassenger
from databus.passenger.attachment import Attachment, AttachmentFormat
from databus.puller.abstract_puller import AbstractPuller

class DemoBinaryPuller(AbstractPuller):
    """ Demo binary puller class """
    _BIN_FILE_NAME = "sample_binary_file.png"
    _MODULE_FILE_NAME = "demo_binary_puller.py"

    def notify_passengers_seated(self, p_seated_passengers: List[AbstractPassenger]):
        """ Handles passengers which are queued already """
        for seated_passenger in p_seated_passengers:
            self.log.append_text(
                "Demo binary puller notified about seated passenger " + seated_passenger.id_text)

    def pull(self) -> List[DemoBinaryPassenger]:
        """ Fake pull from imaginary source system """
        output = []
        passenger1 = DemoBinaryPassenger()
        passenger1.external_id = "ID_BIN_1"
        passenger1.source_system = "DEMO_SYSTEM"
        passenger1.puller_module = self.__module__
        passenger1.attachments.append(Attachment(
            p_name=DemoBinaryPuller._BIN_FILE_NAME,
            p_format=AttachmentFormat.binary,
            p_binary_content=DemoBinaryPuller._get_sample_binary()))
        output.append(passenger1)
        self.log.append_text(f"Got passenger {passenger1.id_text}")
        return output

    @staticmethod
    def _get_sample_binary() -> bytearray:
        """ Returns the binary content of the sample file """
        full_path = path.abspath(__file__).replace(
            DemoBinaryPuller._MODULE_FILE_NAME,
            DemoBinaryPuller._BIN_FILE_NAME)
        with open(full_path, "rb") as bin_file:
            binary_content = bin_file.read()
        return binary_content
