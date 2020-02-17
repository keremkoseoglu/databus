from client.log import Log, LogEntry
from passenger.demo_passenger_2 import DemoPassenger2
from puller.abstract_puller import AbstractPuller
from typing import List


class DemoPuller2(AbstractPuller):

    def hello_world(self):
        print("Demo puller 2 says hello world!")

    def pull(self, p_log: Log) -> List[DemoPassenger2]:
        output = []

        passenger1 = DemoPassenger2()
        passenger1.dataset = "Puller 2 pulled first DemoPassenger2"
        output.append(passenger1)
        p_log.entries.append(LogEntry(passenger1.dataset))

        passenger2 = DemoPassenger2()
        passenger2.dataset = "Puller 2 pulled second DemoPassenger2"
        output.append(passenger2)
        p_log.entries.append(LogEntry(passenger2.dataset))

        return output
