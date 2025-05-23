while True:
    try:
        password = input("\n- Ingresa tu contraseña, debe contener:\n(1) 10 o más caracteres\n(2) Al menos un número\n(3) Al menos un caracter especial\n\n>>> ")
        if not password:
            raise ValueError
    except ValueError:
        print("- Error: Favor de ingresar una contraseña válida.")
    else:
        if password.count(" ") >= 1:
            print("- No debe contener espacios en blanco.")
        elif len(password) < 10:
            print("- Contraseña demasiado corta.")
        elif not any(character.isdigit() for character in password):
            print("- Debe contener al menos un número.")
        elif password.isalnum():
            print("- Debe contener al menos un carácter especial.")
        else:
            print("- Contraseña válida.")
            break