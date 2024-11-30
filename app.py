from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

@app.route("/chat")
def home():
    return render_template('base.html')

if __name__ == '__main__':
    app.run(debug=True)
