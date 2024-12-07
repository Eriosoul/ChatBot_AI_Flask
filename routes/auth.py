from flask import Blueprint, session, redirect, url_for, flash
from functools import wraps

auth_bp = Blueprint('auth', __name__)

# Decorador para verificar si el usuario ha iniciado sesión
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash("Debes iniciar sesión para acceder a esta página.", "warning")
            return redirect(url_for('login.login'))
        return f(*args, **kwargs)
    return decorated_function

# Ruta para cerrar sesión
@auth_bp.route('/logout')
def logout():
    # Limpiar la sesión
    session.clear()
    flash("Has cerrado sesión exitosamente.", "success")
    return redirect(url_for('login.login'))  # Redirigir al login
