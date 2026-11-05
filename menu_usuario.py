import menu
from buscar_rutas_usuario import buscar_rutas_usuario
from limpiar_pantalla import limpiar_pantalla
from mostrar_rutas_usuario import mostrar_rutas_usuario


def menu_usuario():
    while True:
        limpiar_pantalla()
        print("\n======== Consulta de rutas ========")
        print("1. Ver todas las rutas")
        print("2. Buscar por destino o parada")
        print("3. Salir")

        opcion = input("Seleccione una opción (1-3): ").strip()
        if opcion == "1":
            mostrar_rutas_usuario(menu.rutas)
            input("Presione Enter para volver al menú...")
        elif opcion == "2":
            buscar_rutas_usuario()
            input("Presione Enter para volver al menú...")
        elif opcion == "3":
            limpiar_pantalla()
            print("Saliendo de la consulta de rutas.")
            return
        else:
            print("Opción no válida. Seleccione 1, 2 o 3.")
            input("Presione Enter para continuar...")
