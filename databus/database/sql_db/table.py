""" Module for a database table """
from typing import List
from databus.database.sql_db.query_helper import QueryHelper


class Table: # pylint: disable=R0903
    """ Database table class """
    _key_fields: dict = {}

    def __init__(self, p_query_helper: QueryHelper, p_name: str):
        self._query_helper = p_query_helper
        self._name = p_name

    @property
    def key_fields(self) -> List[str]:
        """ Returns a list of key fields """
        if self._name not in Table._key_fields:
            Table._key_fields[self._name] = []

            primary_keys = self._query_helper.select_all_literal_where(
                "primary_keys",
                p_literal_where=" WHERE table_name = '" + self._name + "'")

            for primary_key in primary_keys:
                if primary_key["column_name"] not in Table._key_fields[self._name]:
                    Table._key_fields[self._name].append(primary_key["column_name"])

        return Table._key_fields[self._name]
