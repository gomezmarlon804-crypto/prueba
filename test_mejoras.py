import unittest
from contextlib import redirect_stdout
from io import StringIO
from unittest.mock import patch

import menu
import login_admin
from mostrar_ruta_usuario import mostrar_ruta_usuario
from gestion_registros import (
    _gestionar_conductores,
    _gestionar_rutas,
    _gestionar_vehiculos,
)
from horario import calcular_horarios, hay_conflicto_horario
from registrar import registrar
from seguridad import proteger_clave, verificar_clave
from usuarios_data import usuarios


def crear_ruta(hora, duracion, identificacion="ID-1", vehiculo="ABC123"):
    return {
        "identificacion": identificacion,
        "vehiculo": vehiculo,
        "hora_salida": hora,
        "tiempo_total_recorrido": duracion,
    }


class PruebasHorario(unittest.TestCase):
    def test_calcula_regreso_con_duraciones_independientes(self):
        ruta = {
            "hora_salida": "08:00",
            "paradas": [
                {"nombre": "Parada 1", "tiempo": 10},
                {"nombre": "Parada 2", "tiempo": 20},
            ],
            "tiempo_destino": 15,
            "regresa": True,
            "tiempos_regreso": [12, 8, 25],
        }

        self.assertEqual(
            calcular_horarios(ruta),
            (["08:10", "08:30"], "08:45", ["08:57", "09:05", "09:30"], "09:30"),
        )

    def test_horario_cruza_medianoche(self):
        ruta = {
            "hora_salida": "23:50",
            "paradas": [{"nombre": "Parada", "tiempo": 15}],
            "tiempo_destino": 10,
            "regresa": False,
            "tiempos_regreso": [],
        }

        self.assertEqual(
            calcular_horarios(ruta),
            (["00:05 (+1 día)"], "00:15 (+1 día)", [], None),
        )

    def test_detecta_cruce_de_horario_incluso_al_cruzar_medianoche(self):
        existente = crear_ruta("23:40", 50)
        nueva = crear_ruta("00:10", 30)

        self.assertEqual(
            hay_conflicto_horario(nueva, [existente]),
            (existente, ["conductor", "vehículo"]),
        )

    def test_permite_rutas_consecutivas_sin_superposicion(self):
        existente = crear_ruta("08:00", 60)
        nueva = crear_ruta("09:00", 30)

        self.assertIsNone(hay_conflicto_horario(nueva, [existente]))

    def test_detecta_conflicto_de_vehiculo_aunque_cambie_conductor(self):
        existente = crear_ruta("08:00", 60, identificacion="ID-1")
        nueva = crear_ruta("08:30", 30, identificacion="ID-2")

        self.assertEqual(
            hay_conflicto_horario(nueva, [existente]),
            (existente, ["vehículo"]),
        )


class PruebasRegistros(unittest.TestCase):
    def setUp(self):
        menu.conductores.clear()
        menu.vehiculos.clear()
        menu.rutas.clear()

    def test_conductor_reporta_retraso_y_usuario_ve_sugerencias(self):
        ruta = crear_ruta("08:00", 60)
        ruta.update({
            "conductor": "Ana",
            "origen": "Centro",
            "destino": "Terminal",
            "vehiculo": "ABC123",
            "regresa": False,
            "paradas": [],
            "tiempo_destino": 30,
            "tiempos_regreso": [],
        })
        menu.rutas.append(ruta)
        menu.vehiculos.append({
            "placa": "ABC123",
            "marca": "",
            "modelo": "",
            "tipo": "urbano",
            "capacidad": 40,
        })

        with (
            patch("menu.limpiar_pantalla"),
            patch("builtins.input", side_effect=["1", "15", "1"]),
            redirect_stdout(StringIO()),
        ):
            menu.reportar_retraso()

        salida = StringIO()
        with redirect_stdout(salida):
            mostrar_ruta_usuario(ruta)

        self.assertEqual(ruta["retraso"]["minutos"], 15)
        self.assertIn("AVISO DE RETRASO", salida.getvalue())
        self.assertIn("Sugerencias para el pasajero", salida.getvalue())

    def test_capacidad_de_vehiculo_debe_ser_positiva(self):
        with (
            patch("menu.limpiar_pantalla"),
            patch(
                "builtins.input",
                side_effect=["ABC123", "", "", "", "urbano", "0"],
            ),
            redirect_stdout(StringIO()),
        ):
            menu.registrar_vehiculo()

        self.assertEqual(menu.vehiculos, [])

    def test_no_permite_identificaciones_duplicadas(self):
        menu.conductores.append(
            {"nombre": "Ana", "identificacion": "ID-1", "telefono": "555"}
        )
        with (
            patch("menu.limpiar_pantalla"),
            patch(
                "builtins.input",
                side_effect=["Luis", "id-1", "555-2"],
            ),
            redirect_stdout(StringIO()),
        ):
            menu.registrar_conductor()

        self.assertEqual(len(menu.conductores), 1)

    def test_asigna_ruta_con_regreso_y_horarios_independientes(self):
        menu.conductores.append(
            {"nombre": "Ana", "identificacion": "ID-1", "telefono": "555"}
        )
        menu.vehiculos.append(
            {
                "placa": "ABC123",
                "marca": "",
                "modelo": "",
                "anio": "",
                "tipo": "urbano",
                "capacidad": 40,
            }
        )
        respuestas = [
            "1", "1", "Centro", "Terminal", "s", "1", "08:00",
            "Parada", "10", "20", "15", "25",
        ]
        with (
            patch("menu.limpiar_pantalla"),
            patch("builtins.input", side_effect=respuestas),
            redirect_stdout(StringIO()),
        ):
            menu.asignar_ruta()

        ruta = menu.rutas[0]
        self.assertEqual(ruta["tiempo_vuelta"], 40)
        self.assertEqual(
            calcular_horarios(ruta),
            (["08:10"], "08:30", ["08:45", "09:10"], "09:10"),
        )

    def test_rechaza_asignacion_que_se_superpone(self):
        menu.conductores.append(
            {"nombre": "Ana", "identificacion": "ID-1", "telefono": "555"}
        )
        menu.vehiculos.append(
            {
                "placa": "ABC123",
                "marca": "",
                "modelo": "",
                "anio": "",
                "tipo": "urbano",
                "capacidad": 40,
            }
        )
        menu.rutas.append(
            {
                "conductor": "Ana",
                "identificacion": "ID-1",
                "vehiculo": "ABC123",
                "origen": "Centro",
                "destino": "Terminal",
                "hora_salida": "08:00",
                "regresa": True,
                "paradas": [{"nombre": "Parada", "tiempo": 10}],
                "cantidad_paradas": 1,
                "tiempo_destino": 20,
                "tiempos_regreso": [15, 25],
                "tiempo_total": 30,
                "tiempo_vuelta": 40,
                "tiempo_total_recorrido": 70,
            }
        )
        respuestas = [
            "1", "1", "Otro", "Destino2", "n", "1", "08:20",
            "P2", "10", "20",
        ]
        salida = StringIO()
        with (
            patch("menu.limpiar_pantalla"),
            patch("builtins.input", side_effect=respuestas),
            redirect_stdout(salida),
        ):
            menu.asignar_ruta()

        self.assertEqual(len(menu.rutas), 1)
        self.assertIn("superpuesta", salida.getvalue())

    def test_no_elimina_conductor_con_rutas_asignadas(self):
        conductor = {"nombre": "Ana", "identificacion": "ID-1", "telefono": "555"}
        menu.conductores.append(conductor)
        ruta = crear_ruta("08:00", 60)
        ruta.update({"conductor": "Ana"})
        menu.rutas.append(ruta)

        with (
            patch("builtins.input", side_effect=["1", "d"]),
            redirect_stdout(StringIO()),
        ):
            _gestionar_conductores(menu.conductores, menu.rutas)

        self.assertEqual(menu.conductores, [conductor])

    def test_editar_conductor_actualiza_ruta(self):
        conductor = {"nombre": "Ana", "identificacion": "ID-1", "telefono": "555"}
        ruta = crear_ruta("08:00", 60)
        ruta["conductor"] = "Ana"
        menu.conductores.append(conductor)
        menu.rutas.append(ruta)

        with (
            patch(
                "builtins.input",
                side_effect=["1", "e", "Ana María", "ID-2", ""],
            ),
            redirect_stdout(StringIO()),
        ):
            _gestionar_conductores(menu.conductores, menu.rutas)

        self.assertEqual(ruta["identificacion"], "ID-2")
        self.assertEqual(ruta["conductor"], "Ana María")

    def test_editar_placa_actualiza_rutas_asignadas(self):
        vehiculo = {
            "placa": "ABC123",
            "marca": "",
            "modelo": "",
            "anio": "",
            "tipo": "urbano",
            "capacidad": 40,
        }
        ruta = crear_ruta("08:00", 60)
        menu.vehiculos.append(vehiculo)
        menu.rutas.append(ruta)

        with (
            patch(
                "builtins.input",
                side_effect=["1", "e", "XYZ789", "", "", "", "", ""],
            ),
            redirect_stdout(StringIO()),
        ):
            _gestionar_vehiculos(menu.vehiculos, menu.rutas)

        self.assertEqual(vehiculo["placa"], "XYZ789")
        self.assertEqual(ruta["vehiculo"], "XYZ789")

    def test_edita_hora_de_ruta(self):
        ruta = {
            "conductor": "Ana",
            "identificacion": "ID-1",
            "vehiculo": "ABC123",
            "origen": "Centro",
            "destino": "Terminal",
            "hora_salida": "08:00",
            "regresa": False,
            "paradas": [{"nombre": "Parada", "tiempo": 10}],
            "cantidad_paradas": 1,
            "tiempo_destino": 20,
            "tiempos_regreso": [],
            "tiempo_total": 30,
            "tiempo_vuelta": 0,
            "tiempo_total_recorrido": 30,
        }
        menu.rutas.append(ruta)

        with (
            patch("builtins.input", side_effect=["1", "e", "5", "08:30", "0"]),
            redirect_stdout(StringIO()),
        ):
            _gestionar_rutas(menu.conductores, menu.vehiculos, menu.rutas)

        self.assertEqual(menu.rutas[0]["hora_salida"], "08:30")

    def test_elimina_ruta_seleccionada(self):
        menu.rutas.append(
            {
                "origen": "Centro",
                "destino": "Terminal",
                "hora_salida": "08:00",
            }
        )

        with (
            patch("builtins.input", side_effect=["1", "d", "s"]),
            redirect_stdout(StringIO()),
        ):
            _gestionar_rutas(menu.conductores, menu.vehiculos, menu.rutas)

        self.assertEqual(menu.rutas, [])


class PruebasContrasenas(unittest.TestCase):
    def test_clave_se_guarda_con_hash_y_se_verifica(self):
        protegida = proteger_clave("clave-segura")

        self.assertNotEqual(protegida, "clave-segura")
        self.assertTrue(verificar_clave("clave-segura", protegida))
        self.assertFalse(verificar_clave("otra-clave", protegida))

    def test_registro_no_guarda_la_clave_en_texto_plano(self):
        usuarios.clear()
        with (
            patch("registrar.pedir_credenciales", return_value=("admin", "secreta")),
            patch("builtins.input", return_value=""),
            redirect_stdout(StringIO()),
        ):
            registrar("admin")

        self.assertNotEqual(usuarios[0]["clave"], "secreta")
        self.assertTrue(verificar_clave("secreta", usuarios[0]["clave"]))
        usuarios.clear()

    def test_login_admin_acepta_clave_protegida(self):
        usuarios[:] = [
            {
                "nombre": "admin",
                "clave": proteger_clave("secreta"),
                "rol": "admin",
            }
        ]
        with (
            patch("login_admin.limpiar_pantalla"),
            patch(
                "login_admin.pedir_credenciales",
                return_value=("admin", "secreta"),
            ),
            patch("login_admin.menu.main") as menu_admin,
            patch("builtins.input", return_value=""),
            redirect_stdout(StringIO()),
        ):
            login_admin.login_admin()

        menu_admin.assert_called_once_with()
        usuarios.clear()


if __name__ == "__main__":
    unittest.main()
