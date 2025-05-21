try:
    numero = int(input("\nIntroduce un número entero: "))
    resultado = 10 / numero
except (ValueError, ZeroDivisionError) as e:
    print(f"\nSe produjo un error: {e}")
else:
    print(f"\nResultado: {resultado}")