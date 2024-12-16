from flask import Blueprint, render_template, session, flash, redirect, url_for
from db.connection_db import DataBaseConnection
from db.queries import HotelQueries
from .auth import login_required

home_bp = Blueprint('home', __name__)

@home_bp.route('/home')
@login_required
def home():
    try:
        user_id = session.get('user_id')
        if not user_id:
            flash("No se encontró el ID del usuario en la sesión.", "danger")
            return redirect(url_for('login.login'))

        # Obtener los datos del usuario desde la sesión (ya están cargados en la sesión)
        user_data = session.get('user')
        if not user_data:
            flash("No se encontró información del usuario en la sesión.", "danger")
            return redirect(url_for('login.login'))

        # Obtener datos de los hoteles
        hotels = HotelQueries.get_all_hotels()

    except Exception as ex:
        flash(f"Error al cargar los datos del usuario: {ex}", "danger")
        return redirect(url_for('login.login'))

    # Renderizar la plantilla con los datos del usuario y los hoteles
    return render_template('home.html', user=user_data, hotels=hotels)

