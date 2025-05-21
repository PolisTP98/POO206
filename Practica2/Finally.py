def Despedida(nombre):
    print(f"\n¡Nos vemos luego {nombre}!")

try:
    numero = int(input("\nIntroduce un número entero: "))
    resultado = 10 / numero
except (ValueError, ZeroDivisionError) as e:
    print(f"\nSe produjo un error: {e}")
else:
    print(f"\nResultado: {resultado}")
finally:
    nombre = input("\nIngresa tu primer nombre: ")
    Despedida(nombre)