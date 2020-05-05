""" Module to build delete conditions """
from databus.database.sql_db.sql_database_arguments import SqlDatabaseArguments
from databus.database.sql_db.modifiable import Modifiable
from databus.database.sql_db.where_builder import WhereBuilder

class DeleteBuilder(Modifiable):
    """ Helper class to build update commands """
    def __init__(self, p_args: SqlDatabaseArguments, p_client_id: str = ""):
        super().__init__(p_args, p_client_id)
        self.where = WhereBuilder(p_client_id)

    @property
    def delete_command(self) -> str:
        """ Delete command """
        query = "DELETE FROM " + self.table
        query += self.where.where
        return query


    def clear(self):
        """ Reset """
        super().clear()
        try:
            self.where.clear()
        except Exception: # pylint: disable=W0703
            pass
