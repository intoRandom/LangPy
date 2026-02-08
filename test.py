def calcular_promedio(numeros):
    total = 0
    for num in numeros:
        total = total + num
    return total / len(numeros)

datos = [10, 20, 30, 40]
print("Promedio:", calcular_promedio(datos))
