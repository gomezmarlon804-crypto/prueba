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
        opcion = input("¿Desea iniciar sesión con esta cuenta? (1: Sí, 2: No): ").strip()
        if opcion == "1":
            return "__login__"
        return None

    print("\nPregunta de seguridad para recuperar la contraseña:")
    print("1. ¿Cómo se llama tu mascota?")
    print("2. ¿Cuál es tu ciudad de nacimiento?")
    print("3. ¿Cuál es tu comida favorita?")
    opcion = input("Seleccione una pregunta (1-3): ").strip()
    preguntas = {
        "1": "¿Cómo se llama tu mascota?",
        "2": "¿Cuál es tu ciudad de nacimiento?",
        "3": "¿Cuál es tu comida favorita?",
    }
    if not opcion:
        opcion = "1"
    if opcion not in preguntas:
        print("La pregunta de seguridad seleccionada no es válida.")
        input("Presione Enter para volver al menú...")
        return None

    respuesta = input("Ingrese la respuesta de seguridad: ").strip()
    if not respuesta:
        respuesta = "sin respuesta registrada"

    usuarios.append(
        {
            "nombre": nombre,
            "clave": proteger_clave(clave),
            "rol": rol,
            "pregunta": preguntas[opcion],
            "respuesta": proteger_clave(respuesta.casefold()),
        }
    )
    print(
        f"¡{'Administrador' if rol == 'admin' else 'Usuario'} '{nombre}' registrado con éxito!"
    )
    input("Presione Enter para continuar...")
    return nombre
