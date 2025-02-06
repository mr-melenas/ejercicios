from flask import Flask
from flask_pymongo import PyMongo

app = Flask(__name__)

# Configurar la conexión con MongoDB
app.config["MONGO_URI"] = "mongodb+srv://mbeltranestudio:tAucnxsq2Qc822DS@clusteradan.amk0r.mongodb.net/"

mongo = PyMongo(app) # Conectar a la base de datos

@app.route('/')
def index():
    return "Bienvenido al Taxímetro"

if __name__ == '__main__':
    app.run(debug=True)
