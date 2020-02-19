from client.client import Client, ClientPassenger
from config.constants import *
import json
from os import path, scandir
from typing import List


class JsonClient:
    @staticmethod
    def build_client_dir_path(p_client_id: str) -> str:
        client_root_path = JsonClient.build_client_root_path()
        return path.join(client_root_path, p_client_id)

    @staticmethod
    def build_client_root_path() -> str:
        return path.join(JSON_DB_DATABASE_DIR, JSON_DB_CLIENT_DIR)

    @staticmethod
    def get_all() -> List[Client]:
        output = []
        for client_directory in JsonClient.get_client_directories():
            config_file_path = path.join(JSON_DB_DATABASE_DIR,
                                         JSON_DB_CLIENT_DIR,
                                         client_directory,
                                         JSON_DB_CLIENT_CONFIG)

            with open(config_file_path) as config_json_file:
                config_json = json.load(config_json_file)

                client_passengers = []
                for passenger_json in config_json["passengers"]:
                    client_passenger = ClientPassenger(p_name=passenger_json["name"],
                                                       p_puller_modules=passenger_json["pullers"],
                                                       p_queue_module=passenger_json["queue"],
                                                       p_processor_modules=passenger_json["processors"],
                                                       p_pusher_modules=passenger_json["pushers"],
                                                       p_sync_frequency=passenger_json["sync_frequency"])
                    client_passengers.append(client_passenger)

                client_obj = Client(p_id=client_directory,
                                    p_passengers=client_passengers)

                output.append(client_obj)
        return output

    @staticmethod
    def get_client_directories() -> List[str]:
        return [f.name for f in scandir(JsonClient.build_client_root_path()) if f.is_dir()]

    @staticmethod
    def get_single(p_id: str) -> Client:
        all_clients = JsonClient.get_all()
        for client in all_clients:
            if client.id == p_id:
                return client
        return None