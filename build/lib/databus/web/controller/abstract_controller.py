""" Module for abstract controller
A controller actually corresponds to a method in the
app.py file of Flask. It is named after MVC controllers
because the purpose is the same.
"""
from abc import ABC, abstractmethod
import io
import uuid
from flask import redirect, request, send_file, session, url_for
from databus.client.client import Client
from databus.client.user import User
from databus.database.abstract_database import AbstractDatabase
from databus.dispatcher.abstract_dispatcher import AbstractDispatcher
from databus.passenger.attachment import Attachment, AttachmentFormat
from databus.web.util import user_is_admin


class ClientUser: # pylint: disable=R0903
    """ Defines a user of a client """
    def __init__(self, p_client: Client = None, p_user: User = None):
        if p_client is None:
            self.client = Client()
        else:
            self.client = p_client
        if p_user is None:
            self.user = User()
        else:
            self.user = p_user


class ClientUserFinder: # pylint: disable=R0903
    """ Class to find client users """
    def __init__(self, p_dispatcher: AbstractDispatcher):
        self._dispatcher = p_dispatcher

    def find_by_token(self, p_token: str) -> ClientUser:
        """ Locates & returns a user by his/her token """
        all_clients = self._dispatcher.all_clients
        for client in all_clients:
            for user in client.users:
                if user.credential.token == p_token:
                    return ClientUser(p_client=client, p_user=user)
        return None


class AuthenticationError(Exception):
    """ Dispatcher creation exception """
    def __init__(self, output):
        super().__init__()
        self.output = output


class AbstractController(ABC):
    """ Base class for any controller """
    def __init__(self, p_dispatcher: AbstractDispatcher):
        self.dispatcher = p_dispatcher
        self.authenticated_client_id = None
        self.requested_client_id = ""

    @property
    def authenticated_client_database(self) -> AbstractDatabase:
        """ Returns the database object of the requested client """
        return self.dispatcher.get_client_database(self.authenticated_client_id)

    @property
    def requested_client_database(self) -> AbstractDatabase:
        """ Returns the database object of the requested client """
        return self.dispatcher.get_client_database(self.requested_client_id)

    @abstractmethod
    def execute(self):
        """ Builds and returns the page """

    @staticmethod
    def _download_attachment(att: Attachment):
        if att is None:
            return "File not found"
        if att.format == AttachmentFormat.binary:
            return send_file(
                io.BytesIO(att.binary_content),
                attachment_filename=att.name,
                as_attachment=True)
        if att.format == AttachmentFormat.text:
            return att.text_content
        return "Unexpected attachment format"

    @staticmethod
    def _get_cache_buster() -> str:
        return "&cache_buster=" + str(uuid.uuid1())

    def _authenticate(self, must_be_admin=False):
        self.authenticated_client_id = self._get_authenticated_client_id()
        if self.authenticated_client_id is None:
            output = redirect(url_for("_login"), code=302)
            raise AuthenticationError(output)
        if must_be_admin and (not user_is_admin()):
            output = redirect(url_for("_home"), code=302)
            raise AuthenticationError(output)

    def _authenticate_minding_requested_client(self, must_be_admin=False):
        self._authenticate(must_be_admin)
        self.requested_client_id = request.args.get("client", "", type=str)
        if self.requested_client_id == "":
            try:
                self.requested_client_id = request.form["client"]
            except Exception: # pylint: disable=W0703
                self.requested_client_id = ""

        if self.authenticated_client_id not in (Client.ROOT, self.requested_client_id):
            output = redirect(url_for("_home"), code=302)
            raise AuthenticationError(output)

    def _authenticate_minding_root(self, must_be_admin=False):
        self._authenticate(must_be_admin)
        if self.authenticated_client_id == Client.ROOT:
            self.authenticated_client_id = None

    def _get_authenticated_client_id(self) -> str:
        if "client_id" in session and session["client_id"] != "":
            if self._is_client_id_valid(session["client_id"]):
                return session["client_id"]

        token = request.cookies.get("token")
        if token != "":
            client_user = ClientUserFinder(self.dispatcher).find_by_token(token)
            if client_user is not None:
                session["client_id"] = client_user.client.id
                session["user_role"] = client_user.user.role.name
                return client_user.client.id

        return None

    def _is_client_id_valid(self, p_client_id: str):
        for client in self.dispatcher.all_clients:
            if client.id == p_client_id:
                return True
        return False
