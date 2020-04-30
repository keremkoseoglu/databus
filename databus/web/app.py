""" Module for web interface
This mini web interfaces is based on Flask.
Theme help: https://bootswatch.com/darkly/
"""
from datetime import datetime
import io
import uuid
from flask import Flask, make_response, redirect, render_template, request, send_file, session, url_for # pylint: disable=C0301
from waitress import serve
import databus
from databus.client.client import Client, Credential
from databus.dispatcher.abstract_dispatcher import AbstractDispatcher
from databus.passenger.attachment import Attachment, AttachmentFormat
from databus.pqueue.queue_status import QueueStatus
from databus.report.client_log import ClientLogReader
from databus.report.client_queue import ClientPassengerQueueReader
from databus.report.client_user import ClientUserFinder
from databus.report.puller_peek import PullerPeek

##############################
# Main stuff
##############################

_APP = Flask(__name__)
_APP.secret_key = "databus"
_APP.config["CACHE_TYPE"] = "null"
_DISPATCHER: AbstractDispatcher


def run_web_server(dispatcher: AbstractDispatcher):
    """ Starts the Flask Web Server """
    global _DISPATCHER # pylint: disable=W0603
    _DISPATCHER = dispatcher
    serve(_APP, port=dispatcher.ticket.web_server_port)
    #_APP.run(port=dispatcher.ticket.web_server_port)

##############################
# Home page
##############################

@_APP.route("/")
def _home():
    authenticated_client_id = _get_authenticated_client_id()
    if authenticated_client_id is None:
        return redirect(url_for("_login"), code=302)

    return render_template("home.html")

##############################
# Log pages
##############################

@_APP.route("/log_list")
def _log_list():
    global _DISPATCHER # pylint: disable=W0603

    authenticated_client_id = _get_authenticated_client_id()
    if authenticated_client_id is None:
        return redirect(url_for("_login"), code=302)
    if authenticated_client_id == Client.ROOT:
        authenticated_client_id = None

    entries = ClientLogReader(_DISPATCHER).get_client_log_list(p_client_id=authenticated_client_id)
    return render_template("log_list.html", entries=entries)


@_APP.route("/log_display")
def _log_display():
    authenticated_client_id = _get_authenticated_client_id()
    if authenticated_client_id is None:
        return redirect(url_for("_login"), code=302)

    client_id = request.args.get("client", 0, type=str)
    if authenticated_client_id not in (Client.ROOT, client_id):
        return redirect(url_for("_home"), code=302)

    log_file = request.args.get("log", 0, type=str)
    file_content = ClientLogReader(_DISPATCHER).get_client_log_content(client_id, log_file).replace("\n", "<br><br>") # pylint: disable=C0301
    return file_content

@_APP.route("/log_purge")
def _log_purge():
    global _DISPATCHER # pylint: disable=W0603

    authenticated_client_id = _get_authenticated_client_id()
    if authenticated_client_id is None:
        return redirect(url_for("_login"), code=302)

    client_id = request.args.get("client", 0, type=str)
    if authenticated_client_id not in (Client.ROOT, client_id):
        return redirect(url_for("_home"), code=302)

    _DISPATCHER.get_client_database(client_id).delete_old_logs(datetime.now())
    return redirect(url_for("_log_list"), code=302)

##############################
# Queue pages
##############################

@_APP.route("/queue_list")
def _queue_list():
    global _DISPATCHER # pylint: disable=W0603

    authenticated_client_id = _get_authenticated_client_id()
    if authenticated_client_id is None:
        return redirect(url_for("_login"), code=302)
    if authenticated_client_id == Client.ROOT:
        authenticated_client_id = None

    queue_reader = ClientPassengerQueueReader(_DISPATCHER)
    entries = queue_reader.get_client_passenger_queue_list(p_client_id=authenticated_client_id)
    return render_template("queue_list.html", entries=entries)

@_APP.route("/queue_display")
def _queue_display():
    global _DISPATCHER # pylint: disable=W0603

    authenticated_client_id = _get_authenticated_client_id()
    if authenticated_client_id is None:
        return redirect(url_for("_login"), code=302)

    client = request.args.get("client", 0, type=str)
    if authenticated_client_id not in (Client.ROOT, client):
        return redirect(url_for("_home"), code=302)

    passenger = request.args.get("passenger", 0, type=str)
    entry = ClientPassengerQueueReader(_DISPATCHER).get_client_passenger_queue_entry(client, passenger) # pylint: disable=C0301
    return render_template("queue_display.html", client=client, entry=entry)

@_APP.route("/queue_attachment")
def _queue_attachment():
    global _DISPATCHER # pylint: disable=W0603

    authenticated_client_id = _get_authenticated_client_id()
    if authenticated_client_id is None:
        return redirect(url_for("_login"), code=302)

    client = request.args.get("client", 0, type=str)
    if authenticated_client_id not in (Client.ROOT, client):
        return redirect(url_for("_home"), code=302)

    passenger = request.args.get("passenger", 0, type=str)
    file = request.args.get("file", 0, type=str)
    entry = ClientPassengerQueueReader(_DISPATCHER).get_client_passenger_queue_entry(client, passenger) # pylint: disable=C0301

    for att in entry.passenger.attachments:
        if att.name == file:
            return _download_attachment(att)

    return "File not found"

@_APP.route("/queue_status_update")
def _queue_status_update(): # pylint: disable=R0912
    global _DISPATCHER # pylint: disable=W0603

    authenticated_client_id = _get_authenticated_client_id()
    if authenticated_client_id is None:
        return redirect(url_for("_login"), code=302)

    client = request.args.get("client", 0, type=str)
    if authenticated_client_id not in (Client.ROOT, client):
        return redirect(url_for("_home"), code=302)

    passenger = request.args.get("passenger", "", type=str)
    entry = ClientPassengerQueueReader(_DISPATCHER).get_client_passenger_queue_entry(client, passenger) # pylint: disable=C0301

    puller_notified = request.args.get("puller_notified", "", type=str)
    if puller_notified == "true":
        entry.puller_notified = True
    elif puller_notified == "false":
        entry.puller_notified = False

    processor_module = request.args.get("processor", "", type=str)
    if processor_module != "":
        processed = request.args.get("processed", "", type=str) == "true"
        for processor_status in entry.processor_statuses:
            if processor_status.processor_module == processor_module:
                if processed:
                    processor_status.status = QueueStatus.complete
                else:
                    processor_status.status = QueueStatus.incomplete

    pusher_module = request.args.get("pusher", "", type=str)
    if pusher_module != "":
        processed = request.args.get("pushed", "", type=str) == "true"
        for pusher_status in entry.pusher_statuses:
            if pusher_status.pusher_module == pusher_module:
                if processed:
                    pusher_status.status = QueueStatus.complete
                else:
                    pusher_status.status = QueueStatus.incomplete

    _DISPATCHER.get_client_database(client).update_queue_status(entry)

    redirect_url = url_for("_queue_display")
    redirect_url += "?client=" + client + "&passenger=" + passenger
    redirect_url += _get_cache_buster()
    return redirect(redirect_url, code=302)

@_APP.route("/queue_purge")
def _queue_purge():
    global _DISPATCHER # pylint: disable=W0603

    authenticated_client_id = _get_authenticated_client_id()
    if authenticated_client_id is None:
        return redirect(url_for("_login"), code=302)

    client_id = request.args.get("client", 0, type=str)
    if authenticated_client_id not in (Client.ROOT, client_id):
        return redirect(url_for("_home"), code=302)

    passenger_module = request.args.get("passenger", 0, type=str)
    client_db = _DISPATCHER.get_client_database(client_id)
    client_passenger = client_db.client.get_client_passenger(passenger_module)

    queue = _DISPATCHER.ticket.queue_factory.create_queue(
        client_passenger.queue_module,
        client_db,
        client_db.log)

    queue.delete_completed_passengers(passenger_module, datetime.now())
    return redirect(url_for("_queue_list"), code=302)

##############################
# Passengers
##############################

@_APP.route("/passenger_list")
def _passenger_list():
    global _DISPATCHER # pylint: disable=W0603

    authenticated_client_id = _get_authenticated_client_id()
    if authenticated_client_id is None:
        return redirect(url_for("_login"), code=302)

    if authenticated_client_id == Client.ROOT:
        clients = _DISPATCHER.all_clients
    else:
        clients = [_DISPATCHER.get_client_database(authenticated_client_id).client]

    try:
        expedited = request.args.get("expedited", 0, type=str) == "true"
    except Exception: # pylint: disable=W0703
        expedited = False
    return render_template("passenger_list.html", clients=clients, expedited=expedited)

@_APP.route("/passenger_expedite")
def _passenger_expedite():
    global _DISPATCHER # pylint: disable=W0603

    authenticated_client_id = _get_authenticated_client_id()
    if authenticated_client_id is None:
        return redirect(url_for("_login"), code=302)

    client = request.args.get("client", 0, type=str)
    if authenticated_client_id not in (Client.ROOT, client):
        return redirect(url_for("_home"), code=302)

    passenger = request.args.get("passenger", 0, type=str)
    _DISPATCHER.expedite_client_passenger(client, passenger)
    return redirect(url_for("_passenger_list") + "?expedited=true" + _get_cache_buster(), code=302)

##############################
# Peek
##############################

@_APP.route("/peek")
def _peek():
    global _DISPATCHER # pylint: disable=W0603

    authenticated_client_id = _get_authenticated_client_id()
    if authenticated_client_id is None:
        return redirect(url_for("_login"), code=302)
    if authenticated_client_id == Client.ROOT:
        authenticated_client_id = None

    peek = PullerPeek(_DISPATCHER).peek(authenticated_client_id)
    return render_template("peek.html", peek=peek)

@_APP.route("/peek_attachment")
def _peek_attachment():
    global _DISPATCHER # pylint: disable=W0603

    authenticated_client_id = _get_authenticated_client_id()
    if authenticated_client_id is None:
        return redirect(url_for("_login"), code=302)

    client = request.args.get("client", 0, type=str)
    if authenticated_client_id not in (Client.ROOT, client):
        return redirect(url_for("_home"), code=302)

    puller = request.args.get("puller", 0, type=str)
    passenger = request.args.get("passenger", 0, type=str)
    file_name = request.args.get("file", 0, type=str)

    attachment = PullerPeek(_DISPATCHER).get_attachment(
        p_client_id=client,
        p_puller_module=puller,
        p_external_id=passenger,
        p_attachment_name=file_name)

    if attachment is None:
        return "File not found"

    return _download_attachment(attachment)

##############################
# Login
##############################

@_APP.route("/login")
def _login():
    return render_template("login.html")

@_APP.route("/login_attempt", methods=["POST"])
def _login_attempt():
    global _DISPATCHER # pylint: disable=W0603

    try:
        client_id = request.form["client_id"]
        username = request.form["username"]
        password = request.form["password"]
        remember = False
        if "remember" in request.form:
            if request.form["remember"] == "X":
                remember = True

        client_db = _DISPATCHER.get_client_database(client_id)
        credential = None
        if client_db.client.authorization_active:
            credential = Credential(username=username, password=password)
            if client_db.client.authenticate(credential) is None:
                return redirect(url_for("_login"), code=302)
            if remember:
                credential.generate_token()
                client_db.update_user_credential(credential)

        session["client_id"] = client_db.client_id
        resp = make_response(redirect(url_for("_home"), code=302))
        if credential is not None and credential.token != "":
            resp.set_cookie("token", credential.token)
        return resp

    except Exception: # pylint: disable=W0703
        return redirect(url_for("_login"), code=302)

@_APP.route("/logoff")
def _logoff():
    session["client_id"] = ""
    resp = make_response(redirect(url_for("_login"), code=302))
    resp.set_cookie("token", "")
    return resp

##############################
# Misc
##############################

@_APP.route("/about")
def _about():
    global _DISPATCHER # pylint: disable=W0603

    return render_template("about.html",
                           version=databus.__version__,
                           author=databus.AUTHOR,
                           email=databus.EMAIL,
                           description=databus.DESCRIPTION,
                           python_version=databus.PYTHON_VERSION,
                           dispatcher=_DISPATCHER)

##############################
# Utility
##############################

def _download_attachment(att: Attachment):
    if att is None:
        return "File not found"
    if att.format == AttachmentFormat.binary:
        return send_file(io.BytesIO(att.binary_content),
                         attachment_filename=att.name,
                         as_attachment=True)
    if att.format == AttachmentFormat.text:
        return att.text_content
    return "Unexpected attachment format"

def _get_cache_buster() -> str:
    return "&cache_buster=" + str(uuid.uuid1())

def _get_authenticated_client_id() -> str:
    global _DISPATCHER # pylint: disable=W0603

    if "client_id" in session and session["client_id"] != "":
        if _is_client_id_valid(session["client_id"]):
            return session["client_id"]

    token = request.cookies.get("token")
    if token != "":
        client_user = ClientUserFinder(_DISPATCHER).find_by_token(token)
        if client_user is not None:
            session["client_id"] = client_user.client.id
            return client_user.client.id

    return None

def _is_client_id_valid(p_client_id: str):
    global _DISPATCHER # pylint: disable=W0603
    for client in _DISPATCHER.all_clients:
        if client.id == p_client_id:
            return True
    return False
