from Archivos.Configuracion.logger import logger

# Ejemplo de mensajes de registro en otro archivo
logger.debug("Este mensaje solo se registra en el archivo")
logger.info("Este mensaje se registra en la consola y en el archivo")
logger.warning("Este mensaje se registra en la consola y en el archivo")
logger.error("Este mensaje se registra en la consola y en el archivo")