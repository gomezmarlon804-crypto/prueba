from datetime import datetime, timedelta


MINUTOS_POR_DIA = 24 * 60
MAX_MINUTOS_TRAMO = MINUTOS_POR_DIA


def _formatear_hora(hora, referencia):
    resultado = hora.strftime("%H:%M")
    dias_despues = (hora.date() - referencia.date()).days
    if dias_despues:
        unidad = "día" if dias_despues == 1 else "días"
        resultado += f" (+{dias_despues} {unidad})"
    return resultado


def calcular_horarios(ruta):
    salida = datetime.strptime(ruta["hora_salida"], "%H:%M")
    hora_actual = salida
    horarios_paradas = []

    for parada in ruta["paradas"]:
        hora_actual += timedelta(minutes=parada["tiempo"])
        horarios_paradas.append(_formatear_hora(hora_actual, salida))

    hora_actual += timedelta(minutes=ruta["tiempo_destino"])
    llegada = _formatear_hora(hora_actual, salida)

    horarios_regreso = []
    llegada_regreso = None
    if ruta["regresa"]:
        for tiempo_tramo in ruta["tiempos_regreso"]:
            hora_actual += timedelta(minutes=tiempo_tramo)
            horarios_regreso.append(_formatear_hora(hora_actual, salida))
        llegada_regreso = horarios_regreso[-1]

    return horarios_paradas, llegada, horarios_regreso, llegada_regreso


def _minutos_desde_medianoche(hora):
    momento = datetime.strptime(hora, "%H:%M")
    return momento.hour * 60 + momento.minute


def hay_conflicto_horario(nueva_ruta, rutas):
    inicio_nuevo = _minutos_desde_medianoche(nueva_ruta["hora_salida"])
    duracion_nueva = nueva_ruta["tiempo_total_recorrido"]
    fin_nuevo = inicio_nuevo + duracion_nueva

    for ruta in rutas:
        mismo_conductor = ruta["identificacion"] == nueva_ruta["identificacion"]
        mismo_vehiculo = ruta["vehiculo"] == nueva_ruta["vehiculo"]
        if not (mismo_conductor or mismo_vehiculo):
            continue

        inicio_existente = _minutos_desde_medianoche(ruta["hora_salida"])
        duracion_existente = ruta["tiempo_total_recorrido"]
        if duracion_nueva >= MINUTOS_POR_DIA or duracion_existente >= MINUTOS_POR_DIA:
            recursos = []
            if mismo_conductor:
                recursos.append("conductor")
            if mismo_vehiculo:
                recursos.append("vehículo")
            return ruta, recursos

        for dia in (-1, 0, 1):
            inicio_comparado = inicio_existente + dia * MINUTOS_POR_DIA
            fin_comparado = inicio_comparado + duracion_existente
            if inicio_nuevo < fin_comparado and inicio_comparado < fin_nuevo:
                recursos = []
                if mismo_conductor:
                    recursos.append("conductor")
                if mismo_vehiculo:
                    recursos.append("vehículo")
                return ruta, recursos

    return None
