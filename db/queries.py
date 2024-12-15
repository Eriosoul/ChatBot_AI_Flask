from .connection_db import DataBaseConnection
from flask import session

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

