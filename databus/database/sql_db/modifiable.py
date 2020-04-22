""" Module for modifiable key - values """
import binascii
from datetime import datetime
from typing import List
from databus.database.sql_db.path_builder import PathBuilder
from databus.database.sql_db.sql_database_arguments import SqlDatabaseArguments
from databus.database.sql_db.value_conversion import DatabusToSql


class KeyValue: # pylint: disable=R0903
    """ Key - Value to be used in modification """
    def __init__(self, p_key: str, p_val: str, p_is_string: bool):
        self.key = p_key
        self.val = p_val
        self.is_string = p_is_string


class Modifiable:
    """ Class for modifiable key - value pairs """
    def __init__(self, p_args: SqlDatabaseArguments, p_client_id: str):
        self._client_id = p_client_id
        self._key_values = []
        self._table = ""
        self._args = p_args
        self._path_builder = PathBuilder(p_args)
        self.clear()

    @property
    def key_values(self) -> List[KeyValue]:
        """ Returns the output """
        return self._key_values

    @property
    def table(self) -> str:
        """ Table to be inserted """
        return self._path_builder.get_table_path(self._table)

    @table.setter
    def table(self, p_table: str):
        """ Table setter """
        self.clear()
        self._table = p_table

    def add_binary(self, p_key: str, p_bin: bytearray):
        """ Adds binary content """
        filecontent_hex = '0x'.encode('ascii') + binascii.hexlify(p_bin)
        self.add_string(p_key, filecontent_hex)

    def add_datetime(self, p_key: str, p_val: datetime):
        """ Adds a new datetime """
        keyval = KeyValue(p_key, DatabusToSql.date_time(p_val), True)
        self._key_values.append(keyval)

    def add_int(self, p_key: str, p_val: int):
        """ Adds a new integer """
        keyval = KeyValue(p_key, str(p_val), False)
        self._key_values.append(keyval)

    def add_string(self, p_key: str, p_val):
        """ Adds a new string """
        keyval = KeyValue(p_key, str(p_val), True)
        self._key_values.append(keyval)

    def add_value(self, p_key_value: KeyValue):
        """ Adds a new key - value pair """
        self._key_values.append(p_key_value)

    def clear(self):
        """ Reset """
        self._key_values = []
        self._table = ""

    @staticmethod
    def _get_safe_string(p_input: str) -> str:
        return "{}".format(p_input).replace("'", "''")
