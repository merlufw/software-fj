"""Excepciones del sistema Software FJ.

Todas heredan de SoftwareFJError, de modo que el programa principal pueda
capturar cualquier error propio del dominio con un solo ``except``.
"""


class SoftwareFJError(Exception):
    """Excepción base de la que heredan todos los errores del sistema."""


class ClienteInvalidoError(SoftwareFJError):
    """Se lanza cuando los datos de un cliente no superan las validaciones."""


class ParametroFaltanteError(SoftwareFJError):
    """Se lanza cuando falta un parámetro obligatorio."""


class ServicioInvalidoError(SoftwareFJError):
    """Se lanza cuando los parámetros de un servicio son inválidos."""


class ServicioNoDisponibleError(SoftwareFJError):
    """Se lanza cuando se intenta usar un servicio que no está disponible."""


class ReservaInvalidaError(SoftwareFJError):
    """Se lanza cuando una reserva no puede crearse o procesarse."""


class OperacionNoPermitidaError(SoftwareFJError):
    """Se lanza cuando se pide una transición de estado no permitida."""


class CalculoInconsistenteError(SoftwareFJError):
    """Se lanza cuando un cálculo de costos produce un resultado inválido."""
