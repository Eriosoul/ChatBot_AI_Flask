from flask import Blueprint, render_template, request, flash, redirect, url_for, session
import hashlib
import secrets
from datetime import datetime, timedelta
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
                    # Consulta para verificar usuario y contraseña
                    query = "SELECT id, mail, password FROM clientes WHERE mail = %s"
                    cursor.execute(query, (email,))
                    user = cursor.fetchone()

                if user:
                    stored_hashed_password = user['password']
                    metod_cript = hashlib.sha256()
                    metod_cript.update(password.encode())
                    hashed_input_password = metod_cript.hexdigest()

                    if hashed_input_password == stored_hashed_password:
                        # Generar token y fecha de expiración
                        token = secrets.token_hex(32)  # Token único
                        expires_at = datetime.utcnow() + timedelta(hours=2)  # Expira en 2 horas
                        user_id = user['id']

                        # Guardar token en la tabla de sesiones
                        with db.conn.cursor() as cursor:
                            insert_query = """
                                INSERT INTO sessions (user_id, token, expires_at)
                                VALUES (%s, %s, %s)
                            """
                            cursor.execute(insert_query, (user_id, token, expires_at))
                            db.conn.commit()

                        # Guardar token en la sesión de Flask
                        session['user_id'] = user_id
                        print(f"Usuario con ID {session['user_id']} inició sesión")
                        session['token'] = token

                        flash("Login exitoso", "success")
                        return redirect(url_for('home.home'))  # Endpoint correcto aquí
                    else:
                        flash("Contraseña incorrecta", "danger")
                else:
                    flash("El usuario no existe", "danger")

        except Exception as ex:
            flash(f"Error al intentar iniciar sesión: {ex}", "danger")
            return redirect(url_for('errors.generic_error'))
        finally:
            if db.conn:
                db.close_connection()

    return render_template('login.html')
