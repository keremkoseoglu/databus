""" Resume web module """
from flask import redirect, url_for, render_template
from databus.client.client import Client
from databus.web.controller.abstract_controller import AbstractController, AuthenticationError

class ResumeController(AbstractController):
    """ Pause controller """

    def execute(self):
        """ Builds and returns the page """
        try:
            self._authenticate(must_be_admin=True)
        except AuthenticationError as authentication_error:
            return authentication_error.output

        if self.authenticated_client_id != Client.ROOT:
            return redirect(url_for("_login"), code=302)

        try:
            self.dispatcher.resume()
            success = True
            error = ""
        except Exception as raised_error:
            success = False
            error = f"Resume error: {str(raised_error)}"

        return render_template(
            "resume.html",
            alias=self.dispatcher.ticket.system_alias,
            success=success,
            error=error)
