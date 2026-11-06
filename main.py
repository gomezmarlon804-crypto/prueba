import sys
from almacenamiento import cargar_datos
from buscar_usuario import buscar_usuario
from limpiar_pantalla import limpiar_pantalla
import menu
from menu_usuario import menu_usuario
from pedir_credenciales import pedir_credenciales
from recuperar_cuenta import recuperar_cuenta
from registrar import registrar
from seguridad import verificar_clave


def redirigir_usuario(usuario):
    """Redirige al menú correspondiente según el rol del usuario."""
    rol = usuario.get("rol", "").lower()
    if rol == "admin":
        menu.main()
    else:
        menu_usuario(usuario)


def iniciar_sesion():
    """Flujo unificado de inicio de sesión: solicita credenciales una sola vez."""
    limpiar_pantalla()
    print("=" * 50)
    print("                Iniciar Sesión")
    print("=" * 50)
    nombre, clave = pedir_credenciales("Ingrese su usuario: ", "Ingrese su contraseña: ")
    usuario = buscar_usuario(nombre)

    if usuario is None:
        print(f"\nError: El usuario '{nombre}' no está registrado en el sistema.")
        input("Presione Enter para continuar...")
        return

    if verificar_clave(clave, usuario["clave"]):
        limpiar_pantalla()
        rol_texto = "Administrador" if usuario["rol"] == "admin" else "Pasajero"
        print("=" * 50)
        print(f"¡Acceso concedido! Bienvenido/a {usuario['nombre']} ({rol_texto}).")
        print("=" * 50)
        input("Presione Enter para ingresar al sistema...")
        redirigir_usuario(usuario)
    else:
        print("\nError: Contraseña incorrecta.")
        print("1. Intentar de nuevo")
        print("2. Recuperar contraseña")
        print("3. Volver al menú principal")
        opcion = input("Seleccione una opción (1-3): ").strip()
        if opcion == "1":
            iniciar_sesion()
        elif opcion == "2":
            if recuperar_cuenta(usuario["rol"]):
                print("\nContraseña actualizada. Ahora puede iniciar sesión.")
                input("Presione Enter para continuar...")
                iniciar_sesion()


def flujo_registro():
    """Flujo de registro: tras registrarse, inicia sesión automáticamente."""
    limpiar_pantalla()
    print("=" * 50)
    print("             Registro de Nuevo Usuario")
    print("=" * 50)
    print("1. Usuario Pasajero")
    print("2. Administrador")
    print("3. Cancelar y volver")

    opcion = input("\nSeleccione el tipo de cuenta a registrar (1-3): ").strip()
    if opcion == "1":
        rol = "usuario"
    elif opcion == "2":
        rol = "admin"
    elif opcion == "3":
        return
    else:
        print("Opción inválida.")
        input("Presione Enter para continuar...")
        return

    nombre_registrado = registrar(rol)
    if not nombre_registrado:
        return
    if nombre_registrado == "__login__":
        iniciar_sesion()
        return

    # Iniciar sesión directamente sin volver a pedir las credenciales
    usuario_creado = buscar_usuario(nombre_registrado)
    if usuario_creado:
        limpiar_pantalla()
        rol_texto = "Administrador" if usuario_creado["rol"] == "admin" else "Pasajero"
        print("=" * 50)
        print(f"¡Bienvenido/a {usuario_creado['nombre']}!")
        print(f"Sesión iniciada automáticamente con rol de {rol_texto}.")
        print("=" * 50)
        input("Presione Enter para ingresar al sistema...")
        redirigir_usuario(usuario_creado)


def main():
    """Punto de entrada principal del sistema MoviBus."""
    cargar_datos()

    while True:
        try:
            limpiar_pantalla()
            print("=" * 50)
            print("                Bienvenido a MoviBus")
            print("    Sistema Inteligente de Transporte Universitario")
            print("=" * 50)
            print("\n1. Iniciar Sesión")
            print("2. Registrarse")
            print("3. Salir")

            opcion = input("\nSeleccione una opción (1-3): ").strip()

            if opcion == "1":
                iniciar_sesion()
            elif opcion == "2":
                flujo_registro()
            elif opcion == "3":
                limpiar_pantalla()
                print("\n¡Gracias por utilizar MoviBus! Que tenga un buen viaje.")
                break
            else:
                print("Opción no válida. Ingrese 1, 2 o 3.")
                input("Presione Enter para continuar...")

        except KeyboardInterrupt:
            print("\n\nOperación cancelada por el usuario.")
            print("¡Gracias por utilizar MoviBus! Hasta pronto.")
            break


if __name__ == "__main__":
    main()
