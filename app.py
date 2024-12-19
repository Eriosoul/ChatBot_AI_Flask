import secrets
from flask import Flask
import logging
from routes.login import login_bp
from routes.register import register_bp
from routes.home import home_bp
from routes.auth import auth_bp
from routes.profile import profile_bp
from routes.reservations import reservations_bp
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
app.register_blueprint(reservations_bp)



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


"""
@app.before_request
def load_user():
    user_id = session.get('user_id')
    if user_id:
        # Aquí obtienes el usuario de la base de datos según el ID
        db = DataBaseConnection()
        try:
            with db.conn.cursor(dictionary=True) as cursor:
                cursor.execute(
                    SELECT name, surnames, mail, phone,
                           (SELECT image_url FROM cliente_imagenes
                            WHERE cliente_id = %s
                            ORDER BY uploaded_at DESC LIMIT 1) AS image_url
                    FROM clientes
                    WHERE id = %s
        , (user_id, user_id))

                user = cursor.fetchone()

                if user:
                    # Asegúrate de decodificar el valor de image_url si es tipo bytes
                    if isinstance(user['image_url'], bytes):
                        user['image_url'] = user['image_url'].decode('utf-8')
                        print(user['image_url'])
                    session['user'] = user
        finally:
            if db.conn:
                db.close_connection()

@app.context_processor
def inject_user():
    return dict(user=session.get('user'))
"""