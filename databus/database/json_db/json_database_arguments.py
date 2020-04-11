""" Json database argument module """
from enum import Enum


class JsonDatabaseArgumentError(Exception):
    """ Json database argument exception """

    class ErrorCode(Enum):
        """ Error code """
        invalid_argument: 1

    def __init__(self, p_error_code: ErrorCode, p_argument: str = ""):
        super().__init__()
        self.error_code = p_error_code

        if p_argument is None:
            self.argument = ""
        else:
            self.argument = p_argument

    @property
    def message(self) -> str:
        """ Error message as string """
        if self.error_code == JsonDatabaseArgumentError.ErrorCode.invalid_argument:
            return "Invalid JsonDatabase argument: " + self.argument
        return "JsonDatabase argument error"


class JsonDatabaseArguments: # pylint: disable=R0902, R0903
    """ Json database argument class """
    KEY_CLIENT_CONFIG = "client_config"
    KEY_CLIENT_DIR = "client_dir"
    KEY_DATABASE_DIR = "database_dir"
    KEY_LOG_DIR = "log_dir"
    KEY_LOG_EXTENSION = "log_extension"
    KEY_QUEUE_ATTACHMENT_DIR = "queue_attachment_dir"
    KEY_QUEUE_DIR = "queue_dir"
    KEY_QUEUE_PASSENGER = "queue_passenger"

    def __init__(self, p_arguments: dict):
        self.client_config = "config.json"
        self.client_dir = "clients"
        self.database_dir = "databus/database/json_db"
        self.log_dir = "log"
        self.log_extension = "txt"
        self.queue_attachment_dir = "attachments"
        self.queue_dir = "pqueue"
        self.queue_passenger = "passenger.json"

        for key in p_arguments:
            if key == JsonDatabaseArguments.KEY_CLIENT_CONFIG:
                self.client_config = p_arguments[key]
            elif key == JsonDatabaseArguments.KEY_CLIENT_DIR:
                self.client_dir = p_arguments[key]
            elif key == JsonDatabaseArguments.KEY_DATABASE_DIR:
                self.database_dir = p_arguments[key]
            elif key == JsonDatabaseArguments.KEY_LOG_DIR:
                self.log_dir = p_arguments[key]
            elif key == JsonDatabaseArguments.KEY_LOG_EXTENSION:
                self.log_extension = p_arguments[key]
            elif key == JsonDatabaseArguments.KEY_QUEUE_ATTACHMENT_DIR:
                self.queue_attachment_dir = p_arguments[key]
            elif key == JsonDatabaseArguments.KEY_QUEUE_DIR:
                self.queue_dir = p_arguments[key]
            elif key == JsonDatabaseArguments.KEY_QUEUE_PASSENGER:
                self.queue_passenger = p_arguments[key]
            else:
                raise JsonDatabaseArgumentError(
                    JsonDatabaseArgumentError.ErrorCode.invalid_argument,
                    p_argument=key)
