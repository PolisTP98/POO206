while True:
    try:
        year = int(input("\n- Ingresa un año y determinaré si es biciesto o no (Ingresa '0' para finalizar el programa).\n>>> "))
        if year == 0:
            break
        elif year < 0:
            raise ValueError
    except ValueError as e:
        print("- Error: Favor de ingresar un año válido.")
    else:
        result = (year % 4 == 0 and year % 100 != 0) or (year % 100 == 0 and year % 400 == 0)
        print("- Es biciesto.") if result else print("- No es biciesto.")
print("\n- ¡Nos vemos pronto!.")