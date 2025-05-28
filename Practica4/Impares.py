def impares(numero):
    lista = [index for index in range(2, numero + 1) if index % 2 != 0]
    print(lista)

while True:
    try:
        numero = int(input("\nIngresa un número entero positivo mayor a 10.\n>>> "))
        if numero <= 10:
            raise ValueError
    except ValueError as e:
        print(f"- Error: Favor de ingresar un número entero válido.")
    else:
        impares(numero)