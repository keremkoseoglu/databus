""" Module for customizing pages """
from flask import render_template, redirect, request, url_for
from databus.dispatcher.abstract_dispatcher import CLIENTS_DB_NODE, DATABUS_DB_NODE
from databus.web.controller.abstract_controller import AbstractController, AuthenticationError

class CustomizingListController(AbstractController):
    """ Customizing list page """

    def execute(self):
        """ Builds and returns the page """
        try:
            self._authenticate_minding_root(must_be_admin=True)
        except AuthenticationError as authentication_error:
            return authentication_error.output

        entries = self.dispatcher.get_client_customizing_list(
            p_client_id=self.authenticated_client_id)

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
        entry = self.dispatcher.get_client_customizing_entry(self.requested_client_id, node)
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

        if node == DATABUS_DB_NODE:
            client_db.customizing = customizing
        elif node == CLIENTS_DB_NODE:
            client_db.client_master_data = customizing
        else:
            external_file = self.dispatcher.external_config_file_manager.get_file(self.requested_client_id, node) # pylint: disable=C0301
            external_file.file_content = customizing

        url = url_for("_customizing_list")
        url += "?" + AbstractController._get_cache_buster()
        return redirect(url, code=302)
