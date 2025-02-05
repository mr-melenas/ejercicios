import time

def conducir():
    print("Conduciendo...")
    time.sleep(2)  # Simula el tiempo de conducción
    return time.time() - temporizador1

def cobrar(tiempo_taximetro, tiempo_conduccion):
    print(f"Tiempo total del taxímetro: {tiempo_taximetro:.2f} segundos")
    print(f"Tiempo de conducción: {tiempo_conduccion:.2f} segundos")
    print("Cobro realizado.")

print("Bienvenido al taxímetro")

while True:
    options = input("Desea iniciar el taxímetro? S/N: ")
    if options in ["N", "n"]:
        print("El taxímetro no se ha iniciado")
        print("Bye Bye")
        break
    elif options in ["S", "s"]:
        print("Iniciando taxímetro")
        temporizador1 = time.time()
        tiempo_conduccion = conducir()
        temporizador2 = time.time()
        tiempo_taximetro = temporizador2 - temporizador1
        print("Taxímetro finalizado")
        cobrar(tiempo_taximetro, tiempo_conduccion)
    else:
        print("Por favor, elija entre S o N")
