"""Clase Reserva: integra cliente, servicio, duración y estado."""
from cliente import Cliente
from entidad import Entidad
from excepciones import (CalculoInconsistenteError, OperacionNoPermitidaError,
                         ReservaInvalidaError, ServicioInvalidoError,
                         ServicioNoDisponibleError, SoftwareFJError)
from logger_config import obtener_logger
from servicios import Servicio

log = obtener_logger()  #logger compartido del sistema


class Reserva(Entidad):
    """Reserva con ciclo de vida: PENDIENTE -> CONFIRMADA -> PROCESADA (o CANCELADA)."""

    def __init__(self, cliente, servicio, horas) -> None:
        super().__init__()
        #Se validan los tipos antes de aceptar la reserva
        if not isinstance(cliente, Cliente):
            raise ReservaInvalidaError("La reserva requiere un Cliente válido")
        if not isinstance(servicio, Servicio):
            raise ReservaInvalidaError("La reserva requiere un Servicio válido")
        try:
            servicio.validar_parametros(horas)  #la duración la valida el propio servicio
        except ServicioInvalidoError as error:
            #Encadenamiento de excepciones: se conserva la causa original con 'from'
            raise ReservaInvalidaError(f"Duración no válida para la reserva: {horas!r}") from error
        self._cliente = cliente
        self._servicio = servicio
        self._horas = horas
        self._estado = "PENDIENTE"
        self._costo = None  #se llena al procesar

    @property
    def estado(self) -> str:
        return self._estado

    @property
    def costo(self):
        return self._costo

    def confirmar(self) -> bool:
        """Confirma la reserva si está pendiente y el servicio está disponible."""
        try:
            if self._estado != "PENDIENTE":
                raise OperacionNoPermitidaError(
                    f"No se puede confirmar una reserva en estado {self._estado}")
            if not self._servicio.disponible:
                raise ServicioNoDisponibleError(
                    f"El servicio '{self._servicio.nombre}' no está disponible")
        except SoftwareFJError as error:
            log.error("Fallo al confirmar reserva #%s: %s", self.id, error)  #registra el error
            return False
        else:  #solo se ejecuta si no hubo excepción
            self._estado = "CONFIRMADA"
            log.info("Reserva #%s confirmada", self.id)
            return True
        finally:  #siempre se ejecuta
            log.debug("Intento de confirmación finalizado para reserva #%s", self.id)

    def cancelar(self) -> bool:
        """Cancela la reserva si aún no fue procesada ni cancelada."""
        try:
            if self._estado in ("PROCESADA", "CANCELADA"):
                raise OperacionNoPermitidaError(
                    f"No se puede cancelar una reserva en estado {self._estado}")
        except OperacionNoPermitidaError as error:
            log.error("Fallo al cancelar reserva #%s: %s", self.id, error)
            return False
        else:
            self._estado = "CANCELADA"
            log.info("Reserva #%s cancelada", self.id)
            return True
        finally:
            log.debug("Intento de cancelación finalizado para reserva #%s", self.id)

    def procesar(self, impuesto: float = 0.0, descuento: float = 0.0):
        """Procesa una reserva confirmada y calcula su costo final. Devuelve el costo o None."""
        try:
            if self._estado != "CONFIRMADA":
                raise OperacionNoPermitidaError(
                    f"Solo se procesan reservas CONFIRMADAS (estado actual: {self._estado})")
            try:
                costo = self._servicio.calcular_costo(self._horas, impuesto, descuento)
            except CalculoInconsistenteError as error:
                #Se envuelve el error de cálculo en uno de reserva, conservando la causa
                raise ReservaInvalidaError("No fue posible calcular el costo") from error
        except SoftwareFJError as error:
            log.error("Fallo al procesar reserva #%s: %s (causa: %r)",
                      self.id, error, error.__cause__)
            return None
        else:
            self._costo = costo
            self._estado = "PROCESADA"
            log.info("Reserva #%s procesada. Costo: $%s", self.id, f"{costo:,.2f}")
            return costo
        finally:
            log.debug("Intento de procesamiento finalizado para reserva #%s", self.id)

    def describir(self) -> str:
        costo = f"${self._costo:,.2f}" if self._costo is not None else "sin calcular"
        return (f"Reserva #{self.id} | {self._cliente.nombre} | {self._servicio.nombre} | "
                f"{self._horas} h | {self._estado} | Costo: {costo}")
