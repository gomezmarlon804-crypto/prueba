import menu
from limpiar_pantalla import limpiar_pantalla
from mostrar_rutas_usuario import mostrar_rutas_usuario


def buscar_rutas_usuario():
    limpiar_pantalla()
    if not menu.rutas:
        print("\nTodavía no hay rutas disponibles para buscar.")
        return

    while True:
        consulta = input(
            "\nIngrese el destino, origen o nombre de una parada: "
        ).strip().casefold()
        if consulta:
            break
        print("La búsqueda no puede estar vacía.")

    resultados = [
        ruta
        for ruta in menu.rutas
        if consulta in ruta["origen"].casefold()
        or consulta in ruta["destino"].casefold()
        or any(consulta in parada["nombre"].casefold() for parada in ruta["paradas"])
    ]

    if resultados:
        mostrar_rutas_usuario(resultados)
    else:
        print(f"No se encontraron rutas para '{consulta}'.")
