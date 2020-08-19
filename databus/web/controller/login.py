""" Controller module dealing with logging in and out """
from flask import make_response, redirect, request, session, url_for
from databus.client.client import Credential
from databus.client.user import Role
from databus.web.controller.abstract_controller import AbstractController


class LoginAttemptController(AbstractController):
    """ Login attempt """

    def execute(self):
        """ Builds and returns the page """
        try:
            client_id = request.form["client_id"]
            username = request.form["username"]
            password = request.form["password"]
            remember = False
            if "remember" in request.form:
                if request.form["remember"] == "X":
                    remember = True

            client_db = self.dispatcher.get_client_database(client_id)
            credential = None
            if client_db.client.authorization_active:
                credential = Credential(username=username, password=password)
                user = client_db.client.authenticate(credential)
                if user is None:
                    return redirect(url_for("_login"), code=302)
                user_role = user.role
                if remember:
                    credential.generate_token()
                    client_db.update_user_credential(credential)
            else:
                user_role = Role.ADMINISTRATOR

            session["client_id"] = client_db.client_id
            session["user_role"] = user_role.name
            resp = make_response(redirect(url_for("_home"), code=302))
            if credential is not None and credential.token != "":
                resp.set_cookie("token", credential.token)
            return resp

        except Exception: # pylint: disable=W0703
            return redirect(url_for("_login"), code=302)


class LogoffController(AbstractController):
    """ Logoff """

    def execute(self):
        """ Builds and returns the page """
        session["client_id"] = ""
        resp = make_response(redirect(url_for("_login"), code=302))
        resp.set_cookie("token", "")
        return resp
