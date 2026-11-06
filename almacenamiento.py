import json
import os
from pathlib import Path

from seguridad import proteger_clave

# Directorio base de datos
DATA_DIR = Path(__file__).resolve().parent / "data"
USUARIOS_FILE = DATA_DIR / "usuarios.json"
CONDUCTORES_FILE = DATA_DIR / "conductores.json"
VEHICULOS_FILE = DATA_DIR / "vehiculos.json"
RUTAS_FILE = DATA_DIR / "rutas.json"


def establecer_directorio_datos(nuevo_directorio):
    """Permite configurar un directorio alternativo para datos (ej. pruebas)."""
    global DATA_DIR, USUARIOS_FILE, CONDUCTORES_FILE, VEHICULOS_FILE, RUTAS_FILE
    DATA_DIR = Path(nuevo_directorio)
    USUARIOS_FILE = DATA_DIR / "usuarios.json"
    CONDUCTORES_FILE = DATA_DIR / "conductores.json"
    VEHICULOS_FILE = DATA_DIR / "vehiculos.json"
    RUTAS_FILE = DATA_DIR / "rutas.json"


def guardar_json(ruta_archivo, datos):
    """Guarda una estructura de datos en formato JSON en disco."""
    ruta = Path(ruta_archivo)
    ruta.parent.mkdir(parents=True, exist_ok=True)
    with open(ruta, "w", encoding="utf-8") as archivo:
        json.dump(datos, archivo, ensure_ascii=False, indent=2)


def cargar_json(ruta_archivo, por_defecto=None):
    """Carga datos desde un archivo JSON con manejo de excepciones."""
    if por_defecto is None:
        por_defecto = []
    ruta = Path(ruta_archivo)
    if not ruta.is_file():
        return por_defecto
    try:
        with open(ruta, "r", encoding="utf-8") as archivo:
            contenido = archivo.read().strip()
            if not contenido:
                return por_defecto
            return json.loads(contenido)
    except (FileNotFoundError, json.JSONDecodeError, OSError):
        return por_defecto


def generar_datos_semilla():
    """Genera datos de prueba realistas para inicializar el sistema."""
    usuarios_semilla = [
        {
            "nombre": "admin",
            "clave": proteger_clave("admin123"),
            "rol": "admin",
            "pregunta": "¿Cómo se llama tu mascota?",
            "respuesta": proteger_clave("firulais"),
        },
        {
            "nombre": "pasajero",
            "clave": proteger_clave("pasajero123"),
            "rol": "usuario",
            "pregunta": "¿Cuál es tu comida favorita?",
            "respuesta": proteger_clave("pizza"),
        },
    ]

    conductores_semilla = [
        {
            "nombre": "Carlos Mendoza",
            "identificacion": "COND-001",
            "telefono": "555-1234",
        },
        {
            "nombre": "Laura Gómez",
            "identificacion": "COND-002",
            "telefono": "555-5678",
        },
    ]

    vehiculos_semilla = [
        {
            "placa": "BUS-101",
            "marca": "Mercedes-Benz",
            "modelo": "Sprinter",
            "anio": "2022",
            "tipo": "Microbús",
            "capacidad": 15,
        },
        {
            "placa": "BUS-202",
            "marca": "Volvo",
            "modelo": "B8R",
            "anio": "2021",
            "tipo": "Autobús interurbano",
            "capacidad": 40,
        },
    ]

    rutas_semilla = [
        {
            "conductor": "Carlos Mendoza",
            "identificacion": "COND-001",
            "vehiculo": "BUS-101",
            "origen": "Terminal Central",
            "destino": "Campus Universitario",
            "hora_salida": "07:00",
            "regresa": True,
            "paradas": [
                {"nombre": "Plaza Mayor", "tiempo": 15},
                {"nombre": "Av. Tecnológico", "tiempo": 10},
            ],
            "cantidad_paradas": 2,
            "tiempo_destino": 15,
            "tiempos_regreso": [15, 10, 15],
            "tiempo_total": 40,
            "tiempo_vuelta": 40,
            "tiempo_total_recorrido": 80,
            "asientos_ocupados": 3,
        },
        {
            "conductor": "Laura Gómez",
            "identificacion": "COND-002",
            "vehiculo": "BUS-202",
            "origen": "Estación Norte",
            "destino": "Parque Industrial",
            "hora_salida": "08:30",
            "regresa": False,
            "paradas": [
                {"nombre": "Zona Residencial", "tiempo": 20},
                {"nombre": "Centro Comercial", "tiempo": 15},
            ],
            "cantidad_paradas": 2,
            "tiempo_destino": 25,
            "tiempos_regreso": [],
            "tiempo_total": 60,
            "tiempo_vuelta": 0,
            "tiempo_total_recorrido": 60,
            "asientos_ocupados": 5,
        },
    ]

    return {
        "usuarios": usuarios_semilla,
        "conductores": conductores_semilla,
        "vehiculos": vehiculos_semilla,
        "rutas": rutas_semilla,
    }


def guardar_usuarios(datos=None):
    if datos is None:
        import usuarios_data
        datos = usuarios_data.usuarios
    guardar_json(USUARIOS_FILE, datos)


def guardar_conductores(datos=None):
    if datos is None:
        import menu
        datos = menu.conductores
    guardar_json(CONDUCTORES_FILE, datos)


def guardar_vehiculos(datos=None):
    if datos is None:
        import menu
        datos = menu.vehiculos
    guardar_json(VEHICULOS_FILE, datos)


def guardar_rutas(datos=None):
    if datos is None:
        import menu
        datos = menu.rutas
    guardar_json(RUTAS_FILE, datos)


def guardar_todo(usuarios=None, conductores=None, vehiculos=None, rutas=None):
    guardar_usuarios(usuarios)
    guardar_conductores(conductores)
    guardar_vehiculos(vehiculos)
    guardar_rutas(rutas)


def cargar_datos():
    """
    Carga todos los datos desde disco o los inicializa con semillas si no existen
    o están vacíos. Sincroniza las listas en memoria de los módulos.
    """
    import menu
    import usuarios_data

    semillas = None

    def obtener_semillas():
        nonlocal semillas
        if semillas is None:
            semillas = generar_datos_semilla()
        return semillas

    # 1. Usuarios
    usuarios = cargar_json(USUARIOS_FILE, por_defecto=[])
    if not usuarios:
        usuarios = obtener_semillas()["usuarios"]
        guardar_usuarios(usuarios)

    # 2. Conductores
    conductores = cargar_json(CONDUCTORES_FILE, por_defecto=[])
    if not conductores:
        conductores = obtener_semillas()["conductores"]
        guardar_conductores(conductores)

    # 3. Vehículos
    vehiculos = cargar_json(VEHICULOS_FILE, por_defecto=[])
    if not vehiculos:
        vehiculos = obtener_semillas()["vehiculos"]
        guardar_vehiculos(vehiculos)

    # 4. Rutas
    rutas = cargar_json(RUTAS_FILE, por_defecto=[])
    if not rutas:
        rutas = obtener_semillas()["rutas"]
        guardar_rutas(rutas)

    # Sincronizar listas en memoria existentes
    usuarios_data.usuarios.clear()
    usuarios_data.usuarios.extend(usuarios)

    menu.conductores.clear()
    menu.conductores.extend(conductores)

    menu.vehiculos.clear()
    menu.vehiculos.extend(vehiculos)

    menu.rutas.clear()
    menu.rutas.extend(rutas)

    return {
        "usuarios": usuarios_data.usuarios,
        "conductores": menu.conductores,
        "vehiculos": menu.vehiculos,
        "rutas": menu.rutas,
    }

