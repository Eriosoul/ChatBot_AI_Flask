""" CODIGO VIEJO DEL PROFILE """
from flask import Blueprint, render_template, session, flash, redirect, url_for, request
from db.connection_db import DataBaseConnection
from db.queries import HotelReservationQueries

reservations_bp = Blueprint('reservations', __name__)
#
#
#
#
@reservations_bp.route('/reservations', methods=['GET', 'POST'], endpoint='reservations')
def profile():
    try:
        user_id = session.get('user_id')
        if not user_id:
            flash("No se encontró el ID del usuario en la sesión.", "danger")
            return redirect(url_for('login.login'))

        # Obtener los datos del usuario desde la sesión
        user_data = session.get('user')
        if not user_data:
            flash("No se encontró información del usuario en la sesión.", "danger")
            return redirect(url_for('login.login'))

        # Obtener las reservas con información de hoteles
        hotel_reservation = HotelReservationQueries.get_all_reservations_hotels()

        if not hotel_reservation:
            flash("No se encontraron reservas para este usuario.", "info")

        print(hotel_reservation)  # Depuración
    except Exception as ex:
        flash(f"Error al cargar los datos del usuario: {ex}", "danger")
        return redirect(url_for('login.login'))

    # Renderiza la plantilla con los datos de las reservas
    return render_template('reservations.html', user=user_data, reservas=hotel_reservation)
#
#     try:
#         db = DataBaseConnection()
#         if db.conn:
#             with db.conn.cursor(dictionary=True) as cursor:
#                 if request.method == 'POST':
#                     print(user_id)
#                     # Recogemos los datos del formulario
#                     name = request.form.get('nombre')
#                     surnames = request.form.get('apellido')
#                     mail = request.form.get('email')
#                     phone = request.form.get('telefono')
#                     # password = request.form.get('password')
#
#                     # Hashear contraseña
#                     # metodo_cript = hashlib.sha256()
#                     # metodo_cript.update(password.encode())
#                     # hashed_password = metodo_cript.hexdigest()
#
#                     # Actualizar datos en la base de datos
#                     query_update = """
#                         UPDATE clientes
#                         SET name = %s, surnames = %s, mail = %s, phone = %s
#                         WHERE id = %s
#                     """
#                     cursor.execute(query_update, (name, surnames, mail, phone, user_id))
#                     db.conn.commit()
#                     flash("Tu perfil ha sido actualizado exitosamente.", "success")
#
#                 # Consultar datos del usuario
#                 query_select = "SELECT name, surnames, mail, phone FROM clientes WHERE id = %s"
#                 cursor.execute(query_select, (user_id,))
#                 user_data = cursor.fetchone()
#
#                 if not user_data:
#                     flash("No se encontraron datos para este usuario.", "danger")
#                     return redirect(url_for('login.login'))
#     except Exception as ex:
#         flash(f"Error al procesar la solicitud: {ex}", "danger")
#         return redirect(url_for('home.home'))
#     finally:
#         if db and db.conn:
#             db.close_connection()
#
#     return render_template('profile.html', user=user_data)