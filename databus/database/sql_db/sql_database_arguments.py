""" SQL Server database argument module
This module has imitated the Sql database argument module
"""
from enum import Enum

class SqlDatabaseArgumentError(Exception):
    """ Sql database argument exception """

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
        if self.error_code == SqlDatabaseArgumentError.ErrorCode.invalid_argument:
            return f"Invalid SqlDatabase argument: {self.argument}"
        return "SqlDatabase argument error"


class SqlDatabaseArguments: # pylint: disable=R0902, R0903
    """ Sql database argument class """
    KEY_SERVER = "server"
    KEY_DATABASE = "database"
    KEY_USERNAME = "username"
    KEY_PASSWORD = "password"
    KEY_SCHEMA = "schema"

    TEMPLATE = {
        KEY_SERVER: "(server address)",
        KEY_DATABASE: "(database name)",
        KEY_USERNAME: "(username)",
        KEY_PASSWORD: "(password)",
        KEY_SCHEMA: "(database schema)"
    }

    def __init__(self, p_arguments: dict):
        for key in p_arguments:
            if key == SqlDatabaseArguments.KEY_SERVER:
                self.server = p_arguments[key]
            elif key == SqlDatabaseArguments.KEY_DATABASE:
                self.database = p_arguments[key]
            elif key == SqlDatabaseArguments.KEY_USERNAME:
                self.username = p_arguments[key]
            elif key == SqlDatabaseArguments.KEY_PASSWORD:
                self.password = p_arguments[key]
            elif key == SqlDatabaseArguments.KEY_SCHEMA:
                self.schema = p_arguments[key]
            else:
                raise SqlDatabaseArgumentError(
                    SqlDatabaseArgumentError.ErrorCode.invalid_argument,
                    p_argument=key)
