# from unittest.mock import patch
# from Generador import Generador

# def test_generar_hash_success():
#     with patch('hashlib.sha1') as mock_hash:
#         hash_instance = mock_hash.return_value
#         hash_instance.hexdigest.return_value = 'hashcode'
#         result = Generador.generar_hash()
#         assert result == 'hashcode', "Debería devolver el hash correcto"

# def test_generar_archivos_success():
#     with patch('Generador.Generador.generar_hash', return_value='hashcode'), \
#          patch('Configuracion.Configuracion.misiones', return_value=['Mision1']), \
#          patch('Configuracion.Configuracion.dispositivos_mision', return_value=['Dispositivo1']), \
#          patch('Configuracion.Configuracion.estado', return_value=['Estado1']), \
#          patch('os.makedirs'), \
#          patch('builtins.open', mock_open()):
#         Generador.generar_archivos()
#         # Aquí puedes añadir aserciones para verificar que se llamaron las funciones de creación de directorios y archivos correctamente
# # 