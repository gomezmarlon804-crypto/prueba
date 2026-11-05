from login_admin import login_admin
from limpiar_pantalla import limpiar_pantalla
from login_usuario import login_usuario
from menu_usuario import menu_usuario
from registrar import registrar


def main():
    while True:
        limpiar_pantalla()
        print("=" * 50)
        print("       Bienvenido a MoviBus")
        print("=" * 50)
        print("\n--------- ¿Registrarse como? ---------")
        print("1. Administrador")
        print("2. Usuario")
        print("3. Salir")

        try:
            opcion = int(input("Seleccione una opción: "))
        except ValueError:
            print("Error: Debe ingresar un número entero válido.")
            input("Presione Enter para continuar...")
            continue

        if opcion == 1:
            nombre_registrado = registrar("admin")
            if nombre_registrado:
                login_admin()
                continue

        elif opcion == 2:
            nombre_registrado = registrar("usuario")
            if nombre_registrado:
                login_usuario()
                continue

        elif opcion == 3:
            limpiar_pantalla()
            print("\n¡Gracias por usar MoviBus! Saliendo del sistema...")
            break
        else:
            print("Opción no válida. Intente de nuevo.")
            input("Presione Enter para continuar...")
