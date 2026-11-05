from usuarios_data import usuarios


def buscar_usuario(nombre, rol=None):
    for usuario in usuarios:
        if usuario["nombre"].casefold() == nombre.casefold() and (
            rol is None or usuario["rol"] == rol
        ):
            return usuario
    return None
