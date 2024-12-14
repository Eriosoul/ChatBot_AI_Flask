from flask import Blueprint, render_template

error_bp = Blueprint('errors', __name__)

@error_bp.route('/generic-error')
def generic_error():
    return render_template('error.html', error="Ha ocurrido un error inesperado.")

@error_bp.app_errorhandler(500)
def internal_server_error(error):
    return render_template('error.html', error="Ha ocurrido un error interno del servidor."), 500

@error_bp.app_errorhandler(404)
def not_found_error(error):
    return render_template('error.html', error="Página no encontrada."), 404