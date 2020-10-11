""" Module to build where conditions """
from datetime import datetime
from typing import List
from databus.database.sql_db.value_conversion import DatabusToSql


class WhereFlags: # pylint: disable=R0903
    """ Flags for where building """
    def __init__(self):
        self.has_where = False
        self.has_condition = False
        self.has_order_by = False

class WhereBuilder:
    """ Helper class to build where conditions """
    def __init__(self, p_client_id: str = ""):
        self._client_id = p_client_id
        self._flags = WhereFlags()
        self._where = ""
        self.clear()

    @staticmethod
    def date_lt(p_field: str, p_date: datetime):
        """ p_field < p_date """
        return p_field + " < '" + DatabusToSql.date_time(p_date) + "'"

    @staticmethod
    def int_eq(p_field: str, p_int: int):
        """ p_field = p_int """
        return p_field + " = " + str(p_int)

    @staticmethod
    def str_eq(p_field: str, p_str: str):
        """ p_field = 'p_str' """
        return p_field + " = '" + p_str + "'"

    @property
    def where(self) -> str:
        """ Where string """
        return self._where

    def add_and(self, p_condition: str):
        """ Adds a new and condition """
        if self._flags.has_order_by:
            raise Exception("Can't add conditions after ORDER BY")

        if p_condition is None or p_condition == "":
            return

        self._put_and()
        self._put_condition(p_condition)

    def add_and_date_lt(self, p_field: str, p_date: datetime):
        """ AND p_field > p_date """
        where_cond = WhereBuilder.date_lt(p_field, p_date)
        self.add_and(where_cond)

    def add_and_field_eq_int(self, p_field: str, p_int: int):
        """ AND p_field = p_int """
        where_cond = WhereBuilder.int_eq(p_field, p_int)
        self.add_and(where_cond)

    def add_and_field_eq_str(self, p_field: str, p_str: str):
        """ AND p_field = p_str """
        where_cond = WhereBuilder.str_eq(p_field, p_str)
        self.add_and(where_cond)

    def build(self, p_condition: str, p_order_fields: List[str] = None) -> str:
        """ Builds a new where condition """
        self.clear()
        self.add_and(p_condition)
        if p_order_fields is not None:
            self.set_order_by(p_order_fields)
        return self._where

    def build_without_client(self, p_condition: str) -> str:
        """ Builds a new where condition without using client id """
        self.clear(p_with_client=False)
        self._put_condition(p_condition)
        return self._where

    def clear(self, p_with_client: bool = True):
        """ Clears & starts anew """
        self._flags = WhereFlags()
        self._where = ""
        if p_with_client and self._client_id is not None and self._client_id != "":
            self._put_condition("client_id = '" + self._client_id + "'")

    def set_order_by(self, p_fields: List[str]):
        """ Order By """
        if self._flags.has_order_by:
            raise Exception("Can't set ORDER BY twice")

        if p_fields is None or len(p_fields) <= 0:
            return
        self._where += " ORDER BY "
        first_field = True
        for field in p_fields:
            if not first_field:
                self._where += ", "
            self._where += field
            first_field = False

        self._flags.has_order_by = True

    def _put_and(self):
        self._put_where()
        if self._flags.has_condition:
            self._where += " AND "

    def _put_condition(self, p_condition: str):
        self._put_where()
        self._where += " ( " + p_condition + " ) "
        self._flags.has_condition = True

    def _put_where(self):
        if self._flags.has_order_by:
            raise Exception("Can't put WHERE after ORDER BY")

        if not self._flags.has_where:
            self._where += " WHERE "
            self._flags.has_where = True
