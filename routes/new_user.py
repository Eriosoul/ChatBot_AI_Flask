from mysql.connector import Error
from db.connection_db import DataBaseConnection  # Importamos la clase de conexión

class NewUser:
    def __init__(self, conn):
        self.conn = conn  # Pasamos la conexión como argumento

    def user_new(self):
        name = input("Nombre: ")
        proname = input("Apellidos: ")
        mail = input("Email: ")
        phone = input("Teléfono: ")
        try:
            # Usamos un cursor con administrador de contexto
            with self.conn.cursor() as cursor:
                # Consulta parametrizada para evitar inyección SQL
                query = "INSERT INTO clientes (nombre, apellidos, email, telefono) VALUES (%s, %s, %s, %s)"
                params = (name, proname, mail, phone)
                cursor.execute(query, params)
                self.conn.commit()  # Guardamos los cambios en la base de datos
                print("Nuevo usuario creado correctamente")
        except Error as ex:
            print("Ha ocurrido un error: ", ex)

# Punto de entrada principal
if __name__ == '__main__':
    db = DataBaseConnection()  # Creamos una instancia de conexión
    if db.conn:  # Verificamos que la conexión fue exitosa
        nu = NewUser(db.conn)  # Pasamos la conexión a la clase NewUser
        nu.user_new()
        db.close_connection()  # Cerramos la conexión después de usarla
