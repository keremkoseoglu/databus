""" Module to build insert conditions """
from databus.database.sql_db.modifiable import Modifiable


class InsertBuilder(Modifiable):
    """ Helper class to build insert commands """

    @property
    def insert_command(self) -> str:
        """ Insert command """
        query = "INSERT INTO " + self.table + " (client_id "

        for keyval in self.key_values:
            query += " , " + keyval.key

        query += " ) VALUES ( '" + self._client_id + "' "

        for keyval in self.key_values:
            query += " , "
            if keyval.is_string:
                query += "'"
            query += Modifiable._get_safe_string(keyval.val)
            if keyval.is_string:
                query += "'"

        query += ")"

        return query
