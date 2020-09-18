""" Module for queue controllers """
from datetime import datetime
from typing import List
from flask import redirect, render_template, request, url_for
from databus.client.client import Client
from databus.client.client_passenger import ClientPassenger
from databus.dispatcher.abstract_dispatcher import AbstractDispatcher
from databus.pqueue.queue_status import PassengerQueueStatus, QueueStatus
from databus.web.controller.abstract_controller import AbstractController, AuthenticationError


class ClientPassengerQueue: # pylint: disable=R0903
    """ Defines a client passenger and all queue files present """
    def __init__(self,
                 p_client: Client = None,
                 p_client_passenger: ClientPassenger = None,
                 p_queues: List[PassengerQueueStatus] = None):

        if p_client is None:
            self.client = Client()
        else:
            self.client = p_client

        if p_client_passenger is None:
            self.client_passenger = []
        else:
            self.client_passenger = p_client_passenger

        if p_queues is None:
            self.queues = []
        else:
            self.queues = p_queues


class ClientPassengerQueueReader:
    """ Class dealing with client queue files """
    def __init__(self, p_dispatcher: AbstractDispatcher):
        self._dispatcher = p_dispatcher

    def get_client_passenger_queue_entry(self,
                                         p_client_id: str,
                                         p_internal_id: str
                                        ) -> PassengerQueueStatus:
        """ Returns a list of client - passenger - queue files """
        client_database = self._dispatcher.get_client_database(p_client_id)
        return client_database.get_passenger_queue_entry(p_internal_id)

    def get_client_passenger_queue_list(self,
                                        p_client_id: str = None
                                       ) -> List[ClientPassengerQueue]:
        """ Returns a list of client - passenger - queue files """
        output = []
        for client in self._dispatcher.all_clients:
            if p_client_id is not None and client.id != p_client_id:
                continue
            client_database = self._dispatcher.get_client_database(client.id)
            for client_passenger in client.passengers:
                queue_entries = client_database.get_passenger_queue_entries(p_passenger_module=client_passenger.name) # pylint: disable=C0301

                client_passenger_queue = ClientPassengerQueue(
                    p_client=client,
                    p_client_passenger=client_passenger,
                    p_queues=queue_entries)

                output.append(client_passenger_queue)
        return output


class QueueAttachmentController(AbstractController):
    """ Queue attachment download """

    def execute(self):
        """ Builds and returns the page """
        try:
            self._authenticate_minding_requested_client()
        except AuthenticationError as authentication_error:
            return authentication_error.output

        passenger = request.args.get("passenger", 0, type=str)
        file = request.args.get("file", 0, type=str)
        entry = ClientPassengerQueueReader(self.dispatcher).get_client_passenger_queue_entry(self.requested_client_id, passenger) # pylint: disable=C0301

        for att in entry.passenger.attachments:
            if att.name == file:
                return AbstractController._download_attachment(att)

        return "File not found"


class QueueDisplayController(AbstractController):
    """ Queue display """

    def execute(self):
        """ Builds and returns the page """
        try:
            self._authenticate_minding_requested_client()
        except AuthenticationError as authentication_error:
            return authentication_error.output

        passenger = request.args.get("passenger", 0, type=str)
        entry = ClientPassengerQueueReader(self.dispatcher).get_client_passenger_queue_entry(self.requested_client_id, passenger) # pylint: disable=C0301

        log_ids = []
        client_database = self.requested_client_database
        for log_guid in entry.passenger.log_guids:
            log_id = client_database.convert_log_guid_to_id(log_guid)
            log_ids.append(log_id)

        return render_template(
            "queue_display.html",
            client=self.requested_client_id,
            entry=entry,
            alias=self.dispatcher.ticket.system_alias,
            log_ids=log_ids)


class QueueListController(AbstractController):
    """ Queue list """

    def execute(self):
        """ Builds and returns the page """
        try:
            self._authenticate_minding_root()
        except AuthenticationError as authentication_error:
            return authentication_error.output

        queue_reader = ClientPassengerQueueReader(self.dispatcher)
        entries = queue_reader.get_client_passenger_queue_list(
            p_client_id=self.authenticated_client_id)

        return render_template(
            "queue_list.html",
            entries=entries,
            alias=self.dispatcher.ticket.system_alias)


class QueuePurgeController(AbstractController):
    """ Queue purge """

    def execute(self):
        """ Builds and returns the page """
        try:
            self._authenticate_minding_requested_client()
        except AuthenticationError as authentication_error:
            return authentication_error.output

        passenger_module = request.args.get("passenger", 0, type=str)
        client_db = self.requested_client_database
        client_passenger = client_db.client.get_client_passenger(passenger_module)

        queue = self.dispatcher.ticket.queue_factory.create_queue(
            client_passenger.queue_module,
            client_db,
            client_db.log)

        queue.delete_completed_passengers(passenger_module, datetime.now())
        return redirect(url_for("_queue_list"), code=302)


class QueueStatusUpdateController(AbstractController):
    """ Queue display """

    def execute(self): # pylint: disable=R0912
        """ Builds and returns the page """
        try:
            self._authenticate_minding_requested_client()
        except AuthenticationError as authentication_error:
            return authentication_error.output

        passenger = request.args.get("passenger", "", type=str)
        entry = ClientPassengerQueueReader(self.dispatcher).get_client_passenger_queue_entry(self.requested_client_id, passenger) # pylint: disable=C0301

        puller_notified = request.args.get("puller_notified", "", type=str)
        if puller_notified == "true":
            entry.puller_notified = True
        elif puller_notified == "false":
            entry.puller_notified = False

        processor_module = request.args.get("processor", "", type=str)
        if processor_module != "":
            processed = request.args.get("processed", "", type=str) == "true"
            for processor_status in entry.processor_statuses:
                if processor_status.processor_module == processor_module:
                    if processed:
                        processor_status.status = QueueStatus.complete
                    else:
                        processor_status.status = QueueStatus.incomplete

        pusher_module = request.args.get("pusher", "", type=str)
        if pusher_module != "":
            processed = request.args.get("pushed", "", type=str) == "true"
            for pusher_status in entry.pusher_statuses:
                if pusher_status.pusher_module == pusher_module:
                    if processed:
                        pusher_status.status = QueueStatus.complete
                    else:
                        pusher_status.status = QueueStatus.incomplete

        self.requested_client_database.update_queue_status(entry)

        redirect_url = url_for("_queue_display")
        redirect_url += "?client=" + self.requested_client_id + "&passenger=" + passenger
        redirect_url += AbstractController._get_cache_buster()
        return redirect(redirect_url, code=302)
