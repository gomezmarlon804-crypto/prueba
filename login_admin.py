import menu
from buscar_usuario import buscar_usuario
from limpiar_pantalla import limpiar_pantalla
from pedir_credenciales import pedir_credenciales
from recuperar_cuenta import recuperar_cuenta
from seguridad import verificar_clave


def login_admin():
    while True:
        limpiar_pantalla()
        print("=" * 50)
        print("Verifique su usuario y contraseña para ingresar al sistema")
        print("=" * 50)
        nombre, clave = pedir_credenciales(
            "Confirme su usuario administrador: ", "Confirme su contraseña: "
        )
        admin = buscar_usuario(nombre, rol="admin")

        if admin is None:
            print("El usuario administrador no existe.")
            input("Presione Enter para intentarlo de nuevo...")
            continue

        if verificar_clave(clave, admin["clave"]):
            print("¡Acceso concedido! Bienvenido al sistema.")
            print("=" * 50)
            input("Presione Enter para continuar...")
            menu.main()
            return
        else:
            print("Contraseña incorrecta.")
            print("1. Intentarlo nuevamente")
            print("2. Recuperar contraseña")
            while True:
                opcion = input("Seleccione una opción: ").strip()
                if opcion == "1":
                    break
                if opcion == "2":
                    if recuperar_cuenta("admin"):
                        break
                    continue
                print("Opción inválida. Seleccione 1 o 2.")
