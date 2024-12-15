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

        # Obtener datos de los hoteles
        hotels = HotelQueries.get_all_hotels()
        print(hotels)  # Diagnóstico para verificar los datos

        # Conectar a la base de datos para obtener información del usuario
        db = DataBaseConnection()
        if db.conn:
            with db.conn.cursor(dictionary=True) as cursor:
                query = "SELECT name, mail FROM clientes WHERE id = %s"
                cursor.execute(query, (user_id,))
                user_data = cursor.fetchone()

                if not user_data:
                    flash("No se pudo encontrar el usuario en la base de datos.", "danger")
                    return redirect(url_for('login.login'))

    except Exception as ex:
        flash(f"Error al cargar los datos del usuario: {ex}", "danger")
        return redirect(url_for('login.login'))
    finally:
        if db and db.conn:
            db.close_connection()

    # Renderizar la plantilla con los datos del usuario y los hoteles
    return render_template('home.html', user=user_data, hotels=hotels)
