from flask import Flask, render_template, request, jsonify

from chatbot import get_response, predict_class, intents_json

app = Flask(__name__)

@app.get("/")
def home():
    return render_template('base.html')

@app.post("/predict")
def predict():
    text = request.get_json().get("message")
    intents = predict_class(text)
    response = get_response(intents, intents_json)
    message = {"answer": response}
    return jsonify(message)

if __name__ == '__main__':
    app.run(debug=True)
