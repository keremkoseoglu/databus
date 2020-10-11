""" Module for an export package """
from typing import List
from databus.client.client import Client
from databus.pqueue.queue_status import PassengerQueueStatus


class ExportPackage: # pylint: disable=R0903
    """ Defines an export package """

    def __init__(self,
                 p_client: Client = None,
                 p_queues: List[PassengerQueueStatus] = None):
        self.client = p_client

        if p_queues is None:
            self.queues = []
        else:
            self.queues = p_queues
