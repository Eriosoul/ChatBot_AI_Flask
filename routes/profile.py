import os
from flask import Blueprint, render_template, session, flash, redirect, url_for, request
from db.connection_db import DataBaseConnection

profile_bp = Blueprint('profile', __name__)

# Asegúrate de que la carpeta uploads exista dentro de static/
UPLOAD_FOLDER = os.path.join('static', 'uploads')

def insert_blob(cliente_id, file_path, db):
    """Inserta una imagen en formato binario en la base de datos."""
    try:
        with open(file_path, 'rb') as file:
            binary_data = file.read()

        sql_statement = """
            INSERT INTO cliente_imagenes (cliente_id, image_url, uploaded_at)
            VALUES (%s, %s, NOW())
        """
        with db.conn.cursor() as cursor:
            cursor.execute(sql_statement, (cliente_id, binary_data))
        db.conn.commit()
    except Exception as e:
        db.conn.rollback()
        raise Exception(f"Error al insertar la imagen: {e}")

@profile_bp.route('/profile', methods=['GET', 'POST'])
def profile():
    user_data = None
    user_id = session.get('user_id')

    if not user_id:
        flash("No estás autenticado. Por favor, inicia sesión.", "danger")
        return redirect(url_for('login.login'))

    try:
        db = DataBaseConnection()
        if db.conn:
            with db.conn.cursor(dictionary=True) as cursor:
                if request.method == 'POST':
                    # Datos del formulario
                    name = request.form.get('nombre')
                    surnames = request.form.get('apellido')
                    mail = request.form.get('email')
                    phone = request.form.get('telefono')
                    profile_picture = request.files.get('profile_picture')

                    # Manejo de la imagen
                    if profile_picture and profile_picture.filename != '':
                        # Asegúrate de que la carpeta uploads exista
                        os.makedirs(UPLOAD_FOLDER, exist_ok=True)

                        # Guarda la imagen en el sistema de archivos
                        file_name = f"{user_id}_{profile_picture.filename}"
                        file_path = os.path.join(UPLOAD_FOLDER, file_name)
                        profile_picture.save(file_path)

                        # Guarda solo la ruta en la base de datos (relativa a static/)
                        image_url = f'uploads/{file_name}'

                        # Inserta la ruta de la imagen en la base de datos
                        sql_statement = """
                            INSERT INTO cliente_imagenes (cliente_id, image_url, uploaded_at)
                            VALUES (%s, %s, NOW())
                        """
                        cursor.execute(sql_statement, (user_id, image_url))
                        db.conn.commit()

                    # Actualiza los demás datos del usuario
                    query_update = """
                        UPDATE clientes
                        SET name = %s, surnames = %s, mail = %s, phone = %s
                        WHERE id = %s
                    """
                    cursor.execute(query_update, (name, surnames, mail, phone, user_id))
                    db.conn.commit()
                    flash("Tu perfil ha sido actualizado exitosamente.", "success")

                # Consulta los datos del usuario
                query_select = """
                    SELECT name, surnames, mail, phone,
                    (SELECT image_url FROM cliente_imagenes 
                     WHERE cliente_id = %s 
                     ORDER BY uploaded_at DESC LIMIT 1) AS image_url
                    FROM clientes
                    WHERE id = %s
                """
                cursor.execute(query_select, (user_id, user_id))
                user_data = cursor.fetchone()
                print(user_data)
                if not user_data:
                    flash("No se encontraron datos para este usuario.", "danger")
                    return redirect(url_for('login.login'))

                if user_data:
                    # Convierte la ruta binaria a string si es necesario
                    user_data['image_url'] = user_data['image_url'].decode('utf-8') if isinstance(
                        user_data['image_url'], bytes) else user_data['image_url']
    except Exception as ex:
        flash(f"Error al procesar la solicitud: {ex}", "danger")
        return redirect(url_for('home.home'))
    finally:
        if db and db.conn:
            db.close_connection()

    return render_template('profile.html', user=user_data)
