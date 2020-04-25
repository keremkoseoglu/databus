""" Module for peeking into puller inboxes """
from typing import List
from databus.client.client import Client
from databus.dispatcher.abstract_dispatcher import AbstractDispatcher
from databus.passenger.abstract_passenger import AbstractPassenger, Attachment


class PullerPeekResult: # pylint: disable=R0903
    """ Result of a pullers peek operation """
    def __init__(self, p_puller_module: str = "", p_passengers: List[AbstractPassenger] = None):
        self.puller_module = p_puller_module
        if p_passengers is None:
            self.passengers = []
        else:
            self.passengers = p_passengers


class ClientPeekResult: # pylint: disable=R0903
    """ Result of a clients peek operation """
    def __init__(self, p_client: Client = None, p_results: List[PullerPeekResult] = None):
        if p_client is None:
            self.client = Client()
        else:
            self.client = p_client

        if p_results is None:
            self.results = []
        else:
            self.results = p_results


class PullerPeek: # pylint: disable=R0903
    """ Class to peek into puller inboxes """
    def __init__(self, p_dispatcher: AbstractDispatcher):
        self._dispatcher = p_dispatcher

    def get_attachment(self,
                       p_client_id: str,
                       p_puller_module: str,
                       p_external_id: str,
                       p_attachment_name: str) -> Attachment:
        """ Returns an attachment """
        passenger = self.get_passenger(
            p_client_id=p_client_id,
            p_puller_module=p_puller_module,
            p_external_id=p_external_id)

        if passenger is None:
            return None

        for attachment in passenger.attachments:
            if attachment.name == p_attachment_name:
                return attachment

        return None

    def get_passenger(self,
                      p_client_id: str,
                      p_puller_module: str,
                      p_external_id: str) -> AbstractPassenger:
        """ Returns the requested passenger """
        peeks = self.peek()

        for peek in peeks:
            if peek.client.id != p_client_id:
                continue
            for client_result in peek.results:
                for passenger in client_result.passengers:
                    if passenger.puller_module == p_puller_module:
                        if passenger.external_id == p_external_id:
                            return passenger
        return None

    def peek(self) -> List[ClientPeekResult]:
        """ Peeks into puller inboxes """
        output = []
        driver = self._dispatcher.get_driver()

        for client in self._dispatcher.all_clients:
            client_peek = ClientPeekResult(p_client=client)
            for client_passenger in client.passengers:
                for puller_module in client_passenger.puller_modules:
                    puller_peek = PullerPeekResult(p_puller_module=puller_module)
                    new_passengers = driver.pull_passengers_from_module(puller_module)

                    for new_passenger in new_passengers:
                        puller_peek.passengers.append(new_passenger)
                    client_peek.results.append(puller_peek)
            output.append(client_peek)
        return output
