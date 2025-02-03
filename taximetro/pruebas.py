import keyboard
import time

print("Presiona y mantén cualquier número (0-9). Suelta para ver el tiempo individual.")
print("Presiona 'Esc' para ver el tiempo total y salir.")

# Diccionario para almacenar tiempos de inicio
tiempos_inicio = {}
# Variable para almacenar el tiempo total
tiempo_total = 0.0

while True:
    evento = keyboard.read_event()

    if evento.event_type == "down" and evento.name.isdigit():  # Detectar números 0-9
        numero = evento.name
        if numero not in tiempos_inicio:  # Evita registrar varias veces si la tecla sigue presionada
            tiempos_inicio[numero] = time.time()

    elif evento.event_type == "up" and evento.name.isdigit():
        numero = evento.name
        if numero in tiempos_inicio:
            tiempo_presionado = time.time() - tiempos_inicio[numero]
            tiempo_total += tiempo_presionado  # Acumula el tiempo total
            print(f"\nNúmero {numero} presionado por {tiempo_presionado:.2f} segundos")
            del tiempos_inicio[numero]  # Eliminar registro del tiempo de inicio

    # Salir con ESC y mostrar el tiempo total
    if keyboard.is_pressed("esc"):
        print(f"\nTiempo total presionando números: {tiempo_total:.2f} segundos")
        print("Saliendo...")
        break
