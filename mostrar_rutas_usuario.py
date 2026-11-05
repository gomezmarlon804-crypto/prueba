from mostrar_ruta_usuario import mostrar_ruta_usuario


def mostrar_rutas_usuario(rutas):
    if not rutas:
        print("\nTodavía no hay rutas disponibles.")
        return

    print(f"\nSe encontraron {len(rutas)} ruta(s):")
    for numero, ruta in enumerate(rutas, start=1):
        print(f"\n--- Ruta {numero} ---")
        mostrar_ruta_usuario(ruta)
