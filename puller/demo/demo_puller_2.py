from passenger.abstract_passenger import AbstractPassenger
from passenger.demo.demo_passenger_2 import DemoPassenger2
from puller.abstract_puller import AbstractPuller
from typing import List


class DemoPuller2(AbstractPuller):

    def notify_passengers_seated(self, p_seated_passengers: List[AbstractPassenger]):
        for seated_passenger in p_seated_passengers:
            self.log.append_text(("Demo puller 2 notified about seated passenger " + seated_passenger.id_text))

    def pull(self) -> List[DemoPassenger2]:
        output = []

        passenger1 = DemoPassenger2()
        passenger1.external_id = "ID_2_1"
        passenger1.dataset = "Puller 2 pulled first DemoPassenger2"
        passenger1.source_system = "DEMO_SYSTEM"
        passenger1.puller_module = self.__module__
        output.append(passenger1)
        self.log.append_text("Got passenger " + passenger1.id_text)

        passenger2 = DemoPassenger2()
        passenger2.external_id = "ID_2_2"
        passenger2.dataset = "Puller 2 pulled second DemoPassenger2"
        passenger2.source_system = "DEMO_SYSTEM"
        passenger2.puller_module = self.__module__
        output.append(passenger2)
        self.log.append_text("Got passenger " + passenger2.id_text)

        return output
