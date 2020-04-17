""" Main entry point for Databus execution """
from databus.dispatcher.primal_factory import PrimalDispatcherFactory
from databus.database.sql_db.sql_database import test_connection

if __name__ == "__main__":
    # todo
    # sql server bitecek
    # burayı eski haline getir
    # PrimalDispatcherFactory().create_dispatcher().start()
    test_connection()
