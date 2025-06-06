def serieCollatz(numero):
    while numero != 1:
        print(numero, end = ", ")
        if numero % 2 == 0:
            numero //= 2
        else:
            numero *= 3
            numero += 1
    print(numero)

while True:
    try:
        numero = int(input("\n- Ingresa el número entero >= 2 desde el que iniciará la serie de Collatz.\n  >>> "))
        if numero <= 1: raise ValueError
        else: serieCollatz(numero)
    except ValueError:
        print("\n  Valor inválido, favor de ingresar un número entero >= 2.")