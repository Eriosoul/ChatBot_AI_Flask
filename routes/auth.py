import os
from flask import Blueprint, session, redirect, url_for, flash
from functools import wraps

from db.queries import QuitSessionWhenLogOut

auth_bp = Blueprint('auth', __name__)

def clear_uploads_data():
    # Directorio donde se encuentran las fotos subidas
    folder_path = "./static/uploads/"  # Usa la ruta correcta a tu directorio
    files = os.listdir(folder_path)

    for name in files:
        # Comprobar si el archivo tiene una extensión válida (jpg, png)
        if name.endswith(("jpg", "png", "JPG", "PNG")):
            file_path = os.path.join(folder_path, name)  # Obtén la ruta completa del archivo
            print(f"Borrando archivo: {file_path}")
            os.remove(file_path)  # Elimina el archivo


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
    #eliminar la imagen temporal
    clear_uploads_data()
    # Limpiar la sesión de Flask
    session.clear()
    flash("Has cerrado sesión exitosamente.", "success")
    return redirect(url_for('login.login'))


