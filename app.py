import secrets
import hashlib
from mysql.connector import Error
from db.connection_db import DataBaseConnection
from flask import Flask, render_template, request, jsonify, flash, redirect, url_for
from routes.login import login_bp
from routes.register import register_bp
# from chatbot import get_response, predict_class, intents_json


app = Flask(__name__)

app.secret_key = secrets.token_hex(16)
print(app.secret_key)

app.register_blueprint(login_bp)
# @app.post("/predict")
# def predict():
#     text = request.get_json().get("message")
#     intents = predict_class(text)
#     response = get_response(intents, intents_json)
#     message = {"answer": response}
#     return jsonify(message)
#
# @app.route('/login', methods=['GET', 'POST'])
# def login():
#     print("Método login")
#     if request.method == 'POST':
#         email = request.form.get('email')
#         password = request.form.get('password')
#         print(f"Contraseña recibida: {password}")
#         print(f"Email recibido: {email}")  # Verifica que el email se obtiene correctamente
#
#         try:
#             # Conexión a la base de datos
#             db = DataBaseConnection()
#             if db.conn:
#                 print("Conexión establecida en login")
#                 with db.conn.cursor(dictionary=True) as cursor:
#                     # Consulta parametrizada para obtener el correo y la contraseña
#                     query = "SELECT mail, password FROM clientes WHERE mail = %s"
#                     cursor.execute(query, (email,))
#
#                     # Usamos fetchone para obtener solo un resultado
#                     user = cursor.fetchone()
#                     print("Consulta a base de datos hecha")
#                     print(f"Resultado de la consulta: {user}")  # Verifica lo que devuelve la consulta
#
#                     # Aquí nos aseguramos de que no haya más resultados pendientes
#                     db.conn.commit()  # Asegura que no haya resultados pendientes
#
#                 if user:
#                     print("Comprobando usuario")
#                     # Obtener el hash almacenado de la base de datos
#                     stored_hashed_password = user['password']
#
#                     # Aplicar el mismo hash a la contraseña ingresada
#                     metodo_cript = hashlib.sha256()
#                     metodo_cript.update(password.encode())
#                     hashed_input_password = metodo_cript.hexdigest()
#
#                     # Mostrar los hashes para ver si coinciden
#                     print(f"Contraseña encriptada: {hashed_input_password}")
#                     print(f"Contraseña almacenada: {stored_hashed_password}")
#
#                     # Verificar si los hashes coinciden
#                     if hashed_input_password == stored_hashed_password:
#                         flash("Login exitoso", "success")
#                         print("Login exitoso")  # Verifica en la consola
#                         return redirect(url_for('home'))  # Redirige a la página de inicio
#                     else:
#                         flash("Contraseña incorrecta", "danger")
#                         print("Contraseña incorrecta")  # Para depurar si entra aquí
#                 else:
#                     flash("El usuario no existe", "danger")
#                     print("El usuario no existe")  # Para depurar si entra aquí
#
#         except Exception as ex:
#             flash(f"Error al intentar iniciar sesión: {ex}", "danger")
#             print(f"Error: {ex}")  # Para obtener más detalles sobre el error
#         finally:
#             # Cerrar la conexión a la base de datos
#             if db.conn:
#                 db.close_connection()
#
#     return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
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
        except Error as ex:
            flash(f"Error al registrar usuario: {ex}", "danger")

    # Si hay un error o es una solicitud GET, renderiza el formulario de registro
    return render_template('register.html')

@app.get("/home")
def home():
    return render_template('base.html')

if __name__ == '__main__':
    app.run(debug=True)
