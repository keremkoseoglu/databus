from client.client import Client
from client.log import Log
from config.constants import *
from database.abstract_database import AbstractDatabase
from database.json_client import JsonClient
from database.json_log import JsonLog
from datetime import datetime
import json
from os import path
from puller.abstract_puller import AbstractPuller
from typing import List


class JsonDatabase(AbstractDatabase):
    def __init__(self):
        pass

    def delete_old_logs(self, p_before: datetime):
        # todo
        # tamamla
        # test ekle (münferit log silmek için; test sırasında iki log yarat birini sil)
        # aşağıdaki pass'i sil
        pass

    def get_client(self, p_name: str) -> Client:
        all_clients = self.get_clients()
        for client in all_clients:
            if client.name == p_name:
                return client
        return None

    def get_clients(self) -> List[Client]:
        output = []
        for client_directory in JsonClient.get_client_directories():
            config_file_path = path.join(JSON_DB_DATABASE_DIR,
                                         JSON_DB_CLIENT_DIR,
                                         client_directory,
                                         JSON_DB_CLIENT_CONFIG)

            with open(config_file_path) as config_json_file:
                config_json = json.load(config_json_file)

                client_obj = Client(p_name=client_directory,
                                    p_puller_modules=config_json["pullers"],
                                    p_processor_modules=config_json["processors"],
                                    p_pusher_modules=config_json["pushers"],
                                    p_sync_frequency=config_json["sync_frequency"])

                output.append(client_obj)
        return output

    def insert_log(self, p_client: Client, p_log: Log):
        log_file_content = JsonLog.build_log_file_content(p_log)
        log_file_path = JsonLog.build_log_file_path(p_client, p_log)

        log_file = open(log_file_path, "w+")
        log_file.write(log_file_content)
        log_file.close()
