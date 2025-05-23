while True:
    try:
        numero = int(input("\n- Ingresa un número y determinaré si es par o impar (Ingresa '0' para finalizar el programa).\n>>> "))
        if numero == 0:
            break
        elif numero < 0:
            raise ValueError
    except ValueError as e:
        print(f"- Error: Favor de ingresar un número entero válido.")
    else:
        resultado = numero % 2 == 0
        print("- Es par.") if resultado else print("- Es impar.")
print("\n- ¡Nos vemos pronto!.")