""" Module to build update conditions """
from databus.database.sql_db.modifiable import Modifiable
from databus.database.sql_db.where_builder import WhereBuilder

class UpdateBuilder(Modifiable):
    """ Helper class to build update commands """
    def __init__(self, p_client_id: str = ""):
        super().__init__(p_client_id)
        self.where = WhereBuilder(p_client_id)
        self.clear()

    @property
    def update_command(self) -> str:
        """ Update command """
        query = "UPDATE " + self.table + " SET "

        first_val = True
        for keyval in self._key_values:
            if not first_val:
                query += ", "
            query += keyval.key + " = "
            if keyval.is_string:
                query += "'"
            query += keyval.val # todo özel karakterlere dikkat INSERT ile ortak
            if keyval.is_string:
                query += "' "
            first_val = False

        query += self.where.where
        return query


    def clear(self):
        """ Reset """
        super.clear()
        self.where.clear()
