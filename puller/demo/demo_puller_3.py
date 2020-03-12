from passenger.abstract_passenger import AbstractPassenger
from passenger.demo.demo_passenger_1 import DemoPassenger1
from passenger.attachment import Attachment, AttachmentFormat
from puller.abstract_puller import AbstractPuller
from typing import List


class DemoPuller3(AbstractPuller):

    def notify_passengers_seated(self, p_seated_passengers: List[AbstractPassenger]):
        for seated_passenger in p_seated_passengers:
            self.log.append_text(("Demo puller 3 notified about seated passenger " + seated_passenger.id_text))

    def pull(self) -> List[DemoPassenger1]:
        output = []

        passenger1 = DemoPassenger1()
        passenger1.external_id = "ID_3_1"
        passenger1.dataset = "Puller 3 pulled first DemoPassenger1"
        passenger1.source_system = "DEMO_SYSTEM"
        passenger1.puller_module = self.__module__
        passenger1.attachments.append(Attachment(p_name="puller3_file1.txt",
                                                 p_format=AttachmentFormat.text,
                                                 p_text_content="Lorem Ipsum"))
        output.append(passenger1)
        self.log.append_text("Got passenger " + passenger1.id_text)

        return output
