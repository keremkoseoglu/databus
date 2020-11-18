""" Shutdown web module """
from flask import redirect, url_for, render_template
from databus.client.client import Client
from databus.web.controller.abstract_controller import AbstractController, AuthenticationError


class SystemController(AbstractController):
    """ System controller """

    def execute(self):
        """ Builds and returns the page """
        try:
            self._authenticate(must_be_admin=True)
        except AuthenticationError as authentication_error:
            return authentication_error.output

        if self.authenticated_client_id != Client.ROOT:
            return redirect(url_for("_login"), code=302)

        if self.dispatcher.shutting_down:
            status = "Shutting down"
        elif self.dispatcher.exporting:
            status = "Exporting data"
        elif self.dispatcher.paused:
            status = "Paused"
        elif self.dispatcher.dispatching:
            status = "Dispatching"
        else:
            status = "Idle"

        return render_template(
            "system.html",
            alias=self.dispatcher.ticket.system_alias,
            status=status)
