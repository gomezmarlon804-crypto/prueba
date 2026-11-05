from buscar_usuario import buscar_usuario
from limpiar_pantalla import limpiar_pantalla
from menu_usuario import menu_usuario
from pedir_credenciales import pedir_credenciales
from recuperar_cuenta import recuperar_cuenta
from seguridad import verificar_clave


def login_usuario():
    while True:
        limpiar_pantalla()
        print("=" * 50)
        print("Inicie sesión como usuario")
        print("=" * 50)
        nombre, clave = pedir_credenciales(
            "Ingrese su usuario: ", "Ingrese su contraseña: "
        )
        usuario = buscar_usuario(nombre, rol="usuario")

        if usuario is None:
            print("El usuario no existe.")
            input("Presione Enter para intentarlo de nuevo...")
            continue

        if verificar_clave(clave, usuario["clave"]):
            print("¡Acceso concedido! Bienvenido al sistema.")
            input("Presione Enter para continuar...")
            menu_usuario()
            return

        print("Contraseña incorrecta.")
        print("1. Intentarlo nuevamente")
        print("2. Recuperar contraseña")
        opcion = input("Seleccione una opción: ").strip()
        if opcion == "2":
            recuperar_cuenta("usuario")
