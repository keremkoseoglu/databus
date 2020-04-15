""" Json database implementation module for client """
import json
from os import path, scandir
from typing import List
from databus import get_root_path
from databus.client.client import Client, ClientError, ClientPassenger
from databus.database.json_db.json_database_arguments import JsonDatabaseArguments


class JsonClient:
    """ JSON database implementation for client """

    def __init__(self, args: JsonDatabaseArguments):
        self._args = args

    def build_client_dir_path(self, p_client_id: str) -> str:
        """ Builds the concrete path for client directory """
        client_root_path = self.build_client_root_path()
        return path.join(client_root_path, p_client_id)

    def build_client_root_path(self) -> str:
        """ Builds the concrete root path of client directories """
        databus_root = get_root_path()
        return path.join(databus_root, self._args.database_dir, self._args.client_dir)

    def get_all(self) -> List[Client]:
        """ Returns all clients """
        output = []
        for client_directory in self.get_client_directories():
            config_file_path = path.join(self._args.database_dir,
                                         self._args.client_dir,
                                         client_directory,
                                         self._args.client_config)

            with open(config_file_path) as config_json_file:
                config_json = json.load(config_json_file)

                client_passengers = []
                for passenger_json in config_json["passengers"]:
                    client_passenger = ClientPassenger(
                        p_name=passenger_json["name"],
                        p_puller_modules=passenger_json["pullers"],
                        p_queue_module=passenger_json["queue"],
                        p_processor_modules=passenger_json["processors"],
                        p_pusher_modules=passenger_json["pushers"],
                        p_sync_frequency=passenger_json["sync_frequency"],
                        p_queue_life_span=passenger_json["queue_life_span"])
                    client_passengers.append(client_passenger)

                client_obj = Client(p_id=client_directory,
                                    p_passengers=client_passengers,
                                    p_log_life_span=config_json["log_life_span"])

                output.append(client_obj)
        return output

    def get_client_directories(self) -> List[str]:
        """ Returns all client directories """
        return [f.name for f in scandir(self.build_client_root_path()) if f.is_dir()]

    def get_single(self, p_id: str) -> Client:
        """ Returns a single client """
        if p_id == "" or p_id is None:
            raise ClientError(ClientError.ErrorCode.parameter_missing)
        all_clients = self.get_all()
        for client in all_clients:
            if client.id == p_id:
                return client
        raise ClientError(ClientError.ErrorCode.client_not_found, p_client_id=p_id)
