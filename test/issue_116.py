""" Module to test issue 116
https://github.com/keremkoseoglu/databus/issues/116
"""
from typing import List
from databus.puller.abstract_exchange import AbstractExchange, ExchangeSettings, \
    ExchangeFolder, ExchangeFolderParent
from databus.passenger.abstract_passenger import AbstractPassenger
from databus.client.log import Log

class Exchange116(AbstractExchange):
    """ Test class """
    def notify_passengers_seated(self, p_seated_passengers: List[AbstractPassenger]):
        """ Not needed for this test """

    @property
    def settings(self) -> ExchangeSettings:
        return ExchangeSettings(
            p_email="user@yourexchange.com",
            p_username="user",
            p_password="pass",
            p_server="your_exchange_server.com")

def test116(action: int):
    """ Runs the test for issue 116 """
    log = Log()
    exchange = Exchange116(p_log=log)
    passengers = exchange.pull()

    if passengers is None or len(passengers) <= 0:
        return

    for passenger in passengers:
        if action == 1:
            exchange.delete_seated_passengers_from_inbox([passenger])
            continue
        if action == 2:
            exchange.forward_seated_passengers([passenger], ["kerem.koseoglu@gmail.com"])
            continue
        if action == 3:
            exchange.trash_seated_passengers([passenger])
            continue
        if action == 4:
            folder = ExchangeFolder(ExchangeFolderParent.INBOX, "kktest1")
            exchange.move_seated_passengers([passenger], folder)
            continue
        if action == 5:
            folder = ExchangeFolder(ExchangeFolderParent.ROOT, "kktest2")
            exchange.move_seated_passengers([passenger], folder)
            continue
