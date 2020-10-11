""" Module for customizing pages """
from typing import List
from flask import render_template, redirect, request, url_for
from databus.client.client import Client
from databus.dispatcher.abstract_dispatcher import AbstractDispatcher
from databus.web.controller.abstract_controller import AbstractController, AuthenticationError


_CLIENTS_DB_NODE = "__clients__"
_DATABUS_DB_NODE = "__databus__"

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

    def get_client_customizing_entry(self, p_client_id: str, p_entry_name: str) -> ClientCustomizing: # pylint: disable=C0301
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
            client_nodes = []

            client_database = self._dispatcher.get_client_database(client.id)
            db_node = CustomizingNode(_DATABUS_DB_NODE, client_database.customizing)
            client_nodes.append(db_node)

            if client.id == Client.ROOT:
                clients_node = CustomizingNode(_CLIENTS_DB_NODE, client_database.client_master_data)
                client_nodes.append(clients_node)

            external_files = self._dispatcher.external_config_file_manager.get_files_of_client(client.id) # pylint: disable=C0301
            for external_file in external_files:
                external_node = CustomizingNode(external_file.file_id, external_file.file_content)
                client_nodes.append(external_node)

            output.append(ClientCustomizing(client, client_nodes))
        return output


class CustomizingListController(AbstractController):
    """ Customizing list page """

    def execute(self):
        """ Builds and returns the page """
        try:
            self._authenticate_minding_root(must_be_admin=True)
        except AuthenticationError as authentication_error:
            return authentication_error.output

        cust_reader = ClientCustomizingReader(self.dispatcher)
        entries = cust_reader.get_client_customizing_list(p_client_id=self.authenticated_client_id)

        return render_template(
            "customizing_list.html",
            entries=entries,
            alias=self.dispatcher.ticket.system_alias)

class CustomizingEditController(AbstractController):
    """ Customizing list page """

    def execute(self):
        """ Builds and returns the page """
        try:
            self._authenticate_minding_requested_client(must_be_admin=True)
        except AuthenticationError as authentication_error:
            return authentication_error.output

        node = request.args.get("node", 0, type=str)
        cust_reader = ClientCustomizingReader(self.dispatcher)
        entry = cust_reader.get_client_customizing_entry(self.requested_client_id, node)
        return render_template("customizing_edit.html", client=self.requested_client_id, node=node, entry=entry, alias=self.dispatcher.ticket.system_alias) # pylint: disable=C0301

class CustomizingSaveController(AbstractController):
    """ Customizing save """

    def execute(self):
        """ Builds and returns the page """
        try:
            self._authenticate_minding_requested_client(must_be_admin=True)
        except AuthenticationError as authentication_error:
            return authentication_error.output

        client_db = self.requested_client_database
        node = request.form["node"]
        customizing = request.form["customizing"]
        customizing = customizing.replace("\r\n", "\n") # Windows fix

        if node == _DATABUS_DB_NODE:
            client_db.customizing = customizing
        elif node == _CLIENTS_DB_NODE:
            client_db.client_master_data = customizing
        else:
            external_file = self.dispatcher.external_config_file_manager.get_file(self.requested_client_id, node) # pylint: disable=C0301
            external_file.file_content = customizing

        url = url_for("_customizing_list")
        url += "?" + AbstractController._get_cache_buster()
        return redirect(url, code=302)
