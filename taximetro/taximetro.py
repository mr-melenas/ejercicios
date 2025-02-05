import time
import keyboard
from pymongo import MongoClient
from datetime import datetime


# Conectar a MongoDB
def conectarBD():
    MONGO_URI = "mongodb+srv://mbeltranestudio:tAucnxsq2Qc822DS@clusteradan.amk0r.mongodb.net/"

    # Conectar a la base de datos
    client = MongoClient(MONGO_URI)

    # Seleccionar la base de datos
    db = client["Taximetro"]  # selecciono la BD 
    recorridos = db["recorridos"]
    # Verificar conexión
    # try:
    #     print("Conectado a MongoDB correctamente ✅")
    #     print("Bases de datos disponibles:", client.list_database_names())  # Lista bases de datos
    # except Exception as e:
    #     print("Error al conectar con MongoDB ❌", e)

    return db 

#Funcion para conducir   
def conducir():
    tiempos_inicio = {}
    tiempo_total = 0.0
    tiempo_conduccion = 0.0

    print("Presiona 'Esc' para salir.") #("Presione 'Q' para finalizar el taximetro?: ")

    while True:
        evento = keyboard.read_event()
        
        if evento.event_type == "down" and evento.name.isdigit(): # Detecta que se ha presioando los números 0-9
            numero = evento.name # Almacena el número presionado  
            if numero not in tiempos_inicio: #Registra solo una vez cada numero, 
                tiempos_inicio[numero] = time.time() #lo añade con el valor del tiempo actual

        elif evento.event_type == "up" and evento.name.isdigit():
            numero = evento.name
            if numero in tiempos_inicio:
                tiempo_presionado = time.time() - tiempos_inicio[numero]
                tiempo_total += tiempo_presionado  # Acumula el tiempo total
                #print(f"\nNúmero {numero} presionado por {tiempo_presionado:.2f} segundos")
                del tiempos_inicio[numero]  # Eliminar registro del tiempo de inicio
        
        if keyboard.is_pressed("Esc"):
            #print(f"\nTiempo total presionando números: {tiempo_total:.2f} segundos")
            print("Saliendo...")
            return tiempo_total

def guardar_recorrido(db, conductor, tiempo_total, tiempo_parado, tiempo_movimiento, total_pagar):
    recorridos = db["recorridos"]  # Definir la colección
    fecha_registro = datetime.now() 
    
    recorrido = {
        "conductor": conductor,
        "tiempo_total": tiempo_total,
        "tiempo_parado": tiempo_parado,
        "tiempo_movimiento": tiempo_movimiento,
        "total_pagar": total_pagar,
        "fecha_registro": fecha_registro
    }
    recorridos.insert_one(recorrido)
    print("Recorrido guardado correctamente.")


def cobrar(tiempo_Taximetro, tiempo_conduccion):
    # Calcular tarifa mientras el taxi está parado (2 céntimos por segundo).
    # Calcular tarifa mientras el taxi está en movimiento (5 céntimos por segundo).
    #print(f"el total parado es: {(tiempo_Taximetro-tiempo_conduccion) * 0.02 }") 
    #print(f"el total en movimiento es: { tiempo_conduccion * 0.05 }")  
    total_a_apagar = (tiempo_Taximetro-tiempo_conduccion) * 0.02 + tiempo_conduccion * 0.05
    print(f"el total a pagar es: {total_a_apagar:.2f}€ ") 
    return total_a_apagar
taxi_ascii = r"""
      __________
     |   TAXI   | 
  __/____|_|____\__ 
 |  _          _   `|
'--(o)--------(o)--'
"""
temporizador1 = 0;
finish = "";

conductor=""
tiempo_parado=0.0
tiempo_movimiento=0
tiempo_total=0
total_pagar=""
fecha_registro=""

db = conectarBD()
print("Bienvenido al taximetro")
print(taxi_ascii)
print("Instrucciones:")
print("-Presiones 'S' si desea inciar el taximetro o 'N' para finalizar.")
print("-Conduzca con las teclas numericas del 0 al 9 y precione 'ESC' para finalizar")
print("-Se mostrara el total a cobrar y luego podras elegir si hacer otro trayecto")
print("----------------------------")
while True:
    options= input("Desea iniciar el taximetro? S/N: ")
    if options in ["N", "n"]:
        print("El taximetro no se ha iniciado")
        print("Bye Bye")
        break
    elif options in ["S", "s"]:
        print("Iniciando taximetro")
        temporizador1 = time.time()
        tiempo_movimiento = conducir()
        temporizador2 = time.time()
        tiempo_total = temporizador2 - temporizador1
        print("Taximetro finalizado")
        total_pagar= cobrar(tiempo_total, tiempo_movimiento)

        guardar_recorrido(db,"JAIME",tiempo_total,(tiempo_total-tiempo_movimiento), tiempo_movimiento, total_pagar)

        time.sleep(2)
        #finish= input("Presione 'Q' para finalizar el taximetro?: ")

    else:
        print("Por favor, elija entre S o N")


 