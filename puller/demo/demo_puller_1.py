from client.log import Log
from passenger.demo.demo_passenger_1 import DemoPassenger1
from passenger.attachment import Attachment, AttachmentFormat
from puller.abstract_puller import AbstractPuller
from typing import List


class DemoPuller1(AbstractPuller):

    def hello_world(self):
        print("Demo puller 1 says hello world!")

    def pull(self, p_log: Log) -> List[DemoPassenger1]:
        output = []

        passenger1 = DemoPassenger1()
        passenger1.external_id = "ID1"
        passenger1.dataset = "Puller 1 pulled first DemoPassenger1"
        passenger1.attachments.append(Attachment(p_name="abc.txt",
                                                 p_format=AttachmentFormat.text,
                                                 p_text_content="Lorem Ipsum"))
        output.append(passenger1)
        p_log.append(passenger1.dataset)

        passenger2 = DemoPassenger1()
        passenger2.external_id = "ID2"
        passenger2.dataset = "Puller 1 pulled second DemoPassenger1"
        output.append(passenger2)
        p_log.append(passenger2.dataset)

        return output
