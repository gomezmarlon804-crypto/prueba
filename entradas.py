from datetime import datetime


def leer_texto(mensaje):
    while True:
        texto = input(mensaje).strip()
        if texto:
            return texto
        print("Este dato no puede estar vacío.")


def leer_opcion(mensaje, opciones):
    opciones_validas = {str(opcion) for opcion in opciones}
    while True:
        opcion = input(mensaje).strip()
        if opcion in opciones_validas:
            return opcion
        print(f"Opción inválida. Seleccione una de estas: {', '.join(sorted(opciones_validas))}.")


def leer_entero(mensaje, minimo=None, maximo=None):
    while True:
        try:
            numero = int(input(mensaje).strip())
        except ValueError:
            print("Debe ingresar un número entero válido.")
            continue
        if minimo is not None and numero < minimo:
            print(f"El valor debe ser mayor o igual que {minimo}.")
            continue
        if maximo is not None and numero > maximo:
            print(f"El valor debe ser menor o igual que {maximo}.")
            continue
        return numero


def leer_si_no(mensaje):
    while True:
        respuesta = input(mensaje).strip().casefold()
        if respuesta in ("s", "n"):
            return respuesta
        print("Responda solamente 's' para sí o 'n' para no.")


def leer_hora(mensaje="Ingrese la hora (HH:MM): "):
    while True:
        valor = input(mensaje).strip()
        try:
            return datetime.strptime(valor, "%H:%M").strftime("%H:%M")
        except ValueError:
            print("Hora inválida. Use el formato HH:MM, por ejemplo 08:30.")
