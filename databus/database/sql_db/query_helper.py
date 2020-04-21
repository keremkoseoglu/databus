from typing import List
from databus.database.sql_db.driver.pyodbc_driver import PyodbcDriver
from databus.database.sql_db.insert_builder import InsertBuilder
from databus.database.sql_db.path_builder import PathBuilder
from databus.database.sql_db.sql_database_arguments import SqlDatabaseArguments
from databus.database.sql_db.update_builder import UpdateBuilder
from databus.database.sql_db.where_builder import WhereBuilder

class QueryHelper:
    """ Helper class to access SQL server easier """
    def __init__(self, p_arguments: dict, p_client_id: str, p_auto_commit: bool = False):
        self.args = SqlDatabaseArguments(p_arguments)
        self._client_id = p_client_id
        self._driver = PyodbcDriver()
        self._driver.autocommit = p_auto_commit
        self._driver.connect(SqlDatabaseArguments(p_arguments))
        self._where = WhereBuilder(p_client_id=self._client_id)
        self._path_builder = PathBuilder(self.args)

    @property
    def autocommit(self) -> bool:
        """ Are commands committed automatically """
        return self._driver.autocommit

    @autocommit.setter
    def autocommit(self, p_active: bool):
        """ Are commands committed automatically """
        self._driver.autocommit = p_active

    def commit(self):
        """ Runs a commit operation via the driver """
        self._driver.commit()

    def delete(self, p_table: str, p_where: str = ""):
        """ Deletes entries from SQL server """
        command = "DELETE FROM " + self._path_builder.get_table_path(p_table) + self._where.build(p_where)
        self._driver.execute_sql(command)

    def execute_insert(self, p_insert: InsertBuilder):
        """ Executes an Insert statement """
        self._driver.execute_sql(p_insert.insert_command)

    def execute_update(self, p_update: UpdateBuilder):
        """ Executes an Insert statement """
        self._driver.execute_sql(p_update.update_command)

    def select_all(self, p_table: str, p_where: str = "", p_order_fields: List[str] = None) -> dict:
        """ Selects & returns all entries from table
        The where condition will be touched - client id will be added automatically
        """
        where = self._where.build(p_where, p_order_fields=p_order_fields)
        return self.select_all_literal_where(p_table, p_literal_where=where)

    def select_all_literal_where(self, p_table: str, p_literal_where: str = "") -> List[dict]:
        """ Selects & returns all entries from table
        The where condition is used as a literal value, so it's not polluted by
        client ID or anything.
        """
        query = "SELECT * FROM " + self._path_builder.get_table_path(p_table) + p_literal_where
        return self._driver.select(query)

    def select_all_no_where(self, p_table: str, p_order_by: str = "") -> dict:
        """ Selects & returns all entries from table, without WHERE conditions """
        query = "SELECT * FROM " + self._path_builder.get_table_path(p_table)
        if p_order_by != "":
            query += " ORDER BY " + p_order_by
        return self._driver.select(query)

    def select_all_where_builder(self, p_table: str, p_builder: WhereBuilder) -> dict:
        """ Selects & returns all entries from table which match the builder """
        return self.select_all_literal_where(p_table, p_builder.where)

    def select_single(self, p_table: str, p_where: str = "") -> dict:
        """ Selects & returns a single entry
        The where condition will be touched - client id will be added automatically
        """
        where = self._where.build(p_where)
        return self.select_all_literal_where(p_table, p_literal_where=where)[0]
