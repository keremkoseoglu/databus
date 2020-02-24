from client.log import Log
from passenger.abstract_passenger import AbstractPassenger
from passenger.demo.demo_passenger_1 import DemoPassenger1
from passenger.attachment import Attachment, AttachmentFormat
from puller.abstract_puller import AbstractPuller
from typing import List


class DemoPuller1(AbstractPuller):

    def hello_world(self):
        print("Demo puller 1 says hello world!")

    def notify_passengers_seated(self, p_seated_passengers: List[AbstractPassenger], p_log: Log):
        for seated_passenger in p_seated_passengers:
            p_log.append_text(("Demo puller 1 notified about seated passenger " + seated_passenger.id_text))

    def pull(self, p_log: Log) -> List[DemoPassenger1]:
        output = []

        passenger1 = DemoPassenger1()
        passenger1.external_id = "ID1"
        passenger1.dataset = "Puller 1 pulled first DemoPassenger1"
        passenger1.source_system = "DEMO_SYSTEM"
        passenger1.puller_module = self.__module__
        passenger1.attachments.append(Attachment(p_name="abc.txt",
                                                 p_format=AttachmentFormat.text,
                                                 p_text_content="Lorem Ipsum"))
        output.append(passenger1)
        p_log.append_text("Got passenger " + passenger1.id_text)

        passenger2 = DemoPassenger1()
        passenger2.external_id = "ID2"
        passenger2.dataset = "Puller 1 pulled second DemoPassenger1"
        passenger2.source_system = "DEMO_SYSTEM"
        passenger2.puller_module = self.__module__
        output.append(passenger2)
        p_log.append_text("Got passenger " + passenger2.id_text)

        return output
