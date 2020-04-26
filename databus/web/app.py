""" Module for web interface
This mini web interfaces is based on Flask.
Theme help: https://bootswatch.com/darkly/
"""
import io
import uuid
from flask import Flask, redirect, render_template, request, send_file, url_for
from waitress import serve
import databus
from databus.dispatcher.abstract_dispatcher import AbstractDispatcher
from databus.passenger.attachment import Attachment, AttachmentFormat
from databus.pqueue.queue_status import QueueStatus
from databus.report.client_log import ClientLogReader
from databus.report.client_queue import ClientPassengerQueueReader
from databus.report.puller_peek import PullerPeek


##############################
# Main stuff
##############################

_APP = Flask(__name__)
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
    global _DISPATCHER # pylint: disable=W0603
    return render_template("home.html")

##############################
# Log pages
##############################

@_APP.route("/log_list")
def _log_list():
    global _DISPATCHER # pylint: disable=W0603
    entries = ClientLogReader(_DISPATCHER).get_client_log_list()
    return render_template("log_list.html", entries=entries)


@_APP.route("/log_display")
def _log_display():
    client_id = request.args.get("client", 0, type=str)
    log_file = request.args.get("log", 0, type=str)
    file_content = ClientLogReader(_DISPATCHER).get_client_log_content(client_id, log_file).replace("\n", "<br><br>") # pylint: disable=C0301
    return file_content

##############################
# Queue pages
##############################

@_APP.route("/queue_list")
def _queue_list():
    global _DISPATCHER # pylint: disable=W0603
    entries = ClientPassengerQueueReader(_DISPATCHER).get_client_passenger_queue_list()
    return render_template("queue_list.html", entries=entries)


@_APP.route("/queue_display")
def _queue_display():
    global _DISPATCHER # pylint: disable=W0603
    client = request.args.get("client", 0, type=str)
    passenger = request.args.get("passenger", 0, type=str)
    entry = ClientPassengerQueueReader(_DISPATCHER).get_client_passenger_queue_entry(client, passenger) # pylint: disable=C0301
    return render_template("queue_display.html", client=client, entry=entry)

@_APP.route("/queue_attachment")
def _queue_attachment():
    global _DISPATCHER # pylint: disable=W0603
    client = request.args.get("client", 0, type=str)
    passenger = request.args.get("passenger", 0, type=str)
    file = request.args.get("file", 0, type=str)
    entry = ClientPassengerQueueReader(_DISPATCHER).get_client_passenger_queue_entry(client, passenger) # pylint: disable=C0301

    for att in entry.passenger.attachments:
        if att.name == file:
            return _download_attachment(att)

    return "File not found"

@_APP.route("/queue_status_update")
def _queue_status_update():
    global _DISPATCHER # pylint: disable=W0603
    client = request.args.get("client", "", type=str)
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
    redirect_url += _get_cache_buster
    return redirect(redirect_url, code=302)

##############################
# Passengers
##############################

@_APP.route("/passenger_list")
def _passenger_list():
    global _DISPATCHER # pylint: disable=W0603
    clients = _DISPATCHER.all_clients
    try:
        expedited = request.args.get("expedited", 0, type=str) == "true"
    except Exception: # pylint: disable=W0703
        expedited = False
    return render_template("passenger_list.html", clients=clients, expedited=expedited)

@_APP.route("/passenger_expedite")
def _passenger_expedite():
    global _DISPATCHER # pylint: disable=W0603
    client = request.args.get("client", 0, type=str)
    passenger = request.args.get("passenger", 0, type=str)
    _DISPATCHER.expedite_client_passenger(client, passenger)
    return redirect(url_for("_passenger_list") + "?expedited=true" + _get_cache_buster(), code=302)

##############################
# Misc. pages
##############################

@_APP.route("/peek")
def _peek():
    global _DISPATCHER # pylint: disable=W0603
    peek = PullerPeek(_DISPATCHER).peek()
    return render_template("peek.html", peek=peek)

@_APP.route("/peek_attachment")
def _peek_attachment():
    global _DISPATCHER # pylint: disable=W0603
    client = request.args.get("client", 0, type=str)
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
