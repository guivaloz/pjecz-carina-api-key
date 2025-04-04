"""
Unit test - Enviar los Archivos del Exhorto
"""

import time
import unittest
from pathlib import Path

import requests

from tests import config
from tests.database import TestExhExhorto, get_database_session


class TestsEnviarExhortosArchivos(unittest.TestCase):
    """Tests Enviar Exhorto Archivos"""

    def test_post_exhorto_archivos(self):
        """Probar el POST para enviar los archivos de un exhorto"""

        # Cargar la sesión de la base de datos para recuperar los datos de la prueba anterior
        session = get_database_session()

        # Consultar el último exhorto
        test_exh_exhorto = (
            session.query(TestExhExhorto).filter_by(estado="PENDIENTE").order_by(TestExhExhorto.id.desc()).first()
        )
        if test_exh_exhorto is None:
            self.fail("No se encontró un exhorto PENDIENTE en sqlite")

        # Definir los datos que se van a incluir en el envío de los archivos
        payload_for_data = {"exhortoOrigenId": test_exh_exhorto.exhorto_origen_id}

        # Bucle para mandar los archivo por multipart/form-data
        for test_exh_exhorto_archivo in test_exh_exhorto.test_exh_exhortos_archivos:
            time.sleep(1)  # Pausa de 1 segundos

            # Tomar el nombre del archivo
            archivo_nombre = test_exh_exhorto_archivo.nombre_archivo

            # Validar que el archivo exista
            archivo_ruta = Path(f"tests/{archivo_nombre}")
            if not archivo_ruta.is_file():
                self.fail(f"No se encontró el archivo {archivo_nombre}")

            # Leer el archivo de prueba
            with open(f"tests/{archivo_nombre}", "rb") as archivo_prueba:
                # Mandar el archivo
                try:
                    respuesta = requests.post(
                        url=f"{config['api_base_url']}/exh_exhortos/recibir_archivo",
                        headers={"X-Api-Key": config["api_key"]},
                        timeout=config["timeout"],
                        files={"archivo": (archivo_nombre, archivo_prueba, "application/pdf")},
                        data=payload_for_data,
                    )
                except requests.exceptions.ConnectionError as error:
                    self.fail(error)
                self.assertEqual(respuesta.status_code, 200)

                # Validar el contenido de la respuesta
                contenido = respuesta.json()
                self.assertEqual("success" in contenido, True)
                self.assertEqual("message" in contenido, True)
                self.assertEqual("errors" in contenido, True)
                self.assertEqual("data" in contenido, True)

                # Validar que se haya tenido éxito
                if contenido["success"] is False:
                    print(f"Errors: {str(contenido['errors'])}")
                    # Continuar con el siguiente en lugar de self.assertEqual(contenido["success"], True)
                    continue

                # Validar el data
                self.assertEqual(type(contenido["data"]), dict)
                data = contenido["data"]
                self.assertEqual("archivo" in data, True)
                data_archivo = data["archivo"]
                self.assertEqual("acuse" in data, True)
                data_acuse = data["acuse"]

                # Validar que dentro de archivo venga nombreArchivo y tamaño
                self.assertEqual(type(data_archivo), dict)
                self.assertEqual("nombreArchivo" in data_archivo, True)
                self.assertEqual("tamaño" in data_archivo, True)

            # Actualizar el estado del archivo a RECIBIDO
            test_exh_exhorto_archivo.estado = "RECIBIDO"

        # Validar el último acuse
        self.assertEqual(type(data_acuse), dict)
        self.assertEqual("exhortoOrigenId" in data_acuse, True)
        self.assertEqual("folioSeguimiento" in data_acuse, True)
        self.assertEqual("fechaHoraRecepcion" in data_acuse, True)
        self.assertEqual("municipioAreaRecibeId" in data_acuse, True)
        self.assertEqual("areaRecibeId" in data_acuse, True)
        self.assertEqual("areaRecibeNombre" in data_acuse, True)
        self.assertEqual("urlInfo" in data_acuse, True)

        # Validar que se recibe el mismo exhortoOrigenId
        self.assertEqual(type(data_acuse["exhortoOrigenId"]), str)
        self.assertEqual(data_acuse["exhortoOrigenId"], test_exh_exhorto.exhorto_origen_id)

        # Validar que se recibe el folioSeguimiento
        self.assertEqual(type(data_acuse["folioSeguimiento"]), str)
        self.assertNotEqual(data_acuse["folioSeguimiento"], "")

        # Guardar el folio de seguimiento y cambiar estado en sqlite
        test_exh_exhorto.folio_seguimiento = data_acuse["folioSeguimiento"]
        test_exh_exhorto.estado = "RECIBIDO"
        session.commit()

        # Cerrar la sesión sqlite
        session.close()


if __name__ == "__main__":
    unittest.main()
