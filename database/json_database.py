from client.client import Client
from client.log import Log
from config.constants import *
from database.abstract_database import AbstractDatabase
from database.json_client import *
from database.json_log import *
from datetime import datetime
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

    def get_clients(self) -> List[Client]:
        output = []
        for client_directory in get_client_directories():
            client_obj = Client(client_directory)
            output.append(client_obj)
        return output

    def insert_log(self, p_log: Log):
        log_file_content = build_log_file_content(p_log)
        log_file_path = build_log_file_path(p_log)

        log_file = open(log_file_path, "w+")
        log_file.write(log_file_content)
        log_file.close()
