""" Client customizing backup """
from databus.dispatcher.abstract_dispatcher import AbstractDispatcher

def backup_client_customizings(p_dispatcher: AbstractDispatcher):
    """ Backup client customizing"""
    customs = p_dispatcher.get_client_customizing_list()

    for custom in customs:
        db = p_dispatcher.get_client_database(custom.client.id)
        db.backup_customizing_nodes(custom)
