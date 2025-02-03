#Imperativo: Describe cómo hacer las cosas, con pasos específicos.

#📝 Explicación:
#Creamos una lista vacía mayores_a_tres.
#Recorremos numeros con un for.
#Si el número es mayor que 3, lo agregamos manualmente a la lista.
#Imprimimos el resultado.

numeros = [1, 2, 3, 4, 5]
mayores_a_tres = []

for numero in numeros:
    if numero > 3:
        mayores_a_tres.append(numero)

print(mayores_a_tres)  # [4, 5]