from flask import Flask, request
from flask_cors import CORS

from impossible.main import run

app = Flask(__name__)
CORS(app)


@app.post("/")
def hello_world():
    if request.json["scene"] == "za":
        return run(
            "impossible/ZA_Extended/ZA_monumentValley.json",
            "impossible/ZA_Extended/ZA_monumentValley_decorate.json",
        )
    elif request.json["scene"] == "mt":
        return run(
            "impossible/matryoshka/matryoshka.json",
            "impossible/matryoshka/matryoshka_decorate.json",
            "impossible/matryoshka/matryoshka_inner.json",
        )
    elif request.json["scene"] == "tr":
        return run(
            "impossible/tree/tree.json",
            "impossible/tree/tree_decorate.json",
        )
