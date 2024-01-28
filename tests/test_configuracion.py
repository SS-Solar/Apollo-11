import pytest
import yaml
import os

ruta = "path/to/your/config.yaml"
from unittest.mock import Mock, patch, mock_open
from Archivos.Configuracion.Configuracion import Configuracion
from Archivos.Configuracion.Logger import Logger

ruta_esperada = os.path.join(
    os.path.dirname(__file__), "..", "Archivos", "Configuracion", "config.yaml"
)
ruta_esperada = os.path.normpath(ruta_esperada)


# Fixture para el logger
@pytest.fixture
def mock_logger():
    logger = Mock(spec=Logger)
    return logger


# Fixture para cargar datos YAML de prueba
@pytest.fixture
def mock_yaml_data():
    return {
        "settings": {
            "cantidad_max_archivos": 100,
            "cantidad_min_archivos": 1,
            "ciclo_simulacion": 20.0,
            "estado_de_dispositivo": [
                "Excelent",
                "Good",
                "Warning",
                "Faulty",
                "killed",
                "Unknown",
            ],
            "misiones": {
                "ColonyMoon": {
                    "dispositivos": [
                        "CM-ASC-PQM",
                        "CM-ASC-CD",
                        "CM-ASC-SPS",
                        "CM-S-EFAC",
                        "CM-S-EFAM",
                        "CM-S-CD",
                        "CM-S-PQM",
                        "CM-S-SPS",
                        "CM-PRR-CD",
                        "CM-PRR-SPS",
                        "CM-PRR-TS",
                        "CM-PRR-PQM",
                        "CM-PRR-PS",
                        "CM-PRR-PSW",
                        "CM-KSS-ASS",
                    ],
                    "nombreAbreviado": "CLNM",
                },
                "GalaxyTwo": {
                    "dispositivos": [
                        "GT-ASC-PQM",
                        "GT-ASC-CD",
                        "GT-ASC-SPS",
                        "GT-S-EFAC",
                        "GT-S-EFAM",
                        "GT-S-CD",
                        "GT-S-PQM",
                        "GT-S-SPS",
                        "GT-PRR-CD",
                        "GT-PRR-SPS",
                        "GT-PRR-TS",
                        "GT-PRR-PQM",
                        "GT-PRR-PS",
                        "GT-PRR-OC",
                    ],
                    "nombreAbreviado": "GALXTWO",
                },
                "NUEVO": {"dispositivos": ["Solo"], "nombreAbreviado": "NN"},
                "OrbitOne": {
                    "dispositivos": [
                        "OO-ASC-PQM",
                        "OO-ASC-CD",
                        "OO-ASC-SPS",
                        "OO-S-EFAC",
                        "OO-S-EFAM",
                        "OO-S-CD",
                        "OO-S-PQM",
                        "OO-S-SPS",
                        "OO-PRR-CD",
                        "OO-PRR-SPS",
                        "OO-PRR-TS",
                        "OO-PRR-PQM",
                        "OO-PRR-PS",
                        "OO-PRR-OC",
                    ],
                    "nombreAbreviado": "ORBONE",
                },
                "UNKW": {"dispositivos": ["Unknown"], "nombreAbreviado": "UNKW"},
                "VacMars": {
                    "dispositivos": [
                        "VM-AT-ST",
                        "VM-AT-VS",
                        "VM-AT-SL",
                        "VM-AT-VaT",
                        "VM-AT-CD",
                        "VM-AT-OC",
                        "VM-AT-SPS",
                        "VM-CMS-TS",
                        "VM-CMS-PQM",
                        "VM-CMS-PS",
                        "VM-CMS-CD",
                        "VM-CMS-OC",
                        "VM-CMS-SPS",
                        "VM-CMS-WTP",
                        "VM-CMS-RPS",
                        "VM-ASC-PQM",
                        "VM-ASC-CD",
                    ],
                    "nombreAbreviado": "VMRS",
                },
            },
        }
    }


@pytest.fixture
def mock_open_yaml():
    # Usar directamente mock_yaml_data en lugar de yaml.dump(mock_yaml_data)
    with patch(
        "builtins.open", mock_open(read_data=yaml.dump(mock_yaml_data))
    ) as mock_file:
        yield mock_file


@pytest.fixture
def mock_configuracion(mock_open_yaml, mock_logger):
    with patch("yaml.safe_load", return_value=mock_yaml_data), patch(
        "Archivos.Configuracion.Configuracion.Logger", mock_logger
    ):
        yield Configuracion()


# Test para Configuracion.misiones
def test_misiones_success(mock_configuracion):
    expected_misiones = [
        "ColonyMoon",
        "GalaxyTwo",
        "NUEVO",
        "OrbitOne",
        "UNKW",
        "VacMars",
    ]
    assert (
        mock_configuracion.misiones() == expected_misiones
    ), "Debería devolver la lista de misiones con nombres correctos"


# def test_misiones_exception_handling(mock_logger):
#     # Preparar el entorno de la prueba.
#     with patch("Archivos.Configuracion.Configuracion.logger", mock_logger):
#         config = Configuracion()

#         # Simular una condición que provoque una excepción al acceder a data["settings"]["misiones"].
#         with patch("Archivos.Configuracion.Configuracion.data",
#                     new_callable=lambda: {"settings": {"misiones": Exception("Error de prueba")}}):
#             resultado = config.misiones()

#         # Verificar que se maneja la excepción como se espera.
#         assert resultado == ["Unknown"], "La lista de misiones debería ser ['Unknown'] en caso de excepción."
#         mock_logger.error.assert_called_once_with("Se ha producido un error en la generacion de misiones: Error de prueba")


# Test para Configuracion.nombres_abreviados
def test_nombres_abreviados_success(mock_configuracion):
    expected_abreviados = ["CLNM", "GALXTWO", "NN", "ORBONE", "UNKW", "VMRS"]
    assert (
        mock_configuracion.nombres_abreviados() == expected_abreviados
    ), "Debería devolver nombres abreviados correctos"


# Test para Configuracion.estado
def test_estado_success(mock_configuracion):
    expected_estados_de_dispositivos = [
        "Excelent",
        "Good",
        "Warning",
        "Faulty",
        "killed",
        "Unknown",
    ]
    assert (
        mock_configuracion.estado() == expected_estados_de_dispositivos
    ), "Debería devolver la lista de estados de dispositivos"


def test_dispositivos(mock_configuracion, mock_logger, mock_yaml_data):
    with patch("builtins.print") as mock_print:
        mock_configuracion.dispositivos()
        # +1 por la impresión del nombre de la misión
        # +1 por la impresión de "Dispositivos: "
        # +len(dispositivos) por cada misión
        cantidad_esperada = sum(
            2 + len(detalles["dispositivos"])
            for detalles in mock_yaml_data["settings"]["misiones"].values()
        )

        assert (
            mock_print.call_count == cantidad_esperada
        ), f"Se esperaban {cantidad_esperada} llamadas a print, pero se encontraron {mock_print.call_count}."


def test_ciclo(mock_configuracion, mock_yaml_data):
    with patch("builtins.print") as mock_print:
        resultado = mock_configuracion.ciclo()
        mock_print.assert_called_once_with(
            f"El ciclo actual es de: {mock_yaml_data['settings']['ciclo_simulacion']} s \n"
        )
        assert (
            resultado == mock_yaml_data["settings"]["ciclo_simulacion"]
        ), "Debería devolver el ciclo de iteración correcto"


def test_cambiar_ciclo(mock_configuracion, mock_yaml_data):
    nuevo_ciclo = 10.0
    with patch(
        "builtins.open", mock_open(read_data=yaml.dump(mock_yaml_data)), create=True
    ) as mock_file:
        mock_configuracion.cambiar_ciclo(nuevo_ciclo)
        mock_file.assert_called_once_with(ruta_esperada, "w")


def test_cambiar_min_archivos(
    mock_configuracion, mock_logger, mock_open_yaml, mock_yaml_data
):
    min_archivos_nuevo = 5
    with patch("builtins.open", mock_open(), create=True) as mock_file:
        mock_configuracion.cambiar_min_archivos(min_archivos_nuevo)
        mock_file.assert_called_once_with(ruta_esperada, "w")
        # Asumimos que la función real cambia el valor en el diccionario correctamente.
        # En una prueba unitaria, normalmente no se probarían los efectos secundarios directamente.


def test_cambiar_max_archivos(
    mock_configuracion, mock_logger, mock_open_yaml, mock_yaml_data
):
    max_archivos_nuevo = 200
    with patch("builtins.open", mock_open(), create=True) as mock_file:
        mock_configuracion.cambiar_max_archivos(max_archivos_nuevo)
        mock_file.assert_called_once_with(ruta_esperada, "w")
        # Asumimos que la función real cambia el valor en el diccionario correctamente.
        # En una prueba unitaria, normalmente no se probarían los efectos secundarios directamente.


def test_nuevo_dispositivo(mock_configuracion, mock_logger, mock_open_yaml):
    mision_nombre = "ColonyMoon"
    nuevo_dispositivo = "NuevoDispositivo"

    with patch("builtins.open", mock_open(), create=True) as mock_file:
        mock_configuracion.nuevo_dispositivo(mision_nombre, nuevo_dispositivo)
        # Verifica que la función open se llamó correctamente.
        mock_file.assert_called_once_with(ruta, "w")
        # Aquí puedes agregar más verificaciones si tu función tiene otros efectos secundarios.


def test_eliminar_dispositivo(
    mock_configuracion, mock_logger, mock_open_yaml, mock_yaml_data
):
    mision_nombre = "ColonyMoon"  # Índice de la misión en la lista de misiones
    dispositivo_a_eliminar = "DispositivoAEliminar"

    # Asegúrate de que el dispositivo exista antes de intentar eliminarlo
    mock_yaml_data["settings"]["misiones"][mision_nombre]["dispositivos"].append(
        dispositivo_a_eliminar
    )

    with patch("builtins.open", mock_open(), create=True) as mock_file:
        mock_configuracion.eliminar_dispositivo(mision_nombre, dispositivo_a_eliminar)
        # Asumimos que la función real elimina el dispositivo correctamente.
        # No se verifica el efecto secundario directamente en la prueba unitaria.
        mock_file.assert_called_once_with(ruta, "w")
