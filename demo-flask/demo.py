from flask import Flask, request
from flask_cors import CORS

from impossible.main import run

app = Flask(__name__)
CORS(app)


@app.post("/")
def hello_world():
    return run(request.json)
