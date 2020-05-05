""" Json database implementation module for client """
import json
from os import path, scandir
from typing import List
from databus import get_root_path
from databus.client.client import Client, ClientError, ClientPassenger
from databus.client.user import User, Credential
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
            config_json = self.get_config_as_json(client_directory)
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

            client_users = []
            if "users" in config_json:
                for user_json in config_json["users"]:
                    credential = Credential(
                        username=user_json["username"],
                        password=user_json["password"],
                        token=user_json["token"])
                    user = User(credential=credential)
                    client_users.append(user)

            client_obj = Client(
                p_id=client_directory,
                p_passengers=client_passengers,
                p_log_life_span=config_json["log_life_span"],
                p_users=client_users)

            output.append(client_obj)
        return output

    def get_client_directories(self) -> List[str]:
        """ Returns all client directories """
        return [f.name for f in scandir(self.build_client_root_path()) if f.is_dir()]

    def get_config_as_json(self, p_client_id: str):
        """ Returns the contents of the config file as JSON """
        output = ""
        config_file_path = self._get_config_file_path(p_client_id)
        with open(config_file_path) as config_json_file:
            output = json.load(config_json_file)
        return output

    def get_config_as_string(self, p_client_id: str):
        """ Returns the contents of the config file as string """
        output = ""
        config_file_path = self._get_config_file_path(p_client_id)
        with open(config_file_path) as config_json_file:
            output = config_json_file.read()
        return output

    def get_single(self, p_id: str) -> Client:
        """ Returns a single client """
        if p_id == "" or p_id is None:
            raise ClientError(ClientError.ErrorCode.parameter_missing)
        all_clients = self.get_all()
        for client in all_clients:
            if client.id == p_id:
                return client
        raise ClientError(ClientError.ErrorCode.client_not_found, p_client_id=p_id)

    def save_config(self, p_client_id: str, p_config: str):
        """ Writes the provided configuration to the disk """
        config_file_path = self._get_config_file_path(p_client_id)
        with open(config_file_path, "w") as config_json_file:
            config_json_file.write(p_config)

    def update_user_credential(self, p_client_id: str, p_credential: Credential):
        """ Updates the credential of a client user """
        for client_directory in self.get_client_directories():
            if client_directory != p_client_id:
                continue
            config_file_path = self._get_config_file_path(client_directory)
            with open(config_file_path) as config_json_file:
                config_json = json.load(config_json_file)
            if "users" not in config_json:
                config_json["users"] = []
            user_found = False
            for user in config_json["users"]:
                if user["username"] == p_credential.username:
                    user_found = True
                    user["password"] = p_credential.password
                    user["token"] = p_credential.token
            if not user_found:
                user = {
                    "username": p_credential.username,
                    "password": p_credential.password,
                    "token": p_credential.token
                }
                config_json["users"].append(user)
            with open(config_file_path, "w") as config_json_file:
                json.dump(config_json, config_json_file, indent=4, sort_keys=True)
            return

    def _get_config_file_path(self, p_client_directory: str) -> str:
        return path.join(
            self._args.database_dir,
            self._args.client_dir,
            p_client_directory,
            self._args.client_config)
