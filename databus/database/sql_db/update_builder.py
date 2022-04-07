""" Module to build update conditions """
from databus.database.sql_db.sql_database_arguments import SqlDatabaseArguments
from databus.database.sql_db.modifiable import Modifiable
from databus.database.sql_db.where_builder import WhereBuilder

class UpdateBuilder(Modifiable):
    """ Helper class to build update commands """
    def __init__(self, p_args: SqlDatabaseArguments, p_client_id: str = ""):
        super().__init__(p_args, p_client_id)
        self.where = WhereBuilder(p_client_id)

    @property
    def update_command(self) -> str:
        """ Update command """
        query = f"UPDATE {self.table} SET "

        first_val = True
        for keyval in self._key_values:
            if not first_val:
                query += ", "
            query += keyval.key + " = "
            if keyval.is_string:
                query += "'"
            query += Modifiable._get_safe_string(keyval.val)
            if keyval.is_string:
                query += "' "
            first_val = False

        query += self.where.where
        return query


    def clear(self):
        """ Reset """
        super().clear()
        try:
            self.where.clear()
        except Exception: # pylint: disable=W0703
            pass
