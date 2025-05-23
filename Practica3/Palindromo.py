from unicodedata import normalize

trans_tab = dict.fromkeys(map(ord, u'\u0301\u0308'), None)

while True:
    try:
        string = (input("\n- Ingresa un string y determinaré si es un palíndromo o no.\n>>> ").replace(" ", "")).lower()
        if not string:
            raise ValueError
    except ValueError:
        print("- Error: Favor de ingresar un string válido.")
    else:
        string = normalize('NFKC', normalize('NFKD', string).translate(trans_tab))
        resultado = string[::-1] == string
        print("- Es un palíndromo.") if resultado else print("- No es un palíndromo.")