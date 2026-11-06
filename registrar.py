from almacenamiento import guardar_usuarios
from buscar_usuario import buscar_usuario
from limpiar_pantalla import limpiar_pantalla
from pedir_credenciales import pedir_credenciales
from seguridad import proteger_clave
from usuarios_data import usuarios


def registrar(rol):
    limpiar_pantalla()
    print(f"\n--- Registro de {'Administrador' if rol == 'admin' else 'Usuario'} ---")
    nombre, clave = pedir_credenciales(
        f"Ingrese nombre de {'administrador' if rol == 'admin' else 'usuario'}: ",
        "Ingrese su contraseña: "
    )

    if buscar_usuario(nombre) is not None:
        print(f"Error: el nombre '{nombre}' ya está en uso. Elija otro.")
        while True:
            opcion = input(
                "¿Desea iniciar sesión con esta cuenta? (1: Sí, 2: No): "
            ).strip()
            if opcion == "1":
                return "__login__"
            if opcion == "2":
                return None
            print("Opción inválida. Seleccione 1 o 2.")

    print("\nPregunta de seguridad para recuperar la contraseña:")
    print("1. ¿Cómo se llama tu mascota?")
    print("2. ¿Cuál es tu ciudad de nacimiento?")
    print("3. ¿Cuál es tu comida favorita?")
    preguntas = {
        "1": "¿Cómo se llama tu mascota?",
        "2": "¿Cuál es tu ciudad de nacimiento?",
        "3": "¿Cuál es tu comida favorita?",
    }
    while True:
        opcion = input("Seleccione una pregunta (1-3): ").strip()
        if opcion in preguntas:
            break
        print("La pregunta de seguridad seleccionada no es válida.")

    while True:
        respuesta = input("Ingrese la respuesta de seguridad: ").strip()
        if respuesta:
            break
        print("Error: la respuesta de seguridad no puede estar vacía.")

    usuarios.append(
        {
            "nombre": nombre,
            "clave": proteger_clave(clave),
            "rol": rol,
            "pregunta": preguntas[opcion],
            "respuesta": proteger_clave(respuesta.casefold()),
        }
    )
    guardar_usuarios(usuarios)
    print(
        f"¡{'Administrador' if rol == 'admin' else 'Usuario'} '{nombre}' registrado con éxito!"
    )
    input("Presione Enter para continuar...")
    return nombre
