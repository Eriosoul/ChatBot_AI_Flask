from flask import request, redirect, url_for, session, flash
import os
from werkzeug.utils import secure_filename
from datetime import datetime
from db.connection_db import DataBaseConnection

class QuitSessionWhenLogOut:
    @staticmethod
    def delete_user_sessions():
        user_id = session.get('user_id')  # Utilizar get para evitar errores si no está definido
        if not user_id:
            print("No se encontró user_id en la sesión. No se eliminarán sesiones.")
            return  # Salir si no hay un usuario en sesión

        try:
            database = DataBaseConnection()
            if database.conn:
                query = """DELETE FROM sessions WHERE user_id = %s"""
                print(query)
                with database.conn.cursor() as cursor:
                    cursor.execute(query, (user_id,))
                    database.conn.commit()
                print(f"Sesiones del usuario con ID {user_id} eliminadas.")
        except Exception as ex:
            print(f"Error al eliminar sesiones: {ex}")
        finally:
            if database.conn:
                database.close_connection()

class GetDataToProfile:
    @staticmethod
    def get_info_profile():
        user_id = session.get('user_id')
        if not user_id:
            print("No encontró user_id de la sesión")
            return None
        try:
            database = DataBaseConnection()
            if database.conn:
                query = """SELECT name, surnames, mail, phone,password FROM clientes WHERE id = %s"""
                print(query)
                with database.conn.cursor() as cursor:
                    cursor.execute(query, (user_id,))
                    database.conn.commit()
                print(f"Sesiones del usuario con ID {user_id}.")
        except Exception as ex:
            print(f"Error al identificar el usuario sesiones: {ex}")
        finally:
            if database.conn:
                database.close_connection()


class HotelQueries:
    @staticmethod
    def get_all_hotels():
        try:
            database = DataBaseConnection()
            if database.conn:
                query = "SELECT nombre, descripcion, direccion, ciudad, pais, precio FROM propiedades"
                with database.conn.cursor(dictionary=True) as cursor:  # Asegúrate de usar cursor(dictionary=True)
                    cursor.execute(query)
                    return cursor.fetchall()  # Retorna una lista de diccionarios
        except Exception as ex:
            print(f"Error fetching hotels: {ex}")
            return None
        finally:
            if database.conn:
                database.close_connection()


class HotelReservationQueries:
    @staticmethod
    def get_all_reservations_hotels():
        user_id = session.get('user_id')  # Obtener el ID del usuario desde la sesión
        try:
            database = DataBaseConnection()
            if database.conn:
                # Consulta para combinar reservas con propiedades
                query = """
                    SELECT r.fecha_inicio, r.fecha_fin, r.total, r.estado, r.created_at,
                           p.nombre AS hotel_nombre, p.descripcion AS hotel_descripcion,
                           p.direccion AS hotel_direccion, p.ciudad AS hotel_ciudad, 
                           p.pais AS hotel_pais, p.precio AS hotel_precio
                    FROM reservas r
                    JOIN propiedades p ON r.propiedad_id = p.id
                    WHERE r.cliente_id = %s
                """
                with database.conn.cursor(dictionary=True) as cursor:
                    cursor.execute(query, (user_id,))
                    return cursor.fetchall()  # Devuelve todas las reservas con información del hotel
        except Exception as ex:
            print(f"Error fetching reservation hotels: {ex}")
            return None
        finally:
            if database.conn:
                database.close_connection()



# Define la carpeta de uploads
UPLOAD_FOLDER = 'static/uploads/'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}


# Función para verificar la extensión permitida
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


class ProfilePhoto:
    @staticmethod
    def upload_photo():
        if 'profile_photo' not in request.files:
            flash('No se ha seleccionado ningún archivo', 'danger')
            return redirect(request.url)

        file = request.files['profile_photo']

        # Verifica si el archivo tiene una extensión válida
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file_path = os.path.join(UPLOAD_FOLDER, filename)

            # Guarda el archivo en la carpeta 'uploads'
            file.save(file_path)

            # Obtén el ID de usuario de la sesión
            user_id = session.get('user_id')
            if user_id:
                # Guarda la URL de la imagen en la base de datos
                db = DataBaseConnection()
                try:
                    with db.conn.cursor() as cursor:
                        # Inserta la imagen en la base de datos
                        query = "INSERT INTO cliente_imagenes (cliente_id, image_url, uploaded_at) VALUES (%s, %s, %s)"
                        cursor.execute(query, (user_id, f"uploads/{filename}", datetime.utcnow()))
                        db.conn.commit()
                        flash('Imagen subida correctamente', 'success')
                except Exception as ex:
                    flash(f'Error al guardar la imagen: {ex}', 'danger')
                finally:
                    if db.conn:
                        db.close_connection()

            return redirect(
                url_for('profile.profile_page'))  # Redirige a la página de perfil (ajusta el nombre de la ruta)
