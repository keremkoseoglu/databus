""" Module for user pages """
from flask import render_template, redirect, request, url_for
from databus.client.client import Client
from databus.web.controller.abstract_controller import AbstractController, AuthenticationError

class UserTokenRevokeController(AbstractController):
    """ User token revoke """

    def execute(self):
        """ Builds and returns the page """
        try:
            self._authenticate_minding_requested_client(must_be_admin=True)
        except AuthenticationError as authentication_error:
            return authentication_error.output

        client_db = self.requested_client_database
        username = request.args.get("user", 0, type=str)

        for user in client_db.client.users:
            if user.credential.username == username:
                user.credential.token = ""
                client_db.update_user_credential(user.credential)
                break

        url = url_for("_user_list")
        url += "?" + AbstractController._get_cache_buster()
        return redirect(url, code=302)

class UserListController(AbstractController):
    """ User list page """

    def execute(self):
        """ Builds and returns the page """
        try:
            self._authenticate(must_be_admin=True)
        except AuthenticationError as authentication_error:
            return authentication_error.output

        if self.authenticated_client_id == Client.ROOT:
            clients = self.dispatcher.all_clients
        else:
            clients = [self.authenticated_client_database.client]

        return render_template(
            "user_list.html",
            clients=clients,
            alias=self.dispatcher.ticket.system_alias)
