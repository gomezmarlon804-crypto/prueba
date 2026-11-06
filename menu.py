from datetime import datetime

from almacenamiento import (
    guardar_conductores,
    guardar_rutas,
    guardar_vehiculos,
)
from entradas import leer_entero, leer_hora, leer_opcion, leer_si_no, leer_texto
from gestion_registros import gestionar_registros
from horario import (
    MAX_MINUTOS_TRAMO,
    calcular_horarios,
    hay_conflicto_horario,
)
from limpiar_pantalla import limpiar_pantalla


conductores = []
vehiculos = []
rutas = []


def mostrar_menu():
    limpiar_pantalla()
    print("\n======== Menu de administración ========")
    print("1. Registrar conductores")
    print("2. Registrar vehículos")
    print("3. Asignar rutas")
    print("4. Generar reportes")
    print("5. Editar o eliminar registros")
    print("6. Reportar retraso de una ruta")
    print("7. Salir")


def reportar_retraso():
    limpiar_pantalla()
    print("\n--- Reporte de retraso ---")

    if not rutas:
        print("No hay rutas asignadas.")
        return

    print("Rutas disponibles:")
    for index, ruta in enumerate(rutas, start=1):
        print(
            f"{index}. {ruta['origen']} -> {ruta['destino']} "
            f"| Conductor: {ruta['conductor']} | Hora: {ruta['hora_salida']}"
        )

    while True:
        ruta_index = leer_entero("Seleccione la ruta: ", 1, len(rutas)) - 1
        if ruta_index in range(len(rutas)):
            break
        if ruta_index not in range(len(rutas)):
            print("Selección de ruta inválida.")
    minutos = leer_entero("¿Cuántos minutos de retraso se esperan?: ", 1, 1440)

    print("\nMotivo:")
    print("1. Tráfico o congestión")
    print("2. Inconveniente mecánico")
    print("3. Condiciones climáticas")
    print("4. Otro")
    motivo_opcion = leer_opcion("Seleccione el motivo: ", ("1", "2", "3", "4"))
    motivos = {
        "1": "Tráfico o congestión",
        "2": "Inconveniente mecánico",
        "3": "Condiciones climáticas",
        "4": "",
    }
    motivo = motivos[motivo_opcion]
    if motivo_opcion == "4":
        motivo = leer_texto("Describa el motivo: ")

    ruta = rutas[ruta_index]
    ruta["retraso"] = {
        "conductor": ruta["conductor"],
        "minutos": minutos,
        "motivo": motivo,
        "mensaje": (
            f"El conductor {ruta['conductor']} informa que la ruta tendrá "
            f"aproximadamente {minutos} minuto(s) de retraso por: {motivo.lower()}."
        ),
    }
    guardar_rutas(rutas)
    print(f"\nAviso registrado para la ruta de {ruta['origen']} a {ruta['destino']}.")
    print(ruta["retraso"]["mensaje"])


def registrar_conductor():
    limpiar_pantalla()
    print("\n--- Registro de conductor ---")

    nombre = leer_texto("Ingrese nombre completo: ")
    while True:
        identificacion = leer_texto("Ingrese identificación: ")
        if any(
            conductor["identificacion"].casefold() == identificacion.casefold()
            for conductor in conductores
        ):
            print(f"La identificación '{identificacion}' ya está registrada.")
            continue
        break
    while True:
        telefono = leer_texto("Ingrese teléfono: ")
        if any(caracter.isdigit() for caracter in telefono):
            break
        print("El teléfono debe contener al menos un número.")

    conductores.append(
        {
            "nombre": nombre,
            "identificacion": identificacion,
            "telefono": telefono,
        }
    )
    guardar_conductores(conductores)
    print(f"Conductor '{nombre}' registrado correctamente.")


def registrar_vehiculo():
    limpiar_pantalla()
    print("\n--- Registro de vehículo ---")

    placa = input("Ingrese la placa del vehículo: ").strip().upper()
    while not placa:
        print("La placa del vehículo no puede estar vacía.")
        placa = input("Ingrese la placa del vehículo: ").strip().upper()
    marca = input("Ingrese la marca (opcional): ").strip()
    modelo = input("Ingrese el modelo (opcional): ").strip()
    anio = input("Ingrese el año (opcional): ").strip()
    tipo = leer_texto("Ingrese el tipo de vehículo: ")
    capacidad = leer_entero("Ingrese la capacidad de pasajeros: ", 1)

    while True:
        if not anio:
            break
        if (
            anio.isdigit()
            and 1886 <= int(anio) <= datetime.now().year + 1
        ):
            break
        print("El año debe ser válido y no puede estar en el futuro.")
        anio = input("Ingrese el año (opcional): ").strip()

    while any(
        vehiculo["placa"].casefold() == placa.casefold()
        for vehiculo in vehiculos
    ):
        print(f"El vehículo con placa '{placa}' ya está registrado.")
        placa = input("Ingrese otra placa: ").strip().upper()

    vehiculos.append(
        {
            "placa": placa,
            "marca": marca,
            "modelo": modelo,
            "anio": anio,
            "tipo": tipo,
            "capacidad": capacidad,
        }
    )
    guardar_vehiculos(vehiculos)
    print(f"Vehículo '{placa}' registrado correctamente.")


def asignar_ruta():
    limpiar_pantalla()
    if not conductores:
        print("Primero debe registrar al menos un conductor.")
        return

    if not vehiculos:
        print("Primero debe registrar al menos un vehículo.")
        return

    print("\nConductores disponibles:")
    for index, conductor in enumerate(conductores, start=1):
        print(f"{index}. {conductor['nombre']} - ID: {conductor['identificacion']}")

    conductor_index = (
        leer_entero("Seleccione el conductor: ", 1, len(conductores)) - 1
    )

    print("\nVehículos disponibles:")
    for index, vehiculo in enumerate(vehiculos, start=1):
        descripcion = " ".join(
            dato for dato in (vehiculo["marca"], vehiculo["modelo"]) if dato
        )
        if not descripcion:
            descripcion = vehiculo["tipo"]
        print(f"{index}. {descripcion} - Placa: {vehiculo['placa']}")

    vehiculo_index = (
        leer_entero("Seleccione el vehículo: ", 1, len(vehiculos)) - 1
    )

    origen = leer_texto("Ingrese el punto de inicio (origen): ")
    destino = leer_texto("Ingrese el destino final: ")
    regreso = leer_si_no(
        "¿La ruta regresa por el mismo camino al punto inicial? (s/n): "
    )
    cantidad_paradas = leer_entero(
        "¿Cuántas paradas habrá del origen al destino? ", 1, 100
    )
    hora_salida = leer_hora(
        "Ingrese la hora de salida (HH:MM, formato 24 horas): "
    )

    paradas = []
    tiempo_total = 0

    print("\nIngrese las paradas y la duración de cada tramo desde el punto anterior:")
    for i in range(1, cantidad_paradas + 1):
        nombre_parada = leer_texto(f"Nombre de la parada {i}: ")
        tiempo_parada = leer_entero(
            f"Duración del tramo hasta '{nombre_parada}' (minutos): ",
            1,
            MAX_MINUTOS_TRAMO,
        )

        paradas.append({"nombre": nombre_parada, "tiempo": tiempo_parada})
        tiempo_total += tiempo_parada

    ultimo_punto = paradas[-1]["nombre"]
    tiempo_destino = leer_entero(
        f"Duración desde '{ultimo_punto}' hasta '{destino}' (minutos): ",
        1,
        MAX_MINUTOS_TRAMO,
    )

    tiempo_total += tiempo_destino
    tiempos_regreso = []
    if regreso == "s":
        print("\nIngrese la duración de cada tramo de regreso (minutos):")
        puntos_ida = [parada["nombre"] for parada in paradas]
        puntos_regreso = list(reversed(puntos_ida)) + [origen]
        origenes_regreso = [destino] + list(reversed(puntos_ida))
        for origen_tramo, destino_tramo in zip(
            origenes_regreso, puntos_regreso
        ):
            tiempo_tramo = leer_entero(
                f"Duración desde '{origen_tramo}' hasta '{destino_tramo}': ",
                1,
                MAX_MINUTOS_TRAMO,
            )
            tiempos_regreso.append(tiempo_tramo)

    tiempo_vuelta = sum(tiempos_regreso)
    tiempo_total_recorrido = tiempo_total + tiempo_vuelta

    ruta = {
        "conductor": conductores[conductor_index]["nombre"],
        "identificacion": conductores[conductor_index]["identificacion"],
        "vehiculo": vehiculos[vehiculo_index]["placa"],
        "origen": origen,
        "destino": destino,
        "hora_salida": hora_salida,
        "regresa": regreso == "s",
        "paradas": paradas,
        "cantidad_paradas": cantidad_paradas,
        "tiempo_destino": tiempo_destino,
        "tiempos_regreso": tiempos_regreso,
        "tiempo_total": tiempo_total,
        "tiempo_vuelta": tiempo_vuelta,
        "tiempo_total_recorrido": tiempo_total_recorrido,
        "asientos_ocupados": 0,
    }

    conflicto = hay_conflicto_horario(ruta, rutas)
    while conflicto:
        ruta_existente, recursos = conflicto
        recursos_texto = " y ".join(recursos)
        horarios_existentes = calcular_horarios(ruta_existente)
        hora_fin = (
            horarios_existentes[3]
            if ruta_existente["regresa"]
            else horarios_existentes[1]
        )
        print(
            f"No se puede asignar: el {recursos_texto} ya tiene una ruta "
            f"superpuesta de {ruta_existente['hora_salida']} a "
            f"{hora_fin}."
        )
        hora_salida = leer_hora(
            "Ingrese otra hora de salida para evitar el conflicto (HH:MM): "
        )
        ruta["hora_salida"] = hora_salida
        conflicto = hay_conflicto_horario(ruta, rutas)

    rutas.append(ruta)
    guardar_rutas(rutas)

    print(f"\nRuta asignada correctamente para {conductores[conductor_index]['nombre']}.")
    print(f"Origen: {origen} | Destino: {destino}")
    print(f"Paradas programadas: {cantidad_paradas}")
    horarios_paradas, hora_llegada, horarios_regreso, hora_regreso = calcular_horarios(ruta)
    print(f"Salida: {hora_salida} | Llegada estimada: {hora_llegada}")
    print(f"Tiempo estimado de ida: {tiempo_total} minutos")
    if regreso == "s":
        print(f"Tiempo estimado de regreso: {tiempo_vuelta} minutos")
        print(f"Tiempo total del recorrido: {tiempo_total_recorrido} minutos")
        print(f"Llegada estimada al origen: {hora_regreso}")
    else:
        print("La ruta no regresa por el mismo camino.")

    print("Detalle de paradas:")
    for index, (parada, hora_parada) in enumerate(
        zip(paradas, horarios_paradas), start=1
    ):
        print(
            f"  {index}. {parada['nombre']} - {parada['tiempo']} min de tramo "
            f"| Llegada: {hora_parada}"
        )
    if regreso == "s":
        print("Detalle de regreso:")
        puntos_regreso = [parada["nombre"] for parada in reversed(paradas)] + [origen]
        for punto, hora_llegada_regreso in zip(puntos_regreso, horarios_regreso):
            print(f"  {hora_llegada_regreso} - {punto}")


def generar_reportes():
    limpiar_pantalla()
    print("\n===== Reportes del sistema =====")
    print(f"Total de conductores: {len(conductores)}")
    print(f"Total de vehículos: {len(vehiculos)}")
    print(f"Total de rutas asignadas: {len(rutas)}")

    if conductores:
        print("\nConductores registrados:")
        for conductor in conductores:
            print(
                f"- Nombre: {conductor['nombre']} | "
                f"ID: {conductor['identificacion']} | "
                f"Teléfono: {conductor['telefono']}"
            )

    if vehiculos:
        print("\nVehículos registrados:")
        for vehiculo in vehiculos:
            detalles = [
                f"Marca: {vehiculo['marca']}" if vehiculo["marca"] else "",
                f"Modelo: {vehiculo['modelo']}" if vehiculo["modelo"] else "",
                f"Año: {vehiculo['anio']}" if vehiculo["anio"] else "",
            ]
            detalles = [detalle for detalle in detalles if detalle]
            print(
                f"- Placa: {vehiculo['placa']} | Tipo: {vehiculo['tipo']} | "
                f"Capacidad: {vehiculo['capacidad']}"
                + (f" | {' | '.join(detalles)}" if detalles else "")
            )

    if rutas:
        print("\nRutas asignadas:")
        for ruta in rutas:
            horarios_paradas, hora_llegada, horarios_regreso, hora_regreso = calcular_horarios(ruta)
            print(
                f"- Conductor: {ruta['conductor']} | ID: {ruta['identificacion']} | "
                f"Vehículo: {ruta['vehiculo']} | Origen: {ruta['origen']} | "
                f"Destino: {ruta['destino']} | Paradas: {ruta['cantidad_paradas']} | "
                f"Salida: {ruta['hora_salida']} | Llegada: {hora_llegada} | "
                f"Tiempo ida: {ruta['tiempo_total']} min | "
                f"Regresa: {'Sí' if ruta['regresa'] else 'No'}"
            )
            print("  Detalle de paradas:")
            for index, (parada, hora_parada) in enumerate(
                zip(ruta["paradas"], horarios_paradas), start=1
            ):
                print(
                    f"    {index}. {parada['nombre']} - {parada['tiempo']} min "
                    f"| Llegada: {hora_parada}"
                )
            if ruta["regresa"]:
                print("  Horarios de regreso:")
                puntos_regreso = [
                    parada["nombre"] for parada in reversed(ruta["paradas"])
                ] + [ruta["origen"]]
                for punto, hora_parada in zip(puntos_regreso, horarios_regreso):
                    print(f"    {hora_parada} - {punto}")
                print(
                    f"  Tiempo total recorrido (ida y regreso): "
                    f"{ruta['tiempo_total_recorrido']} min | "
                    f"Llegada al origen: {hora_regreso}"
                )
    else:
        print("No hay rutas asignadas aún.")


def main():
    while True:
        mostrar_menu()
        try:
            opcion = int(input("Seleccione una opción (1-7): "))
        except ValueError:
            print("Debe ingresar un número válido.")
            input("Presione Enter para continuar...")
            continue

        if opcion == 1:
            registrar_conductor()
            input("Presione Enter para volver al menú...")
        elif opcion == 2:
            registrar_vehiculo()
            input("Presione Enter para volver al menú...")
        elif opcion == 3:
            asignar_ruta()
            input("Presione Enter para volver al menú...")
        elif opcion == 4:
            generar_reportes()
            input("Presione Enter para volver al menú...")
        elif opcion == 5:
            gestionar_registros(conductores, vehiculos, rutas)
        elif opcion == 6:
            reportar_retraso()
            input("Presione Enter para volver al menú...")
        elif opcion == 7:
            limpiar_pantalla()
            print("\nSaliendo del sistema de administración...")
            break
        else:
            print("Opción no válida. Intente nuevamente.")
            input("Presione Enter para continuar...")


if __name__ == "__main__":
    main()