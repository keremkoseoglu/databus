""" Module for web interface 
This mini web interfaces is based on Flask.
It uses the darkly theme available at https://bootswatch.com/darkly/
"""
from flask import Flask, render_template
import databus
from databus.dispatcher.abstract_dispatcher import AbstractDispatcher


##############################
# Main stuff
##############################

_app = Flask(__name__)
_dispatcher: AbstractDispatcher


async def run_web_server(dispatcher: AbstractDispatcher):
    """ Starts the Flask Web Server """
    global _dispatcher
    _dispatcher = dispatcher
    print(_dispatcher.ticket.database_module)
    _app.run()

##############################
# Home page
##############################

@_app.route("/")
def _home():
    global _dispatcher
    print(_dispatcher.ticket.database_module)
    return render_template("home.html")

##############################
# Log pages
##############################

@_app.route("/log_list")
def _log_list():
    # todo
    return render_template("log_list.html")


@_app.route("/log_display")
def _log_display():
    # todo
    return render_template("log_display.html")

##############################
# Queue pages
##############################

@_app.route("/queue_list")
def _queue_list():
    # todo
    # - log ile ortak olabilir mi?
    # - tamamla
    return render_template("queue_list.html")


@_app.route("/queue_display")
def _queue_display():
    # todo
    # - log ile ortak olabilir mi?
    # - tamamla
    return render_template("queue_display.html")

##############################
# Misc. pages
##############################

@_app.route("/about")
def _about():
    # todo
    # - kim yazmış
    # - setup.py içerisinden versiyonu yaz
    return render_template("about.html", 
                           version=databus.__version__, 
                           author=databus.AUTHOR,
                           email=databus.EMAIL,
                           description=databus.DESCRIPTION,
                           python_version=databus.PYTHON_VERSION)
