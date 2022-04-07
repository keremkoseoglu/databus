""" Demo puller module """
from typing import List
from databus.passenger.abstract_passenger import AbstractPassenger
from databus.passenger.demo.demo_passenger_1 import DemoPassenger1
from databus.passenger.attachment import Attachment, AttachmentFormat
from databus.puller.abstract_puller import AbstractPuller


class DemoPuller1(AbstractPuller):
    """ Demo puller class """

    def notify_passengers_seated(self, p_seated_passengers: List[AbstractPassenger]):
        """ Handles passengers which are queued already """
        for seated_passenger in p_seated_passengers:
            self.log.append_text(
                f"Demo puller 1 notified about seated passenger {seated_passenger.id_text}")

    def pull(self) -> List[DemoPassenger1]:
        """ Fake pull from imaginary source system """
        output = []

        passenger1 = DemoPassenger1()
        passenger1.external_id = "ID_1_1"
        passenger1.dataset = "Puller 1 pulled first DemoPassenger1"
        passenger1.source_system = "DEMO_SYSTEM"
        passenger1.puller_module = self.__module__
        passenger1.attachments.append(Attachment(p_name="puller1_file1.txt",
                                                 p_format=AttachmentFormat.text,
                                                 p_text_content="Lorem Ipsum"))
        output.append(passenger1)
        self.log.append_text(f"Got passenger {passenger1.id_text}")

        passenger2 = DemoPassenger1()
        passenger2.external_id = "ID_1_2"
        passenger2.dataset = "Puller 1 pulled second DemoPassenger1"
        passenger2.source_system = "DEMO_SYSTEM"
        passenger2.puller_module = self.__module__
        output.append(passenger2)
        self.log.append_text(f"Got passenger {passenger2.id_text}")

        return output
