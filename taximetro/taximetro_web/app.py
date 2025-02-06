from flask import Flask, render_template, request, redirect, url_for ,session, flash
from flask_pymongo import PyMongo
from flask_bcrypt import Bcrypt
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'secreto_super_seguro'  # Clave para manejar sesiones


# Conectar a MongoDB Atlas
app.config["MONGO_URI"] = "mongodb+srv://mbeltranestudio:tAucnxsq2Qc822DS@clusteradan.amk0r.mongodb.net/"
mongo = PyMongo(app)
bcrypt = Bcrypt(app)

#----------------------------------------------------------------------------------------------------------------------------
# Página de login
#----------------------------------------------------------------------------------------------------------------------------
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        usuario = mongo.db.usuarios.find_one({'username': username})

        if usuario and bcrypt.check_password_hash(usuario['password'], password):
            session['usuario'] = username
            flash('¡Inicio de sesión exitoso!', 'success')
            return redirect(url_for('index'))
        else:
            flash('Usuario o contraseña incorrectos.', 'danger')

    return render_template('login.html')

# Cerrar sesión
@app.route('/logout')
def logout():
    session.pop('usuario', None)
    flash('Sesión cerrada.', 'info')
    return redirect(url_for('login'))


#----------------------------------------------------------------------------------------------------------------------------
# Página principal
#----------------------------------------------------------------------------------------------------------------------------
# Página principal (requiere login)
@app.route('/')
def index():
    if 'usuario' not in session:
        return redirect(url_for('login'))
    return render_template('index.html', usuario=session['usuario'])

# Ruta para ver los recorridos
@app.route('/recorridos')
def mostrar_recorridos():
    if 'usuario' not in session:
        return redirect(url_for('login'))
    recorridos = mongo.db.recorridos.find({'conductor': session['usuario']})
    return render_template('recorridos.html', recorridos=recorridos)

# Ruta para guardar un recorrido
@app.route('/guardar_recorrido', methods=['POST'])
def guardar_recorrido():
    if 'usuario' not in session:
        return redirect(url_for('login'))

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
    flash('¡Recorrido guardado con éxito!', 'success')
    return redirect(url_for('mostrar_recorridos'))

if __name__ == '__main__':
    app.run(debug=True)

