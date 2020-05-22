""" Module for data export request """
from databus.database.abstract_database import AbstractDatabase
from databus.dispatcher.abstract_dispatcher import AbstractDispatcher

class ExportRequest: # pylint: disable=R0903, R0913
    """ Defines an export request """

    def __init__(self,
                 p_dispatcher: AbstractDispatcher,
                 p_to: AbstractDatabase,
                 p_args: dict,
                 p_client: str,
                 p_requesting_client_id: str):
        self.target_db = p_to
        self.args = p_args
        self.client = p_client
        self.dispatcher = p_dispatcher
        self.requesting_client_id = p_requesting_client_id
