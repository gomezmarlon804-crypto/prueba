from copy import deepcopy
from datetime import datetime

from entradas import leer_entero, leer_hora, leer_opcion, leer_si_no, leer_texto
from horario import MAX_MINUTOS_TRAMO, hay_conflicto_horario
from limpiar_pantalla import limpiar_pantalla


def _leer_entero_positivo(mensaje):
    return leer_entero(mensaje, 1, MAX_MINUTOS_TRAMO)


def _seleccionar_elemento(elementos, etiqueta):
    if not elementos:
        print(f"No hay {etiqueta} registrados.")
        return None
    for indice, elemento in enumerate(elementos, start=1):
        if etiqueta == "conductores":
            descripcion = f"{elemento['nombre']} - ID: {elemento['identificacion']}"
        elif etiqueta == "vehículos":
            descripcion = f"{elemento['placa']} - {elemento['tipo']}"
        else:
            descripcion = (
                f"{elemento['origen']} -> {elemento['destino']} "
                f"({elemento['hora_salida']})"
            )
        print(f"{indice}. {descripcion}")
    indice = leer_entero(
        "Seleccione un número (0 para cancelar): ", 0, len(elementos)
    )
    if indice == 0:
        return None
    return indice - 1


def _confirmar():
    return input("¿Confirma la eliminación? (s/n): ").strip().casefold() == "s"


def _gestionar_conductores(conductores, rutas):
    indice = _seleccionar_elemento(conductores, "conductores")
    if indice is None:
        return
    conductor = conductores[indice]
    accion = leer_opcion("¿Editar o eliminar? (e/d): ", ("e", "d")).casefold()

    if accion == "d":
        if any(ruta["identificacion"] == conductor["identificacion"] for ruta in rutas):
            print("No se puede eliminar: el conductor tiene rutas asignadas.")
            return
        if _confirmar():
            conductores.pop(indice)
            print("Conductor eliminado.")
        return
    nombre = input(f"Nombre [{conductor['nombre']}]: ").strip()
    while True:
        identificacion = input(
            f"Identificación [{conductor['identificacion']}]: "
        ).strip()
        nueva_identificacion = identificacion or conductor["identificacion"]
        if any(
            otro is not conductor
            and otro["identificacion"].casefold() == nueva_identificacion.casefold()
            for otro in conductores
        ):
            print(f"La identificación '{nueva_identificacion}' ya está registrada.")
            continue
        break
    while True:
        telefono = input(f"Teléfono [{conductor['telefono']}]: ").strip()
        nuevo_telefono = telefono or conductor["telefono"]
        if nuevo_telefono and any(caracter.isdigit() for caracter in nuevo_telefono):
            break
        print("El teléfono debe contener al menos un número.")
    if not (nombre or conductor["nombre"]) or not (
        telefono or conductor["telefono"]
    ):
        print("El nombre y el teléfono son obligatorios.")
        return

    identificacion_anterior = conductor["identificacion"]
    conductor.update(
        {
            "nombre": nombre or conductor["nombre"],
            "identificacion": nueva_identificacion,
            "telefono": nuevo_telefono,
        }
    )
    for ruta in rutas:
        if ruta["identificacion"] == identificacion_anterior:
            ruta["identificacion"] = nueva_identificacion
            ruta["conductor"] = conductor["nombre"]
    print("Conductor actualizado.")


def _gestionar_vehiculos(vehiculos, rutas):
    indice = _seleccionar_elemento(vehiculos, "vehículos")
    if indice is None:
        return
    vehiculo = vehiculos[indice]
    accion = leer_opcion("¿Editar o eliminar? (e/d): ", ("e", "d")).casefold()

    if accion == "d":
        if any(ruta["vehiculo"] == vehiculo["placa"] for ruta in rutas):
            print("No se puede eliminar: el vehículo tiene rutas asignadas.")
            return
        if _confirmar():
            vehiculos.pop(indice)
            print("Vehículo eliminado.")
        return
    while True:
        placa = input(f"Placa [{vehiculo['placa']}]: ").strip().upper()
        nueva_placa = placa or vehiculo["placa"]
        if any(
            otro is not vehiculo
            and otro["placa"].casefold() == nueva_placa.casefold()
            for otro in vehiculos
        ):
            print(f"La placa '{nueva_placa}' ya está registrada.")
            continue
        break
    marca = input(f"Marca [{vehiculo['marca'] or 'vacía'}] (- para borrar): ").strip()
    modelo = input(
        f"Modelo [{vehiculo['modelo'] or 'vacío'}] (- para borrar): "
    ).strip()
    anio = input(f"Año [{vehiculo['anio'] or 'vacío'}] (- para borrar): ").strip()
    tipo = input(f"Tipo [{vehiculo['tipo']}]: ").strip()
    capacidad_texto = input(
        f"Capacidad [{vehiculo['capacidad']}]: "
    ).strip()

    nuevo_tipo = tipo or vehiculo["tipo"]
    nueva_capacidad = vehiculo["capacidad"]
    if capacidad_texto:
        while True:
            try:
                nueva_capacidad = int(capacidad_texto)
                if nueva_capacidad <= 0:
                    raise ValueError
                break
            except ValueError:
                print("La capacidad debe ser un número entero positivo.")
                capacidad_texto = input(
                    f"Capacidad [{vehiculo['capacidad']}]: "
                ).strip()
    nuevo_anio = vehiculo["anio"] if not anio else ("" if anio == "-" else anio)
    if nuevo_anio and (
        not nuevo_anio.isdigit()
        or int(nuevo_anio) < 1886
        or int(nuevo_anio) > datetime.now().year + 1
    ):
        print("El año debe ser válido y no puede estar en el futuro.")
        return
    placa_anterior = vehiculo["placa"]
    vehiculo.update(
        {
            "placa": nueva_placa,
            "marca": (
                vehiculo["marca"]
                if not marca
                else ("" if marca == "-" else marca)
            ),
            "modelo": (
                vehiculo["modelo"]
                if not modelo
                else ("" if modelo == "-" else modelo)
            ),
            "anio": nuevo_anio,
            "tipo": nuevo_tipo,
            "capacidad": nueva_capacidad,
        }
    )
    for ruta in rutas:
        if ruta["vehiculo"] == placa_anterior:
            ruta["vehiculo"] = nueva_placa
    print("Vehículo actualizado.")


def _leer_duracion(mensaje):
    return _leer_entero_positivo(mensaje)


def _editar_tiempos_ida(ruta):
    cantidad = leer_entero("Cantidad de paradas (mínimo 1): ", 1, 100)

    paradas = []
    for indice in range(1, cantidad + 1):
        nombre = leer_texto(f"Nombre de la parada {indice}: ")
        duracion = _leer_duracion(f"Duración hasta '{nombre}' (minutos): ")
        if duracion is None:
            return False
        paradas.append({"nombre": nombre, "tiempo": duracion})
    destino = _leer_duracion(
        f"Duración desde '{paradas[-1]['nombre']}' hasta "
        f"'{ruta['destino']}' (minutos): "
    )
    if destino is None:
        return False
    ruta["paradas"] = paradas
    ruta["cantidad_paradas"] = cantidad
    ruta["tiempo_destino"] = destino
    return True


def _editar_regreso(ruta):
    respuesta = leer_si_no("¿La ruta regresa al origen? (s/n): ")
    if respuesta == "n":
        ruta["regresa"] = False
        ruta["tiempos_regreso"] = []
        return True

    puntos_ida = [parada["nombre"] for parada in ruta["paradas"]]
    puntos_regreso = list(reversed(puntos_ida)) + [ruta["origen"]]
    origenes_regreso = [ruta["destino"]] + list(reversed(puntos_ida))
    tiempos = []
    for desde, hasta in zip(origenes_regreso, puntos_regreso):
        duracion = _leer_duracion(
            f"Duración desde '{desde}' hasta '{hasta}' (minutos): "
        )
        if duracion is None:
            return False
        tiempos.append(duracion)
    ruta["regresa"] = True
    ruta["tiempos_regreso"] = tiempos
    return True


def _recalcular_duracion(ruta):
    ruta["tiempo_total"] = sum(
        parada["tiempo"] for parada in ruta["paradas"]
    ) + ruta["tiempo_destino"]
    ruta["tiempo_vuelta"] = (
        sum(ruta["tiempos_regreso"]) if ruta["regresa"] else 0
    )
    ruta["tiempo_total_recorrido"] = (
        ruta["tiempo_total"] + ruta["tiempo_vuelta"]
    )


def _gestionar_rutas(conductores, vehiculos, rutas):
    indice = _seleccionar_elemento(rutas, "rutas")
    if indice is None:
        return
    ruta = rutas[indice]
    accion = leer_opcion("¿Editar o eliminar? (e/d): ", ("e", "d")).casefold()
    if accion == "d":
        if _confirmar():
            rutas.pop(indice)
            print("Ruta eliminada.")
        return
    candidata = deepcopy(ruta)
    cancelar = False
    while True:
        print("\n1. Cambiar conductor")
        print("2. Cambiar vehículo")
        print("3. Cambiar origen")
        print("4. Cambiar destino")
        print("5. Cambiar hora de salida")
        print("6. Editar paradas y duraciones de ida")
        print("7. Editar regreso")
        print("0. Guardar cambios")
        opcion = input("Seleccione qué desea modificar: ").strip()
        if opcion == "0":
            break
        if opcion == "1":
            seleccionado = _seleccionar_elemento(conductores, "conductores")
            if seleccionado is not None:
                candidata["conductor"] = conductores[seleccionado]["nombre"]
                candidata["identificacion"] = conductores[seleccionado][
                    "identificacion"
                ]
        elif opcion == "2":
            seleccionado = _seleccionar_elemento(vehiculos, "vehículos")
            if seleccionado is not None:
                candidata["vehiculo"] = vehiculos[seleccionado]["placa"]
        elif opcion == "3":
            valor = input(f"Origen [{candidata['origen']}]: ").strip()
            if valor:
                candidata["origen"] = valor
        elif opcion == "4":
            valor = input(f"Destino [{candidata['destino']}]: ").strip()
            if valor:
                candidata["destino"] = valor
        elif opcion == "5":
            valor = input(
                f"Hora de salida [{candidata['hora_salida']}] (HH:MM): "
            ).strip()
            if valor:
                while True:
                    try:
                        candidata["hora_salida"] = datetime.strptime(
                            valor, "%H:%M"
                        ).strftime("%H:%M")
                        break
                    except ValueError:
                        print("Hora inválida. Use el formato HH:MM.")
                        valor = input(
                            f"Hora de salida [{candidata['hora_salida']}] (HH:MM): "
                        ).strip()
        elif opcion == "6":
            if not _editar_tiempos_ida(candidata):
                cancelar = True
                break
            if candidata["regresa"] and not _editar_regreso(candidata):
                cancelar = True
                break
        elif opcion == "7":
            if not _editar_regreso(candidata):
                cancelar = True
                break
        else:
            print("Opción no válida.")

    if cancelar:
        print("No se guardaron los cambios.")
        return

    _recalcular_duracion(candidata)
    otras_rutas = rutas[:indice] + rutas[indice + 1 :]
    conflicto = hay_conflicto_horario(candidata, otras_rutas)
    while conflicto:
        _, recursos = conflicto
        print(
            "No se guardaron los cambios: el "
            f"{' y '.join(recursos)} tiene otra ruta en ese horario."
        )
        candidata["hora_salida"] = leer_hora(
            "Ingrese otra hora de salida (HH:MM): "
        )
        conflicto = hay_conflicto_horario(candidata, otras_rutas)
    rutas[indice] = candidata
    print("Ruta actualizada.")


def gestionar_registros(conductores, vehiculos, rutas):
    while True:
        limpiar_pantalla()
        print("\n======== Gestión de registros ========")
        print("1. Editar o eliminar conductores")
        print("2. Editar o eliminar vehículos")
        print("3. Editar o eliminar rutas")
        print("4. Volver")
        opcion = input("Seleccione una opción (1-4): ").strip()
        if opcion == "1":
            _gestionar_conductores(conductores, rutas)
        elif opcion == "2":
            _gestionar_vehiculos(vehiculos, rutas)
        elif opcion == "3":
            _gestionar_rutas(conductores, vehiculos, rutas)
        elif opcion == "4":
            return
        else:
            print("Opción no válida.")
        input("Presione Enter para continuar...")
