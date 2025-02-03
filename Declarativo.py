#Declarativo: Más conciso, se describe lo que se quiere sin preocuparse por los detalles internos.

#📝 Explicación:
#Sin bucles manuales, usamos una comprensión de listas para decir qué queremos (n > 3).


numeros = [1, 2, 3, 4, 5, 6]
pares = list(filter(lambda x: x % 2 == 0, numeros))

print(pares)  # [2, 4, 6]