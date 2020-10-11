""" Shutdown web module """
from flask import redirect, url_for, render_template
from databus.client.client import Client
from databus.web.controller.abstract_controller import AbstractController, AuthenticationError

class ShutdownController(AbstractController):
    """ Shutdown controller """

    def execute(self):
        """ Builds and returns the page """
        try:
            self._authenticate(must_be_admin=True)
        except AuthenticationError as authentication_error:
            return authentication_error.output

        if self.authenticated_client_id != Client.ROOT:
            return redirect(url_for("_login"), code=302)

        return render_template("shutdown.html", alias=self.dispatcher.ticket.system_alias)

class ShutdownExeController(AbstractController):
    """ Shutdown execution """

    def execute(self):
        """ Shutdown execute """
        try:
            self._authenticate(must_be_admin=True)
        except AuthenticationError:
            return "Error shutting down, cant authenticate"

        if self.authenticated_client_id != Client.ROOT:
            return "Error shutting down, no permission"

        self.dispatcher.request_shutdown()
        return "Shutdown started"
