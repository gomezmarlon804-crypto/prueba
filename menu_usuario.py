import menu
from almacenamiento import guardar_rutas
from buscar_rutas_usuario import buscar_rutas_usuario
from entradas import leer_entero, leer_si_no
from limpiar_pantalla import limpiar_pantalla
from mostrar_rutas_usuario import mostrar_rutas_usuario


def obtener_capacidad_vehiculo(placa):
    """Obtiene la capacidad configurada para el vehículo con la placa indicada."""
    for vehiculo in menu.vehiculos:
        if vehiculo["placa"] == placa:
            return vehiculo["capacidad"]
    return 40


def reservar_pasaje(usuario=None):
    """Permite al usuario comprar o reservar pasajes controlando la capacidad del bus."""
    limpiar_pantalla()
    print("\n======== Comprar / Reservar Pasaje ========")
    if not menu.rutas:
        print("No hay rutas disponibles para reservar.")
        return

    print("Rutas disponibles:")
    for index, ruta in enumerate(menu.rutas, start=1):
        capacidad = obtener_capacidad_vehiculo(ruta["vehiculo"])
        ocupados = ruta.get("asientos_ocupados", 0)
        disponibles = max(0, capacidad - ocupados)
        estado = f"Quedan {disponibles} de {capacidad} asientos"
        if disponibles == 0:
            estado += " (AGOTADO)"
        print(
            f"{index}. {ruta['origen']} -> {ruta['destino']} "
            f"| Salida: {ruta['hora_salida']} | Vehículo: {ruta['vehiculo']} "
            f"| {estado}"
        )

    print("0. Cancelar")
    opcion = leer_entero("\nSeleccione el número de ruta a reservar (0 para cancelar): ", 0, len(menu.rutas))
    if opcion == 0:
        print("Operación cancelada.")
        return

    ruta_sel = menu.rutas[opcion - 1]
    capacidad = obtener_capacidad_vehiculo(ruta_sel["vehiculo"])
    ocupados = ruta_sel.get("asientos_ocupados", 0)
    disponibles = max(0, capacidad - ocupados)

    print(f"\nRuta seleccionada: {ruta_sel['origen']} -> {ruta_sel['destino']}")
    print(f"Disponibilidad actual: Quedan {disponibles} de {capacidad} asientos")

    if disponibles <= 0:
        print("No es posible reservar: la ruta no cuenta con asientos disponibles (Agotado).")
        return

    cantidad = leer_entero(
        f"¿Cuántos asientos desea comprar/reservar? (1-{disponibles}, 0 para cancelar): ",
        0,
    )
    if cantidad == 0:
        print("Operación cancelada.")
        return

    if cantidad > disponibles:
        print(f"Error: No hay suficiente cupo. Solo quedan {disponibles} de {capacidad} asientos.")
        return

    confirmacion = leer_si_no(f"¿Confirma la compra/reserva de {cantidad} pasaje(s)? (s/n): ")
    if confirmacion == "s":
        ruta_sel["asientos_ocupados"] = ocupados + cantidad
        guardar_rutas(menu.rutas)
        quedan = capacidad - ruta_sel["asientos_ocupados"]
        print("\n¡Reserva confirmada con éxito!")
        print(f"Pasajes reservados: {cantidad}")
        print(f"Ruta: {ruta_sel['origen']} -> {ruta_sel['destino']}")
        print(f"Vehículo: {ruta_sel['vehiculo']}")
        print(f"Hora de salida: {ruta_sel['hora_salida']}")
        print(f"Disponibilidad actualizada: Quedan {quedan} de {capacidad} asientos")
    else:
        print("Reserva cancelada.")


def menu_usuario(usuario=None):
    while True:
        limpiar_pantalla()
        nombre_display = f" - Pasajero: {usuario['nombre']}" if usuario else ""
        print(f"\n======== Menú de Usuario / Pasajero{nombre_display} ========")
        print("1. Ver todas las rutas")
        print("2. Buscar por destino o parada")
        print("3. Comprar / Reservar pasaje")
        print("4. Salir")

        opcion = input("Seleccione una opción (1-4): ").strip()
        if opcion == "1":
            mostrar_rutas_usuario(menu.rutas)
            input("Presione Enter para volver al menú...")
        elif opcion == "2":
            buscar_rutas_usuario()
            input("Presione Enter para volver al menú...")
        elif opcion == "3":
            reservar_pasaje(usuario)
            input("Presione Enter para volver al menú...")
        elif opcion == "4":
            limpiar_pantalla()
            print("Saliendo del menú de usuario...")
            return
        else:
            print("Opción no válida. Seleccione 1, 2, 3 o 4.")
            input("Presione Enter para continuar...")
