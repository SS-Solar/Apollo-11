# import pytest
# from mock import patch
# from Configuracion import Configuracion

# def test_misiones_success():
#     mock_data = {
#         "settings": {
#             "misiones": {
#                 "ColonyMoon": {"nombreAbreviado": "CLNM"},
#                 "GalaxyTwo": {"nombreAbreviado": "GALXTWO"},
#                 # ... otros datos de misiones ...
#             }
#         }
#     }
#     with patch('yaml.safe_load', return_value=mock_data):
#         config = Configuracion()
#         expected_misiones = ["ColonyMoon", "GalaxyTwo"]
#         assert config.misiones() == expected_misiones, "Debería devolver la lista de misiones con nombres correctos"

# def test_nombres_abreviados_success():
#     mock_data = {
#         "settings": {
#             "misiones": {
#                 "ColonyMoon": {"nombreAbreviado": "CLNM"},
#                 "GalaxyTwo": {"nombreAbreviado": "GALXTWO"},
#                 # ... otros datos de misiones ...
#             }
#         }
#     }
#     with patch('yaml.safe_load', return_value=mock_data):
#         config = Configuracion()
#         expected_abreviados = ["CLNM", "GALXTWO"]
#         assert config.nombres_abreviados() == expected_abreviados, "Debería devolver nombres abreviados correctos"

# def test_estado_success():
#     mock_data = {
#         "settings": {
#             "estado_de_dispositivo": ["Excelent", "Good", "Warning", "Faulty", "killed", "Unknown"]
#         }
#     }
#     with patch('yaml.safe_load', return_value=mock_data):
#         config = Configuracion()
#         expected_estados = ["Excelent", "Good", "Warning", "Faulty", "killed", "Unknown"]
#         assert config.estado() == expected_estados, "Debería devolver la lista de estados de dispositivos"

# def test_suma():
#     pass
#     # assert(True)

def inc(x):
    return x + 1


def test_answer():
    assert inc(4) == 5