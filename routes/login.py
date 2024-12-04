from flask import Blueprint, render_template, request, flash, redirect, url_for, session
import hashlib
import secrets
from datetime import datetime, timedelta
from db.connection_db import DataBaseConnection

login_bp = Blueprint('login', __name__)

@login_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        try:
            db = DataBaseConnection()
            if db.conn:
                with db.conn.cursor(dictionary=True) as cursor:
                    query = "SELECT id, mail, password FROM clientes WHERE mail = %s"
                    cursor.execute(query, (email,))
                    user = cursor.fetchone()

                if user:
                    hashed_input_password = hashlib.sha256(password.encode()).hexdigest()
                    if hashed_input_password == user['password']:
                        session['user_id'] = user['id']
                        session['token'] = secrets.token_hex(32)
                        flash("Inicio de sesión exitoso.", "success")
                        return redirect(url_for('home.home'))
                    else:
                        flash("Contraseña incorrecta.", "danger")
                else:
                    flash("El usuario no existe.", "danger")

        except Exception as e:
            flash(f"Error al iniciar sesión: {e}", "danger")
        finally:
            if db.conn:
                db.close_connection()

    return render_template('login.html')
