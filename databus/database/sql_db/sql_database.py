""" Module for SQL databases
Credentials for development server:
databus-server.database.windows.net databus_db databus Honk+honk+2
"""
import pymssql

# todo
# - tabloları oluştur (binary nerede duracak)
# - abstract database yordamlarını uygula
# - schema oluşturmak için yeni yordam? gittiğimiz yerlerde elle mi açacağız?
# -- abstract'e ekle
# -- json'da olsun (ama boş olsun)
# -- burada olsun
# - main içerisinde test et
# - main'i eski haline getir
# - pylint
# - apply branch
# - versiyon yükselt

def test_connection():
    server = "databus-server.database.windows.net"
    database = "databus_db"
    username = "databus"
    password = "Honk+honk+2"
    conn = pymssql.connect(server=server,
                           user=username,
                           password=password,
                           database=database) 
    
    cursor = conn.cursor()
    cursor.execute("SELECT @@version;")
    row = cursor.fetchone()
    while row:
        print(row[0])
        row = cursor.fetchone()