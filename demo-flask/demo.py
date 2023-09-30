from flask import Flask, request
from flask_cors import CORS

from impossible.main import run

app = Flask(__name__)
CORS(app)


@app.post("/")
def hello_world():
    try:
        complexity = int(request.json["complexity"])
    except ValueError:
        return {"Error": "the complexity parameter should be an integer"}

    return run(
        "impossible/ZA_Extended/ZA_monumentValley.json",
        "impossible/ZA_Extended/ZA_monumentValley_decorate.json",
        complexity,
    )
