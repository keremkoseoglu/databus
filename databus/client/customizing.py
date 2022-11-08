""" Client customizing """
from typing import List
from databus.client.client import Client

class CustomizingNode:  # pylint: disable=R0903
    """ Defines a customizing node """
    def __init__(self, p_name: str = "", p_content: str = ""):
        self.name = p_name
        self.content = p_content


class ClientCustomizing: # pylint: disable=R0903
    """ Defines a client and its customizing files """
    def __init__(self, p_client: Client = None, p_customs: List[CustomizingNode] = None):
        if p_client is None:
            self.client = Client()
        else:
            self.client = p_client

        if p_customs is None:
            self.nodes = []
        else:
            self.nodes = p_customs
