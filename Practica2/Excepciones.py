try:
    numero = int(input("\nIntroduce un número: "))
    resultado = 10 / numero
    print(f"\nResultado: {resultado}")
except ValueError:
    print("Error: Se ingresó algo que no es un número entero.")
except ZeroDivisionError:
    print("Error: Estás intentando dividir entre cero.")