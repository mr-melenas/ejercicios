from pymongo import MongoClient

# Cadena de conexión a MongoDB Atlas
MONGO_URI = "mongodb+srv://mbeltranestudio:tAucnxsq2Qc822DS@clusteradan.amk0r.mongodb.net/"

# Conectar a la base de datos
client = MongoClient(MONGO_URI)

# Seleccionar la base de datos
db = client["Taximetro"]  # Cambia "taximetro_db" por el nombre que quieras

# Verificar conexión
try:
    print("Conectado a MongoDB correctamente ✅")
    print("Bases de datos disponibles:", client.list_database_names())  # Lista bases de datos
except Exception as e:
    print("Error al conectar con MongoDB ❌", e)
