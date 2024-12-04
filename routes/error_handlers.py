from flask import Blueprint, render_template

error_bp = Blueprint('errors', __name__)

# Manejo de errores genéricos
@error_bp.app_errorhandler(Exception)
def handle_generic_error(error):
    error_message = str(error)
    print(f"Error: {error_message}")  # Puedes reemplazar con un logger para registrar en un archivo
    return render_template('error.html', message="Ocurrió un error inesperado."), 500

# Manejo de errores específicos de MySQL
@error_bp.app_errorhandler(Exception)
def handle_mysql_error(error):
    if "Can't connect to MySQL server" in str(error):
        return render_template('error.html', message="Error al conectar con la base de datos. Por favor, inténtalo más tarde."), 500
    return handle_generic_error(error)