""" Observer module for significant dispatcher events """
from typing import Protocol
from databus.client.client import Client
from databus.client.client_passenger import ClientPassenger
from databus.client.log import Log


class DispatcherObserver(Protocol): # pylint: disable=R0903
    """ Observer class for significant dispatcher events
    You can implement this class into your project and pass it via
    the dispatcher ticket.
    """
    def drive_passenger_complete(self,
                                 p_client: Client,
                                 p_client_passenger: ClientPassenger,
                                 p_log: Log):
        """ Fired when primal_dispatcher.drive_passenger is completed.
        You can typically use this method to send E-Mail notifications if p_log contains errors.
        """
