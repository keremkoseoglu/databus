""" Web module for exporting data """
import json
from typing import List
from flask import jsonify, render_template, request, redirect, url_for
from databus.client.client import Client
from databus.client.log import Log
from databus.database.export.export import ExporterFactory, ExportStatus
from databus.database.export.export_request import ExportRequest
from databus.dispatcher.abstract_dispatcher import AbstractDispatcher
from databus.web.controller.abstract_controller import AbstractController, AuthenticationError


class ExportableClientList: # pylint: disable=R0903
    """ Class dealing with exportable clients """
    def __init__(self, p_dispatcher: AbstractDispatcher):
        self._dispatcher = p_dispatcher

    def get_exportable_clients(self, p_client_id: str = None) -> List[Client]:
        """ Returns a list of exportable clients """
        client_db = self._dispatcher.get_client_database(p_client_id)
        if p_client_id is None:
            return client_db.get_clients()
        return [client_db.client]


class ExportController(AbstractController):
    """ Export data """

    def execute(self):
        """ Builds and returns the page """
        try:
            self._authenticate_minding_root(must_be_admin=True)
        except AuthenticationError as authentication_error:
            return authentication_error.output

        exporter = ExporterFactory.get_singleton()
        if exporter.status == ExportStatus.BUSY:
            return render_template("export_busy.html", alias=self.dispatcher.ticket.system_alias)

        list_builder = ExportableClientList(self.dispatcher)
        exportable_clients = list_builder.get_exportable_clients(self.authenticated_client_id)
        db_modules = self.dispatcher.ticket.database_factory.database_modules

        return render_template(
            "export.html",
            exportable_clients=exportable_clients,
            db_modules=db_modules,
            alias=self.dispatcher.ticket.system_alias)


class ExportGetDictController(AbstractController):
    """ Returns the dict of the database """

    def execute(self):
        """ Builds and returns the page """
        try:
            self._authenticate_minding_root(must_be_admin=True)
        except AuthenticationError as authentication_error:
            return authentication_error.output

        db_module_name = request.args.get("db_module", 0, type=str)
        classes = self.dispatcher.ticket.database_factory.database_classes
        db_module = __import__(db_module_name, fromlist=classes)
        output = getattr(db_module, "ARGS_TEMPLATE")
        return jsonify(output)


class ExportExeController(AbstractController):
    """ Executes an export request """

    def execute(self):
        """ Executes an export request """
        try:
            self._authenticate(must_be_admin=True)
        except AuthenticationError as authentication_error:
            return authentication_error.output

        exporter = ExporterFactory.get_singleton()
        if exporter.status == ExportStatus.BUSY:
            return render_template("export_busy.html", alias=self.dispatcher.ticket.system_alias)

        client = request.form["client"]
        db_module = request.form["db_module"]
        db_args = json.loads(request.form["args"])
        mode = request.form["mode"]

        if self.authenticated_client_id != Client.ROOT:
            if client != self.authenticated_client_id:
                return redirect(url_for("_login"), code=302)

        target_db = self.dispatcher.ticket.database_factory.create_database(
            db_module,
            client,
            Log(),
            self.dispatcher.ticket.passenger_factory,
            db_args
        )

        export_request = ExportRequest(
            self.dispatcher,
            target_db,
            db_args,
            client,
            self.authenticated_client_id
        )

        if mode == "async":
            exporter.execute_async(export_request)
        else:
            exporter.execute(export_request)

        return render_template(
            "export_started.html",
            mode=mode,
            alias=self.dispatcher.ticket.system_alias)
