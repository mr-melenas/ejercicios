from flask import Flask, render_template, request, redirect, url_for
from flask_pymongo import PyMongo
from datetime import datetime

app = Flask(__name__)

# Conectar a MongoDB Atlas
app.config["MONGO_URI"] = "mongodb+srv://mbeltranestudio:tAucnxsq2Qc822DS@clusteradan.amk0r.mongodb.net/"
mongo = PyMongo(app)

# Página principal
@app.route('/')
def index():
    return render_template('index.html')

# Ruta para ver los recorridos
@app.route('/recorridos')
def mostrar_recorridos():
    recorridos = mongo.db.recorridos.find()
    return render_template('recorridos.html', recorridos=recorridos)

# Ruta para guardar un recorrido
@app.route('/guardar_recorrido', methods=['POST'])
def guardar_recorrido():
    data = request.form
    nuevo_recorrido = {
        "conductor": data["conductor"],
        "tiempo_total": int(data["tiempo_total"]),
        "tiempo_parado": int(data["tiempo_parado"]),
        "tiempo_movimiento": int(data["tiempo_movimiento"]),
        "total_pagar": float(data["total_pagar"]),
        "fecha_registro": datetime.now()
    }
    mongo.db.recorridos.insert_one(nuevo_recorrido)
    return redirect(url_for('mostrar_recorridos'))

if __name__ == '__main__':
    app.run(debug=True)
