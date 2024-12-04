from flask import Blueprint, render_template

error_bp = Blueprint('errors', __name__)

@error_bp.app_errorhandler(404)
def not_found_error(error):
    return render_template('error.html', message="Página no encontrada."), 404

@error_bp.app_errorhandler(500)
def internal_server_error(error):
    return render_template('error.html', message="Error interno del servidor."), 500

@error_bp.app_errorhandler(Exception)
def generic_error(error):
    return render_template('error.html', message="Ocurrió un error inesperado."), 500