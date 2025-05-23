while True:
    try:
        numero = int(input("\nIngresa un número y determinaré si es par o impar (Ingresa '0' para finalizar el programa)\n>>> "))
        if numero == 0:
            break
    except ValueError as e:
        print(f"\n- Error: {e}.\n  Favor de ingresar un número entero válido.")
    else:
        resultado = numero % 2 == 0
        print("\nEl número es par") if resultado else print("\nEl número es impar")
print("\n¡Nos vemos pronto!")