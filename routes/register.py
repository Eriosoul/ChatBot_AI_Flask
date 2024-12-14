import hashlib
from mysql.connector import Error
from flask import Blueprint, render_template, request, flash, redirect, url_for
from db.connection_db import DataBaseConnection

register_bp = Blueprint('register', __name__)

@register_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form.get('nombre')
        proname = request.form.get('apellido')
        mail = request.form.get('email')
        password = request.form.get('password')
        phone = request.form.get('telefono')

        metodo_cript = hashlib.sha256()
        metodo_cript.update(password.encode())
        hashed_password = metodo_cript.hexdigest()

        try:
            db = DataBaseConnection()
            if not db.conn:
                raise Error("Conexión fallida a la base de datos.")
            with db.conn.cursor() as cursor:
                query = """
                    INSERT INTO clientes (name, surnames, mail, phone, password)
                    VALUES (%s, %s, %s, %s, %s)
                """
                params = (name, proname, mail, phone, hashed_password)
                cursor.execute(query, params)
                db.conn.commit()
                flash("Usuario registrado correctamente", "success")
            db.close_connection()
            return redirect(url_for('login.login'))
        except Error as e:
            flash(f"Error con la base de datos: {e.msg}", "danger")
            return redirect(url_for('errors.generic_error'))
        except Exception as ex:
            flash(f"Error inesperado: {ex}", "danger")
            return redirect(url_for('errors.generic_error'))

    return render_template('register.html')


# from mysql.connector import Error
# from db.connection_db import DataBaseConnection  # Importamos la clase de conexión
#
# class NewUser:
#     def __init__(self, conn):
#         self.conn = conn  # Pasamos la conexión como argumento
#
#     def user_new(self):
#         name = input("Nombre: ")
#         proname = input("Apellidos: ")
#         mail = input("Email: ")
#         phone = input("Teléfono: ")
#         try:
#             # Usamos un cursor con administrador de contexto
#             with self.conn.cursor() as cursor:
#                 # Consulta parametrizada para evitar inyección SQL
#                 query = "INSERT INTO clientes (nombre, apellidos, email, telefono) VALUES (%s, %s, %s, %s)"
#                 params = (name, proname, mail, phone)
#                 cursor.execute(query, params)
#                 self.conn.commit()  # Guardamos los cambios en la base de datos
#                 print("Nuevo usuario creado correctamente")
#         except Error as ex:
#             print("Ha ocurrido un error: ", ex)
#
# # Punto de entrada principal
# if __name__ == '__main__':
#     db = DataBaseConnection()  # Creamos una instancia de conexión
#     if db.conn:  # Verificamos que la conexión fue exitosa
#         nu = NewUser(db.conn)  # Pasamos la conexión a la clase NewUser
#         nu.user_new()
#         db.close_connection()  # Cerramos la conexión después de usarla
