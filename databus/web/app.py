""" Module for web interface
This mini web interfaces is based on Flask.
Theme help: https://bootswatch.com/darkly/
"""
from flask import Flask, render_template # pylint: disable=C0301
from waitress import serve
from databus.dispatcher.abstract_dispatcher import AbstractDispatcher
from databus.web.controller.customizing import CustomizingEditController,\
    CustomizingListController, CustomizingSaveController
from databus.web.controller.export import \
    ExportController, ExportGetDictController, ExportExeController
from databus.web.controller.home import HomeController, AboutController
from databus.web.controller.log import LogDisplayController, LogListController, LogPurgeController
from databus.web.controller.login import LoginAttemptController, LogoffController
from databus.web.controller.passenger import PassengerExpediteController, PassengerListController
from databus.web.controller.peek import PeekAttachmentController, PeekController
from databus.web.controller.queue import QueueAttachmentController, QueueDisplayController,\
    QueueListController, QueuePurgeController, QueueStatusUpdateController
from databus.web.controller.user import UserListController, UserTokenRevokeController
from databus.web.controller.system import SystemController
from databus.web.controller.pause import PauseController
from databus.web.controller.resume import ResumeController
from databus.web.controller.shutdown import ShutdownController, ShutdownExeController
from databus.web import util

##############################
# Main stuff
##############################

_APP = Flask(__name__)
_APP.secret_key = "databus"
_APP.config["CACHE_TYPE"] = "null"
_APP.config["JSONIFY_PRETTYPRINT_REGULAR"] = True
_DISPATCHER: AbstractDispatcher


def run_web_server(dispatcher: AbstractDispatcher):
    """ Starts the Flask Web Server """
    global _DISPATCHER # pylint: disable=W0603
    _DISPATCHER = dispatcher
    serve(_APP, port=dispatcher.ticket.web_server_port)
    #_APP.run(port=dispatcher.ticket.web_server_port)

@_APP.context_processor
def databus_context_processor():
    """ Returns if the user is root or not, used in default template """
    return util.get_authorization()

##############################
# Home page
##############################

@_APP.route("/")
def _home():
    return HomeController(_DISPATCHER).execute()

@_APP.route("/about")
def _about():
    return AboutController(_DISPATCHER).execute()

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
# Users
##############################

@_APP.route("/user_list")
def _user_list():
    return UserListController(_DISPATCHER).execute()

@_APP.route("/user_token_revoke")
def _user_token_revoke():
    return UserTokenRevokeController(_DISPATCHER).execute()

##############################
# Customizing
##############################

@_APP.route("/customizing_list")
def _customizing_list():
    return CustomizingListController(_DISPATCHER).execute()

@_APP.route("/customizing_edit")
def _customizing_edit():
    return CustomizingEditController(_DISPATCHER).execute()

@_APP.route("/customizing_save", methods=["POST"])
def _customizing_save():
    return CustomizingSaveController(_DISPATCHER).execute()

##############################
# Export
##############################

@_APP.route("/export")
def _export():
    return ExportController(_DISPATCHER).execute()

@_APP.route("/export_get_dict")
def _export_get_dict():
    return ExportGetDictController(_DISPATCHER).execute()

@_APP.route("/export_exe", methods=["POST"])
def _export_exe():
    return ExportExeController(_DISPATCHER).execute()

##############################
# System
##############################

@_APP.route("/system")
def _system():
    return SystemController(_DISPATCHER).execute()

@_APP.route("/pause")
def _pause():
    return PauseController(_DISPATCHER).execute()

@_APP.route("/resume")
def _resume():
    return ResumeController(_DISPATCHER).execute()

@_APP.route("/shutdown")
def _shutdown():
    return ShutdownController(_DISPATCHER).execute()

@_APP.route("/shutdown_exe")
def _shutdown_exe():
    return ShutdownExeController(_DISPATCHER).execute()
