""" Module for passenger pages """
from flask import render_template, redirect, request, url_for
from databus.client.client import Client
from databus.web.controller.abstract_controller import AbstractController, AuthenticationError


class PassengerExpediteController(AbstractController):
    """ Passenger expedite """

    def execute(self):
        """ Builds and returns the page """
        try:
            self._authenticate_minding_requested_client()
        except AuthenticationError as authentication_error:
            return authentication_error.output

        passenger = request.args.get("passenger", 0, type=str)
        self.dispatcher.expedite_client_passenger(self.requested_client_id, passenger)
        url = url_for("_passenger_list")
        url += "?expedited=true"
        url += AbstractController._get_cache_buster()
        return redirect(url, code=302)


class PassengerListController(AbstractController):
    """ Passenger list page """

    def execute(self):
        """ Builds and returns the page """
        try:
            self._authenticate()
        except AuthenticationError as authentication_error:
            return authentication_error.output

        if self.authenticated_client_id == Client.ROOT:
            clients = self.dispatcher.all_clients
        else:
            clients = [self.authenticated_client_database.client]

        try:
            expedited = request.args.get("expedited", 0, type=str) == "true"
        except Exception: # pylint: disable=W0703
            expedited = False

        return render_template(
            "passenger_list.html",
            clients=clients,
            expedited=expedited,
            alias=self.dispatcher.ticket.system_alias)
