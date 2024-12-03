from flask import Blueprint, render_template, request, flash, redirect, url_for
import hashlib
from db.connection_db import DataBaseConnection

login_bp = Blueprint('login', __name__)  # Nombre del Blueprint

@login_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        try:
            db = DataBaseConnection()
            if db.conn:
                with db.conn.cursor(dictionary=True) as cursor:
                    query = "SELECT mail, password FROM clientes WHERE mail = %s"
                    cursor.execute(query, (email,))
                    user = cursor.fetchone()

                if user:
                    stored_hashed_password = user['password']
                    metodo_cript = hashlib.sha256()
                    metodo_cript.update(password.encode())
                    hashed_input_password = metodo_cript.hexdigest()

                    if hashed_input_password == stored_hashed_password:
                        flash("Login exitoso", "success")
                        return redirect(url_for('home'))  # Endpoint correcto aquí
                    else:
                        flash("Contraseña incorrecta", "danger")
                else:
                    flash("El usuario no existe", "danger")

        except Exception as ex:
            flash(f"Error al intentar iniciar sesión: {ex}", "danger")
        finally:
            if db.conn:
                db.close_connection()

    return render_template('login.html')
