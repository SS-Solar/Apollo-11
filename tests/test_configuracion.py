import pytest
import yaml
import os
from unittest.mock import Mock, patch, mock_open
from Archivos.Configuracion.Configuracion import Configuracion
from Archivos.Configuracion.Logger import Logger

"""Ruta al directorio donde se encuentra este script de pruebas."""
base_test_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

"""Ruta al directorio donde reside configuracion.py. """
ruta_absoluta = os.path.join(base_test_dir, "Archivos", "Configuracion")

"""Ruta que se usará en las aserciones de los tests"""
ruta_config_yaml = os.path.join(ruta_absoluta, 'config.yaml')




"""Fixture para el logger"""
@pytest.fixture
def mock_logger():
    logger = Mock(spec=Logger)
    return logger


"""Fixture para cargar datos YAML de prueba"""
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
    """
    Fixture de pytest para simular la apertura y lectura de un archivo YAML.
    
    Utiliza `mock_open` para crear un objeto mock que devuelve una cadena YAML
    serializada de `mock_yaml_data` cuando se llama a `open`. Este enfoque permite
    probar funciones que leen archivos sin acceder al sistema de archivos real.
    
    Devuelve:
        Objeto MagicMock que simula la función `open`.
    """
    with patch(
        "builtins.open", mock_open(read_data=yaml.dump(mock_yaml_data))
    ) as mock_file:
        yield mock_file


@pytest.fixture
def mock_configuracion(mock_open_yaml, mock_logger):
    """
    Proporciona una versión mockeada de la clase Configuracion para pruebas, con sus
    dependencias 'yaml.safe_load' y 'Logger' también mockeadas.
    
    Args:
        mock_open_yaml (fixture): Mock para la función 'open'.
        mock_logger (fixture): Mock para el Logger.

    Yields:
        Configuracion: Instancia mockeada de la clase Configuracion.
    """
    with patch("yaml.safe_load", return_value=mock_yaml_data), patch(
        "Archivos.Configuracion.Configuracion.Logger", mock_logger
    ):
        yield Configuracion()


"""Test para Configuracion.misiones"""
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


"""Test para Configuracion.nombres_abreviados"""
def test_nombres_abreviados_success(mock_configuracion):
    expected_abreviados = ["CLNM", "GALXTWO", "NN", "ORBONE", "UNKW", "VMRS"]
    assert (
        mock_configuracion.nombres_abreviados() == expected_abreviados
    ), "Debería devolver nombres abreviados correctos"


"""Test para Configuracion.estado"""
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

"""Test para ver dispositivos"""
def test_dispositivos(mock_configuracion, mock_logger, mock_yaml_data):
    with patch("builtins.print") as mock_print:
        mock_configuracion.dispositivos()
        """
        +1 por la impresión del nombre de la misión
        # +1 por la impresión de "Dispositivos: "
        # +len(dispositivos) por cada misión
        """
        cantidad_esperada = sum(
            2 + len(detalles["dispositivos"])
            for detalles in mock_yaml_data["settings"]["misiones"].values()
        )
        assert (
            mock_print.call_count == cantidad_esperada
        ), f"Se esperaban {cantidad_esperada} llamadas a print, pero se encontraron {mock_print.call_count}."

"""Test para ciclo"""
def test_ciclo(mock_configuracion, mock_yaml_data):
    with patch("builtins.print") as mock_print:
        resultado = mock_configuracion.ciclo()
        mock_print.assert_called_once_with(
            f"El ciclo actual es de: {mock_yaml_data['settings']['ciclo_simulacion']} s \n"
        )
        assert (
            resultado == mock_yaml_data["settings"]["ciclo_simulacion"]
        ), "Debería devolver el ciclo de iteración correcto"

"""Test para cambiar_ciclo"""
def test_cambiar_ciclo(mock_configuracion, mock_yaml_data):
    nuevo_ciclo = 10.0
    with patch(
        "builtins.open", mock_open(read_data=yaml.dump(mock_yaml_data)), create=True
    ) as mock_file:
        mock_configuracion.cambiar_ciclo(nuevo_ciclo)
        mock_file.assert_called_once_with(os.path.join(ruta_absoluta, 'config.yaml'), "w")


"""Test para cambiar_min_archivos"""
def test_cambiar_min_archivos(
    mock_configuracion, mock_logger, mock_open_yaml, mock_yaml_data
):
    min_archivos_nuevo = 5
    with patch("builtins.open", mock_open(), create=True) as mock_file:
        mock_configuracion.cambiar_min_archivos(min_archivos_nuevo)
        mock_file.assert_called_once_with(os.path.join(ruta_absoluta, 'config.yaml'), "w")



"""Test para cambiar_max_archivos"""
def test_cambiar_max_archivos(
    mock_configuracion, mock_logger, mock_open_yaml, mock_yaml_data
):
    max_archivos_nuevo = 200
    with patch("builtins.open", mock_open(), create=True) as mock_file:
        mock_configuracion.cambiar_max_archivos(max_archivos_nuevo)
        mock_file.assert_called_once_with(os.path.join(ruta_absoluta, 'config.yaml'), "w")



"""Test para nuevo_dispositivo"""
def test_nuevo_dispositivo(mock_configuracion, mock_logger, mock_yaml_data):
    mision_nombre = "ColonyMoon"
    nuevo_dispositivo = "NuevoDispositivo"
    # Simula la adición del dispositivo en mock_yaml_data
    mock_yaml_data["settings"]["misiones"][mision_nombre]["dispositivos"].append(nuevo_dispositivo)

    with patch("Archivos.Configuracion.Configuracion.open", mock_open(), create=True) as mock_file:
        mock_configuracion.nuevo_dispositivo(mision_nombre, nuevo_dispositivo)
        # Verifica que la función open se llamó correctamente.
        mock_file.assert_called_once_with(os.path.join(ruta_absoluta, 'config.yaml'), "w")




# def test_eliminar_dispositivo(mock_configuracion, mock_logger, mock_yaml_data):
#     dispositivo_a_eliminar = "DispositivoAEliminar"

#     for mision_nombre, mision_datos in mock_yaml_data["settings"]["misiones"].items():
#         # Asegúrate de que el dispositivo exista antes de intentar eliminarlo
#         if dispositivo_a_eliminar not in mision_datos["dispositivos"]:
#             mision_datos["dispositivos"].append(dispositivo_a_eliminar)

#         with patch("builtins.open", mock_open(), create=True) as mock_file:
#             try:
#                 # Llama a la función de eliminación de dispositivo
#                 mock_configuracion.eliminar_dispositivo(mision_nombre, dispositivo_a_eliminar)
#                 # Verifica que se llamó a la función open
#                 mock_file.assert_called_once_with(ruta_config_yaml, "w")
#                 # Verifica que el dispositivo fue eliminado
#                 assert dispositivo_a_eliminar not in mision_datos["dispositivos"], f"El dispositivo {dispositivo_a_eliminar} no fue eliminado de la misión {mision_nombre}"
#             except AssertionError as e:
#                 # Maneja cualquier AssertionError que ocurra durante la prueba
#                 print(f"Error en la prueba con la misión {mision_nombre}: {str(e)}")
#                 raise e






