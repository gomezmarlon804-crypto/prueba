from buscar_usuario import buscar_usuario
from limpiar_pantalla import limpiar_pantalla
from pedir_credenciales import _leer_clave
from seguridad import proteger_clave, verificar_clave


def recuperar_cuenta(rol):
    limpiar_pantalla()
    print("\n--- Recuperación de contraseña ---")
    while True:
        nombre = input(
            f"Ingrese el nombre de la cuenta {rol} (0 para cancelar): "
        ).strip()
        if nombre == "0":
            return False
        if not nombre:
            print("El nombre no puede estar vacío.")
            continue
        usuario = buscar_usuario(nombre, rol=rol)
        if usuario is not None:
            break
        print("No existe una cuenta con ese nombre y rol.")
    if "pregunta" not in usuario or "respuesta" not in usuario:
        print("Esta cuenta no tiene configurada una pregunta de seguridad.")
        input("Presione Enter para volver...")
        return False

    print(f"\nPregunta de seguridad: {usuario['pregunta']}")
    while True:
        respuesta = input("Respuesta: ").strip()
        if respuesta and verificar_clave(respuesta.casefold(), usuario["respuesta"]):
            break
        print("La respuesta de seguridad es incorrecta.")

    while True:
        nueva_clave = _leer_clave("Ingrese la nueva contraseña: ").strip()
        confirmar_clave = _leer_clave("Confirme la nueva contraseña: ").strip()

        if not nueva_clave:
            print("La nueva contraseña no puede estar vacía.")
            continue
        if nueva_clave != confirmar_clave:
            print("Las contraseñas no coinciden.")
            continue
        break

    usuario["clave"] = proteger_clave(nueva_clave)
    print("La contraseña fue recuperada correctamente.")
    input("Presione Enter para continuar...")
    return True
