""" Module for client queue reporting """
from typing import List
from databus.client.client import Client
from databus.client.client_passenger import ClientPassenger
from databus.dispatcher.abstract_dispatcher import AbstractDispatcher
from databus.pqueue.queue_status import PassengerQueueStatus

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
