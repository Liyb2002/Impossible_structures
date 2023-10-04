from flask import Flask, request
from flask_cors import CORS

from impossible.main import run, scale_complexity

app = Flask(__name__)
CORS(app)


@app.post("/")
def hello_world():
    try:
        complexity = scale_complexity(
            int(request.json["complexity"]), request.json["scene"]
        )
    except ValueError:
        return {"Error": "invalid complexity parameter"}

    if request.json["scene"] == "za":
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
