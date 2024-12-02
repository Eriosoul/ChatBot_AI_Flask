import secrets
from flask import Flask, render_template, request, jsonify, flash, redirect, url_for
from routes.login import login_bp
from routes.register import register_bp
# from chatbot import get_response, predict_class, intents_json


app = Flask(__name__)

app.secret_key = secrets.token_hex(16)
print(app.secret_key)

app.register_blueprint(login_bp)
app.register_blueprint(register_bp)

@app.get("/home")
def home():
    return render_template('base.html')

if __name__ == '__main__':
    host = '127.0.0.1'
    port = 5000
    print(f"Running on http://{host}:{port}/login")  # Imprime la ruta completa al login
    app.run(host=host, port=port)
