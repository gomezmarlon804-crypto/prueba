from buscar_usuario import buscar_usuario
from limpiar_pantalla import limpiar_pantalla
from pedir_credenciales import _leer_clave
from seguridad import proteger_clave, verificar_clave


def recuperar_cuenta(rol):
    limpiar_pantalla()
    print("\n--- Recuperación de contraseña ---")
    nombre = input(f"Ingrese el nombre de la cuenta {rol}: ").strip()
    usuario = buscar_usuario(nombre, rol=rol)

    if usuario is None:
        print("No existe una cuenta con ese nombre y rol.")
        input("Presione Enter para volver...")
        return False
    if "pregunta" not in usuario or "respuesta" not in usuario:
        print("Esta cuenta no tiene configurada una pregunta de seguridad.")
        input("Presione Enter para volver...")
        return False

    print(f"\nPregunta de seguridad: {usuario['pregunta']}")
    respuesta = input("Respuesta: ").strip()
    if not verificar_clave(respuesta.casefold(), usuario["respuesta"]):
        print("La respuesta de seguridad es incorrecta.")
        input("Presione Enter para volver...")
        return False

    nueva_clave = _leer_clave("Ingrese la nueva contraseña: ").strip()
    confirmar_clave = _leer_clave("Confirme la nueva contraseña: ").strip()
    if not nueva_clave or nueva_clave != confirmar_clave:
        print("Las contraseñas están vacías o no coinciden.")
        input("Presione Enter para volver...")
        return False

    usuario["clave"] = proteger_clave(nueva_clave)
    print("La contraseña fue recuperada correctamente.")
    input("Presione Enter para continuar...")
    return True
