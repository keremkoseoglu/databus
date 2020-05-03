""" Module for customizing pages """
from typing import List
from flask import render_template, redirect, request, url_for
from databus.client.client import Client
from databus.dispatcher.abstract_dispatcher import AbstractDispatcher
from databus.web.controller.abstract_controller import AbstractController, AuthenticationError


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


class ClientCustomizingReader: # pylint: disable=R0903
    """ Class dealing with client customizing files """
    def __init__(self, p_dispatcher: AbstractDispatcher):
        self._dispatcher = p_dispatcher

    def get_client_customizing_entry(self, p_client_id: str, p_entry_name: str) -> ClientCustomizing:
        """ Returns a single node """
        all_entries = self.get_client_customizing_list(p_client_id=p_client_id)
        if all_entries is None or len(all_entries) < 0:
            return None
        for entry in all_entries[0].nodes:
            if entry.name == p_entry_name:
                return entry
        return None

    def get_client_customizing_list(self, p_client_id: str = None):
        """ Returns a list of client - customizing files """
        output = []

        for client in self._dispatcher.all_clients:
            if p_client_id is not None and client.id != p_client_id:
                continue
            client_database = self._dispatcher.get_client_database(client.id)
            db_node = CustomizingNode("databus", client_database.customizing)
            output.append(ClientCustomizing(client, [db_node]))
        return output


class CustomizingListController(AbstractController):
    """ Customizing list page """

    def execute(self):
        """ Builds and returns the page """
        try:
            self._authenticate_minding_root()
        except AuthenticationError as authentication_error:
            return authentication_error.output

        cust_reader = ClientCustomizingReader(self.dispatcher)
        entries = cust_reader.get_client_customizing_list(p_client_id=self.authenticated_client_id)
        return render_template("customizing_list.html", entries=entries)

class CustomizingEditController(AbstractController):
    """ Customizing list page """

    def execute(self):
        """ Builds and returns the page """
        try:
            self._authenticate_minding_requested_client()
        except AuthenticationError as authentication_error:
            return authentication_error.output

        node = request.args.get("node", 0, type=str)
        cust_reader = ClientCustomizingReader(self.dispatcher)
        entry = cust_reader.get_client_customizing_entry(self.requested_client_id, node)
        return render_template("customizing_edit.html", client=self.requested_client_id, entry=entry)

class CustomizingSaveController(AbstractController):
    """ Customizing save """

    def execute(self):
        """ Builds and returns the page """
        try:
            self._authenticate_minding_requested_client()
        except AuthenticationError as authentication_error:
            return authentication_error.output

        client_db = self.requested_client_database
        customizing = request.form["customizing"]
        client_db.customizing = customizing

        url = url_for("_customizing_list")
        url += "?" + AbstractController._get_cache_buster()
        return redirect(url, code=302)
