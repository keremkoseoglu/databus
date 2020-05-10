""" Json database implementation module for client """
from copy import copy
import json
from os import mkdir, path, scandir
from shutil import rmtree
from typing import List
from databus import get_root_path
from databus.client.client import Client, ClientError, ClientPassenger
from databus.client.user import User, Credential
from databus.database.difference_check import Action, DifferenceChecker, TableKey
from databus.database.json_db.json_database_arguments import JsonDatabaseArguments

class JsonClient:
    """ JSON database implementation for client """
    def __init__(self, args: JsonDatabaseArguments):
        self._args = args

    @property
    def all_clients(self) -> List[Client]:
        """ Returns all clients """
        output = []
        for client_directory in self.client_directories:
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

    @property
    def client_directories(self) -> List[str]:
        """ Returns all client directories """
        return [f.name for f in scandir(self.client_root_path) if f.is_dir()]

    @property
    def client_master_as_json(self) -> str:
        """ Returns client master data as a JSON string """
        output_dict = {"client": []}
        for client in self.all_clients:
            client_dict = {
                "client_id": client.id,
                "log_life_span": client.log_life_span
            }
            output_dict["client"].append(client_dict)
        return json.dumps(output_dict, indent=4, sort_keys=True)

    @client_master_as_json.setter
    def client_master_as_json(self, p_master: str):
        """ Saves client master data from JSON string
        Check getter for JSON format
        """
        memory_dict = json.loads(p_master)
        database_dict = json.loads(self.client_master_as_json)
        table_keys = [TableKey("client", ["client_id"])]

        diff_check = DifferenceChecker(table_keys, memory_dict, database_dict)

        for diff_result in diff_check.result:
            if diff_result.action == Action.INSERT:
                self._create_client(diff_result.row["client_id"], diff_result.row)
            elif diff_result.action == Action.UPDATE:
                self._save_config_dict(diff_result.row["client_id"], diff_result.row)
            elif diff_result.action == Action.DELETE:
                self._delete_client(diff_result.row["client_id"])

    @property
    def client_root_path(self) -> str:
        """ Builds the concrete root path of client directories """
        databus_root = get_root_path()
        return path.join(databus_root, self._args.database_dir, self._args.client_dir)

    def build_client_dir_path(self, p_client_id: str) -> str:
        """ Builds the concrete path for client directory """
        client_root_path = self.client_root_path
        return path.join(client_root_path, p_client_id)

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
        for client in self.all_clients:
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
        for client_directory in self.client_directories:
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

    def _create_client(self, p_client_id: str, p_base_dict: dict):
        client_dir = self.build_client_dir_path(p_client_id)
        mkdir(client_dir)
        self._save_config_dict(p_client_id, p_base_dict)

    def _delete_client(self, p_client_id: str):
        rmtree(self.build_client_dir_path(p_client_id))

    def _get_config_file_path(self, p_client_directory: str) -> str:
        return path.join(
            self._args.database_dir,
            self._args.client_dir,
            p_client_directory,
            self._args.client_config)

    def _save_config_dict(self, p_client_id: str, p_base_dict: dict):
        config = copy(p_base_dict)
        if "client_id" in config:
            del config["client_id"]
        if "log_life_span" not in config:
            config["log_life_span"] = 1
        if "passengers" not in config:
            config["passengers"] = []
        if "users" not in config:
            config["users"] = []

        self.save_config(p_client_id, json.dumps(config))
