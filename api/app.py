from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

@app.route('/')
def home():
    return "Hello, this is the Line Bot with Flask and ChatGPT!"

if __name__ == '__main__':
    app.run(debug=True)
