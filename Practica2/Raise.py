def calcular_media(numeros):
    if not numeros:
        raise ValueError("\nLa lista de números no puede estar vacía.")
    return sum(numeros) / len(numeros)

try:
    v = [1, 2, 3, 4, 5] #Aquí se colocan los números
    media = calcular_media(v)
    print(f"\nLa media es {media:.2f}")
except ValueError as e:
    print(f"\nError de cálculo: {e}")