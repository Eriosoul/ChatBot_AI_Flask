import secrets
from flask import Flask
from routes.login import login_bp
from routes.register import register_bp
from routes.home import home_bp
from routes.error_handlers import error_bp
# from chatbot import get_response, predict_class, intents_json


app = Flask(__name__)

app.secret_key = secrets.token_hex(16)
print(app.secret_key)

app.register_blueprint(login_bp)
app.register_blueprint(register_bp)
app.register_blueprint(home_bp)
# Registra el Blueprint de errores
app.register_blueprint(error_bp)

if __name__ == '__main__':
    host = '127.0.0.1'
    port = 5000
    print(f"Running on http://{host}:{port}/login")  # Imprime la ruta completa al login
    app.run(host=host, port=port)
