""" Module for home type of pages """
from flask import render_template
import databus
from databus.web.controller.abstract_controller import AbstractController, AuthenticationError


class AboutController(AbstractController):
    """ About page """

    def execute(self):
        """ Builds and returns the page """

        return render_template(
            "about.html",
            version=databus.__version__,
            author=databus.AUTHOR,
            email=databus.EMAIL,
            description=databus.DESCRIPTION,
            python_version=databus.PYTHON_VERSION,
            dispatcher=self.dispatcher,
            alias=self.dispatcher.ticket.system_alias)


class HomeController(AbstractController):
    """ Home page """

    def execute(self):
        """ Builds and returns the page """
        try:
            self._authenticate()
        except AuthenticationError as authentication_error:
            return authentication_error.output

        return render_template("home.html", alias=self.dispatcher.ticket.system_alias)
