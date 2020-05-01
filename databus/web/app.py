""" Module for web interface
This mini web interfaces is based on Flask.
Theme help: https://bootswatch.com/darkly/
"""
from flask import Flask, render_template # pylint: disable=C0301
from waitress import serve
from databus.dispatcher.abstract_dispatcher import AbstractDispatcher
from databus.web.controller.home import HomeController, AboutController
from databus.web.controller.log import LogDisplayController, LogListController, LogPurgeController
from databus.web.controller.login import LoginAttemptController, LogoffController
from databus.web.controller.passenger import PassengerExpediteController, PassengerListController
from databus.web.controller.peek import PeekAttachmentController, PeekController
from databus.web.controller.queue import QueueAttachmentController, QueueDisplayController,\
    QueueListController, QueuePurgeController, QueueStatusUpdateController

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
    return HomeController(_DISPATCHER).execute()

##############################
# Log pages
##############################

@_APP.route("/log_list")
def _log_list():
    return LogListController(_DISPATCHER).execute()

@_APP.route("/log_display")
def _log_display():
    return LogDisplayController(_DISPATCHER).execute()

@_APP.route("/log_purge")
def _log_purge():
    return LogPurgeController(_DISPATCHER).execute()

##############################
# Queue pages
##############################

@_APP.route("/queue_list")
def _queue_list():
    return QueueListController(_DISPATCHER).execute()

@_APP.route("/queue_display")
def _queue_display():
    return QueueDisplayController(_DISPATCHER).execute()

@_APP.route("/queue_attachment")
def _queue_attachment():
    return QueueAttachmentController(_DISPATCHER).execute()

@_APP.route("/queue_status_update")
def _queue_status_update(): # pylint: disable=R0912
    return QueueStatusUpdateController(_DISPATCHER).execute()

@_APP.route("/queue_purge")
def _queue_purge():
    return QueuePurgeController(_DISPATCHER).execute()

##############################
# Passengers
##############################

@_APP.route("/passenger_list")
def _passenger_list():
    return PassengerListController(_DISPATCHER).execute()

@_APP.route("/passenger_expedite")
def _passenger_expedite():
    return PassengerExpediteController(_DISPATCHER).execute()

##############################
# Peek
##############################

@_APP.route("/peek")
def _peek():
    return PeekController(_DISPATCHER).execute()

@_APP.route("/peek_attachment")
def _peek_attachment():
    return PeekAttachmentController(_DISPATCHER).execute()

##############################
# Login
##############################

@_APP.route("/login")
def _login():
    return render_template("login.html")

@_APP.route("/login_attempt", methods=["POST"])
def _login_attempt():
    return LoginAttemptController(_DISPATCHER).execute()

@_APP.route("/logoff")
def _logoff():
    return LogoffController(_DISPATCHER).execute()

##############################
# Misc
##############################

@_APP.route("/about")
def _about():
    return AboutController(_DISPATCHER).execute()
