""" Client Log reporting """
from typing import List
from databus.client.client import Client
from databus.database.abstract_database import LogListItem
from databus.dispatcher.abstract_dispatcher import AbstractDispatcher


class ClientLog: # pylint: disable=R0903
    """ Defines a client and all log files present """
    def __init__(self, p_client: Client = None, p_logs: List[LogListItem] = None):
        if p_client is None:
            self.client = Client()
        else:
            self.client = p_client

        if p_logs is None:
            self.logs = p_logs
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

    def get_client_log_list(self) -> List[ClientLog]:
        """ Returns a list of client - log files """
        output = []

        for client in self._dispatcher.all_clients:
            client_database = self._dispatcher.get_client_database(client.id)
            logs = client_database.get_log_list()
            logs.sort(key=lambda r: r.log_id, reverse=True)
            output.append(ClientLog(client, logs))
        return output
