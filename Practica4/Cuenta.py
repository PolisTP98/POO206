from unicodedata import normalize

formato = dict.fromkeys(map(ord, u'\u0301\u0308'), None)

def contar(frase, letra):
    print(f"\n- La letra '{letra}' aparece {frase.count(letra)} veces en la frase: {frase}.")

while True:
    try:
        frase = normalize('NFKC', normalize('NFKD', input("\n- Ingresa una palabra.\n>>> ").lower()).translate(formato))
        letra = normalize('NFKC', normalize('NFKD', input("  Ingresa una letra y contaré las veces que aparece en la frase.\n>>> ").lower()).translate(formato))
        if not frase or not letra or len(letra) > 1:
            raise ValueError
    except ValueError:
        print("- Error: Favor de ingresar el/los dato(s) solicitado(s).")
    else:
        contar(frase, letra)