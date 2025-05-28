def regresivo(numero):
    for index in range(0, numero + 1):
        print(numero - index, end = ", ") if index < numero else print(numero - index)

while True:
    try:
        numero = int(input("\n- Ingresa un número entero positivo.\n>>> "))
        if numero <= 0:
            raise ValueError
    except ValueError as e:
        print(f"- Error: Favor de ingresar un número entero válido.")
    else:
        regresivo(numero)