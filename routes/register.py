import hashlib
from flask import Blueprint, render_template, request, flash, redirect, url_for
from db.connection_db import DataBaseConnection

register_bp = Blueprint('register', __name__)

@register_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        # Capturamos los datos del formulario
        name = request.form.get('nombre')
        proname = request.form.get('apellido')
        mail = request.form.get('email')
        password = request.form.get('password')  # En una app real, encripta la contraseña
        phone = request.form.get('telefono')

        metodo_cript = hashlib.sha256()
        metodo_cript.update(password.encode())
        hashed_password = metodo_cript.hexdigest()

        try:
            # Conexión a la base de datos
            db = DataBaseConnection()
            if db.conn:
                with db.conn.cursor() as cursor:
                    # Consulta SQL para insertar datos
                    query = """
                        INSERT INTO clientes (name, surnames, mail, phone, password)
                        VALUES (%s, %s, %s, %s, %s)
                    """
                    params = (name, proname, mail, phone, hashed_password)
                    cursor.execute(query, params)
                    db.conn.commit()  # Guardamos los cambios
                    flash("Usuario registrado correctamente", "success")
                db.close_connection()
                # Si el registro es exitoso, redirige al formulario de login
                return redirect(url_for('login'))
        except Exception as ex:
            flash(f"Error al registrar usuario: {ex}", "danger")

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
