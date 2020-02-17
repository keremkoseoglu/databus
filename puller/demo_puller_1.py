from client.log import Log, LogEntry
from passenger.demo_passenger_1 import DemoPassenger1
from puller.abstract_puller import AbstractPuller
from typing import List


class DemoPuller1(AbstractPuller):

    def hello_world(self):
        print("Demo puller 1 says hello world!")

    def pull(self, p_log: Log) -> List[DemoPassenger1]:
        output = []

        passenger1 = DemoPassenger1()
        passenger1.dataset = "Puller 1 pulled first DemoPassenger1"
        output.append(passenger1)
        p_log.entries.append(LogEntry(passenger1.dataset))

        passenger2 = DemoPassenger1()
        passenger2.dataset = "Puller 1 pulled second DemoPassenger1"
        output.append(passenger2)
        p_log.entries.append(LogEntry(passenger2.dataset))

        return output
