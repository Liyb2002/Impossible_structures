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

    if request.json["scene"] == "za":
        complexity = max(complexity, 2)
        return run(
            "impossible/ZA_Extended/ZA_monumentValley.json",
            "impossible/ZA_Extended/ZA_monumentValley_decorate.json",
            complexity,
        )
    elif request.json["scene"] == "mt":
        return run(
            "impossible/matryoshka/matryoshka.json",
            "impossible/matryoshka/matryoshka_decorate.json",
            complexity,
            "impossible/matryoshka/matryoshka_inner.json",
        )
    elif request.json["scene"] == "tr":
        return run(
            "impossible/tree/tree.json",
            "impossible/tree/tree_decorate.json",
            complexity,
        )
