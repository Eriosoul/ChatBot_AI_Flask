import secrets
from flask import Flask

from routes.login import login_bp
from routes.register import register_bp
from routes.home import home_bp
from routes.auth import auth_bp
from routes.profile import profile_bp
from routes.hotels import hotels_bp
from error_handlers import error_bp




app = Flask(__name__, static_folder='static')
app.secret_key = secrets.token_hex(16)

# Registrar Blueprints
app.register_blueprint(login_bp)
app.register_blueprint(register_bp)
app.register_blueprint(home_bp)
app.register_blueprint(error_bp)
app.register_blueprint(auth_bp)
app.register_blueprint(profile_bp)
app.register_blueprint(hotels_bp)

import logging

logging.basicConfig(
    filename='logs/error.log',
    level=logging.ERROR,
    format='%(asctime)s [%(levelname)s] %(message)s'
)

if __name__ == '__main__':
    host = '127.0.0.1'
    port = 5000
    print(f"Running on http://{host}:{port}/login")  # Imprime la ruta completa al login
    app.run(host=host, port=port, debug=True)
