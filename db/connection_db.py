import mysql.connector
from mysql.connector import Error

class DataBaseConnection:
    def __init__(self):
        self.conn = None
        self.connection_to_db()

    def connection_to_db(self):
        try:
            self.conn = mysql.connector.connect(
                host="localhost",
                port=3306,
                user="root",
                password="",
                database="hotel"
            )
            if self.conn.is_connected():
                print("Conexion establecida")
                print("Información del servidor:", self.conn.get_server_info())
        except Error as ex:
            print("Error en la conexión: ", ex)

    def close_connection(self):
        if self.conn and self.conn.get_server_info():
            self.conn.close()
            print("Conexión cerrada")

def test_db():
    db: DataBaseConnection = DataBaseConnection()
    db.connection_to_db()
    db.close_connection()