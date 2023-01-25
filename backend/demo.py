from flask import Flask, request
from flask_cors import CORS
from raytracer.generate import generate

app = Flask(__name__)
CORS(app)


@app.post("/")
def hello_world():
    return generate(request.json["layers"], request.json["intersections"])
