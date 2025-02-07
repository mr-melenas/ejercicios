from flask import Flask, render_template, request, redirect, url_for ,session, flash
from flask_pymongo import PyMongo
from flask_bcrypt import Bcrypt
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'secreto_super_seguro'  # Clave para manejar sesiones


# Conectar a MongoDB Atlas
app.config["MONGO_URI"] = "mongodb+srv://mbeltranestudio:tAucnxsq2Qc822DS@clusteradan.amk0r.mongodb.net/Taximetro"
mongo = PyMongo(app)
bcrypt = Bcrypt(app)


#----------------------------------------------------------------------------------------------------------------------------
# prueba test BD
#----------------------------------------------------------------------------------------------------------------------------
@app.route('/test-connection')
def test_connection():
    try:
        # Intentar acceder a la colección 'conductores'
        mongo.db.conductores.find_one()
        return "✅ Conexión a MongoDB exitosa."
    except Exception as e:
        return f"❌ Error de conexión: {str(e)}"


#----------------------------------------------------------------------------------------------------------------------------
# Página de registro
#----------------------------------------------------------------------------------------------------------------------------
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':

        username = request.form['username'].strip()
        password = bcrypt.generate_password_hash(request.form['password']).decode('utf-8')
        nombre = request.form['nombre'].strip()
        apellido = request.form['apellido'].strip()
        email = request.form['email'].strip()
        telefono = request.form.get('telefono', '').strip()  # Opcional
        matricula = request.form.get('matricula', '').strip()  # Opcional

        # Verificar si el usuario ya existe
        if mongo.db.conductores.find_one({'username': username}):
            flash('El usuario ya existe. Intenta con otro.', 'danger')
            return redirect(url_for('register'))
        
        # Verificar si el email ya existe
        if mongo.db.conductores.find_one({'email': email}):
                flash('El correo electrónico ya está registrado.', 'danger')
                return redirect(url_for('register'))
        
        nuevo_usuario = {
            'username': username,
            'password': password,
            'nombre': nombre,
            'apellido': apellido,
            'email': email,
            'telefono': telefono if telefono else None,
            'matricula': matricula if matricula else None
        }

        # Insertar el nuevo usuario en la colección 'conductores'
        mongo.db.conductores.insert_one(nuevo_usuario)
        flash('¡Registro exitoso! Ahora inicia sesión.', 'success')
        return redirect(url_for('login'))

    return render_template('register.html')



#----------------------------------------------------------------------------------------------------------------------------
# Página de login
#----------------------------------------------------------------------------------------------------------------------------
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        usuario = mongo.db.conductores.find_one({'username': username})

        if usuario and bcrypt.check_password_hash(usuario['password'], password):
            session['usuario'] = username
            flash('¡Inicio de sesión exitoso!', 'success')
            return redirect(url_for('index'))
        else:
            flash('Usuario o contraseña incorrectos.', 'danger')
            return redirect(url_for('login'))  # Redirige para que el mensaje se muestre

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

# Mostrar todas las rutas registradas por Flask
for rule in app.url_map.iter_rules():
    print(rule)

if __name__ == '__main__':
    app.run(debug=True)

