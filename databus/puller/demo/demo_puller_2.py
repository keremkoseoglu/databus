""" Demo puller module """
from typing import List
from databus.passenger.abstract_passenger import AbstractPassenger
from databus.passenger.demo.demo_passenger_2 import DemoPassenger2
from databus.puller.abstract_puller import AbstractPuller


class DemoPuller2(AbstractPuller):
    """ Demo puller class """

    def notify_passengers_seated(self, p_seated_passengers: List[AbstractPassenger]):
        """ Fake operation """
        for seated_passenger in p_seated_passengers:
            self.log.append_text(
                f"Demo puller 2 notified about seated passenger {seated_passenger.id_text}")

    def pull(self) -> List[DemoPassenger2]:
        """ Fake operation """
        output = []

        passenger1 = DemoPassenger2()
        passenger1.external_id = "ID_2_1"
        passenger1.dataset = "Puller 2 pulled first DemoPassenger2"
        passenger1.source_system = "DEMO_SYSTEM"
        passenger1.puller_module = self.__module__
        output.append(passenger1)
        self.log.append_text(f"Got passenger {passenger1.id_text}")

        passenger2 = DemoPassenger2()
        passenger2.external_id = "ID_2_2"
        passenger2.dataset = "Puller 2 pulled second DemoPassenger2"
        passenger2.source_system = "DEMO_SYSTEM"
        passenger2.puller_module = self.__module__
        output.append(passenger2)
        self.log.append_text(f"Got passenger {passenger2.id_text}")

        return output
