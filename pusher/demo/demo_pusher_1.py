from client.log import Log, LogEntry
from passenger.abstract_passenger import AbstractPassenger
from pusher.abstract_pusher import AbstractPusher
from typing import List


class DemoPusher1(AbstractPusher):

    def hello_world(self):
        print("Demo pusher 1 says hello world!")

    def push(self, p_log: Log, p_passengers: List[AbstractPassenger]):
        p_log.append("Pusher 1 did its job")

