from flask import Blueprint, session, redirect, url_for, flash
from functools import wraps

from db.queries import QuitSessionWhenLogOut

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


@auth_bp.route('/logout')
def logout():
    # Eliminar sesiones del usuario actual
    QuitSessionWhenLogOut.delete_user_sessions()
    # Limpiar la sesión de Flask
    session.clear()
    flash("Has cerrado sesión exitosamente.", "success")
    return redirect(url_for('login.login'))


