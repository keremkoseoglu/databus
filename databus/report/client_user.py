""" Module for client user reporting purposes """
from databus.client.client import Client
from databus.client.user import User
from databus.dispatcher.abstract_dispatcher import AbstractDispatcher


class ClientUser: # pylint: disable=R0903
    """ Defines a user of a client """
    def __init__(self, p_client: Client = None, p_user: User = None):
        if p_client is None:
            self.client = Client()
        else:
            self.client = p_client
        if p_user is None:
            self.user = User()
        else:
            self.user = p_user


class ClientUserFinder: # pylint: disable=R0903
    """ Class to find client users """
    def __init__(self, p_dispatcher: AbstractDispatcher):
        self._dispatcher = p_dispatcher

    def find_by_token(self, p_token: str) -> ClientUser:
        """ Locates & returns a user by his/her token """
        all_clients = self._dispatcher.all_clients
        for client in all_clients:
            for user in client.users:
                if user.credential.token == p_token:
                    return ClientUser(p_client=client, p_user=user)
        return None
