"""Configuración del archivo de logs."""
import logging
import os

# Ruta del archivo de log junto a este módulo
RUTA_LOG = os.path.join(os.path.dirname(os.path.abspath(__file__)), "software_fj.log")


def obtener_logger() -> logging.Logger:
    """Devuelve el logger del sistema, creándolo una sola vez."""
    logger = logging.getLogger("software_fj")  # nombre único del logger
    if not logger.handlers:  # evita duplicar handlers si se llama varias veces
        logger.setLevel(logging.DEBUG)  # registra todos los niveles
        manejador = logging.FileHandler(RUTA_LOG, encoding="utf-8")  # escribe en archivo
        formato = logging.Formatter(
            "%(asctime)s | %(levelname)-8s | %(message)s", "%Y-%m-%d %H:%M:%S"
        )  # formato: fecha | nivel | mensaje
        manejador.setFormatter(formato)  # asigna el formato al manejador
        logger.addHandler(manejador)  # conecta el manejador al logger
    return logger
