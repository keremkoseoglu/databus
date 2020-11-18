""" Module for peek controllers """
from typing import List
from flask import render_template, request
from databus.client.client import Client
from databus.dispatcher.abstract_dispatcher import AbstractDispatcher
from databus.passenger.abstract_passenger import AbstractPassenger, Attachment
from databus.web.controller.abstract_controller import AbstractController, AuthenticationError


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

    def peek(self, p_client_id: str = None) -> List[ClientPeekResult]:
        """ Peeks into puller inboxes """
        output = []
        driver = self._dispatcher.get_driver()

        for client in self._dispatcher.all_clients:
            if p_client_id is not None and p_client_id != client.id:
                continue
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


class PeekAttachmentController(AbstractController):
    """ Peek attachment """

    def execute(self):
        """ Builds and returns the page """
        try:
            self._authenticate_minding_requested_client()
        except AuthenticationError as authentication_error:
            return authentication_error.output

        puller = request.args.get("puller", 0, type=str)
        passenger = request.args.get("passenger", 0, type=str)
        file_name = request.args.get("file", 0, type=str)

        attachment = PullerPeek(self.dispatcher).get_attachment(
            p_client_id=self.requested_client_id,
            p_puller_module=puller,
            p_external_id=passenger,
            p_attachment_name=file_name)

        if attachment is None:
            return "File not found"

        return AbstractController._download_attachment(attachment)


class PeekController(AbstractController):
    """ Peek """

    def execute(self):
        """ Builds and returns the page """
        try:
            self._authenticate_minding_root()
        except AuthenticationError as authentication_error:
            return authentication_error.output

        try:
            peek = PullerPeek(self.dispatcher).peek(self.authenticated_client_id)
            peek_error = ""
        except Exception as diaper: # pylint: disable=W0703
            peek = []
            peek_error = str(diaper)

        return render_template(
            "peek.html",
            peek=peek,
            peek_error=peek_error,
            alias=self.dispatcher.ticket.system_alias)
