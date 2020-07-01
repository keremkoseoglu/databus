""" Module for log controllers """
from datetime import datetime
from typing import List
from flask import redirect, render_template, request, url_for
from databus.client.client import Client
from databus.database.abstract_database import LogListItem
from databus.dispatcher.abstract_dispatcher import AbstractDispatcher
from databus.web.controller.abstract_controller import AbstractController, AuthenticationError


class ClientLog: # pylint: disable=R0903
    """ Defines a client and all log files present """
    def __init__(self, p_client: Client = None, p_logs: List[LogListItem] = None):
        if p_client is None:
            self.client = Client()
        else:
            self.client = p_client

        if p_logs is None:
            self.logs = []
        else:
            self.logs = p_logs


class ClientLogReader:
    """ Class dealing with client log files """
    def __init__(self, p_dispatcher: AbstractDispatcher):
        self._dispatcher = p_dispatcher

    def get_client_log_content(self, p_client_id: str, p_log_id: str) -> str:
        """ Returns content of the log file """
        client_db = self._dispatcher.get_client_database(p_client_id)
        log_content = client_db.get_log_content(p_log_id)
        return log_content

    def get_client_log_list(self, p_client_id: str = None) -> List[ClientLog]:
        """ Returns a list of client - log files """
        output = []

        for client in self._dispatcher.all_clients:
            if p_client_id is not None and client.id != p_client_id:
                continue
            client_database = self._dispatcher.get_client_database(client.id)
            logs = client_database.get_log_list()
            logs.sort(key=lambda r: r.log_id, reverse=True)
            output.append(ClientLog(client, logs))
        return output


class LogDisplayController(AbstractController):
    """ Log display """

    def execute(self):
        """ Builds and returns the page """
        try:
            self._authenticate_minding_requested_client()
        except AuthenticationError as authentication_error:
            return authentication_error.output

        log_file = request.args.get("log", 0, type=str)
        file_content = ClientLogReader(self.dispatcher).get_client_log_content(self.requested_client_id, log_file).replace("\n", "<br><br>") # pylint: disable=C0301
        return file_content


class LogListController(AbstractController):
    """ Log list """

    def execute(self):
        """ Builds and returns the page """
        try:
            self._authenticate_minding_root()
        except AuthenticationError as authentication_error:
            return authentication_error.output

        log_reader = ClientLogReader(self.dispatcher)
        entries = log_reader.get_client_log_list(p_client_id=self.authenticated_client_id)

        return render_template(
            "log_list.html",
            entries=entries,
            alias=self.dispatcher.ticket.system_alias)


class LogPurgeController(AbstractController):
    """ Log purge """

    def execute(self):
        """ Builds and returns the page """
        try:
            self._authenticate_minding_requested_client()
        except AuthenticationError as authentication_error:
            return authentication_error.output

        self.requested_client_database.delete_old_logs(datetime.now())
        return redirect(url_for("_log_list"), code=302)
