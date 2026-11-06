import menu
from horario import calcular_horarios


def mostrar_ruta_usuario(ruta):
    horarios_paradas, hora_llegada, horarios_regreso, _ = calcular_horarios(ruta)
    vehiculo = next(
        (item for item in menu.vehiculos if item["placa"] == ruta["vehiculo"]),
        None,
    )

    print(f"\nOrigen: {ruta['origen']}")
    print(f"Destino final: {ruta['destino']}")
    print(f"Vehículo asignado: {ruta['vehiculo']}")
    if vehiculo:
        descripcion = " ".join(
            dato for dato in (vehiculo["marca"], vehiculo["modelo"]) if dato
        )
        print(
            f"  {descripcion + ' | ' if descripcion else ''}"
            f"Tipo: {vehiculo['tipo']} "
            f"| Capacidad: {vehiculo['capacidad']} pasajeros"
        )

    capacidad = vehiculo["capacidad"] if vehiculo else ruta.get("capacidad", 40)
    ocupados = ruta.get("asientos_ocupados", ruta.get("pasajeros_actuales", 0))
    disponibles = max(0, capacidad - ocupados)
    print(f"  Disponibilidad: Quedan {disponibles} de {capacidad} asientos")

    print("Recorrido de ida:")
    print(f"  {ruta['hora_salida']} - {ruta['origen']} (salida)")
    for parada, hora_parada in zip(ruta["paradas"], horarios_paradas):
        print(f"  {hora_parada} - {parada['nombre']}")
    print(f"  {hora_llegada} - {ruta['destino']} (llegada)")

    if ruta["regresa"]:
        print("Regreso: por el mismo camino")
        print(f"Tiempo estimado de regreso: {ruta['tiempo_vuelta']} min")
        print(f"Tiempo estimado total: {ruta['tiempo_total_recorrido']} min")
        puntos_regreso = [
            parada["nombre"] for parada in reversed(ruta["paradas"])
        ] + [ruta["origen"]]
        for punto, hora_parada in zip(puntos_regreso, horarios_regreso):
            print(f"  {hora_parada} - {punto}")
    else:
        print("Regreso: no incluido en esta ruta")

    retraso = ruta.get("retraso")
    if retraso:
        print("\nAVISO DE RETRASO")
        print(f"  {retraso['mensaje']}")
        print("  Sugerencias para el pasajero:")
        print("  1. Considere esperar unos minutos antes de dirigirse a la parada.")
        print("  2. Manténgase atento a nuevas actualizaciones del conductor.")
        print("  3. Puede tomar una ruta alterna si tiene una urgencia.")
