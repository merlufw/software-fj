"""Clase abstracta Servicio y tres servicios especializados (polimorfismo)."""
from abc import abstractmethod

from entidad import Entidad
from excepciones import (CalculoInconsistenteError, ParametroFaltanteError,
                         ServicioInvalidoError)


class Servicio(Entidad):
    """Servicio genérico de Software FJ. Las subclases definen costo, descripción y validación."""

    def __init__(self, nombre=None, tarifa_hora=None) -> None:
        super().__init__()  # id único
        if nombre is None or tarifa_hora is None:
            raise ParametroFaltanteError("Un servicio requiere 'nombre' y 'tarifa_hora'")
        self._nombre = str(nombre).strip()  # nombre del servicio
        self._tarifa_hora = tarifa_hora  # tarifa por hora (se valida abajo)
        self._disponible = True  # por defecto el servicio está disponible
        if not self._nombre:
            raise ServicioInvalidoError("El nombre del servicio no puede estar vacío")
        if not isinstance(tarifa_hora, (int, float)) or tarifa_hora <= 0:
            raise ServicioInvalidoError(f"Tarifa por hora inválida: {tarifa_hora!r}")

    @property
    def nombre(self) -> str:
        return self._nombre

    @property
    def tarifa_hora(self) -> float:
        return self._tarifa_hora

    @property
    def disponible(self) -> bool:
        return self._disponible

    def cambiar_disponibilidad(self, estado: bool) -> None:
        """Activa o desactiva el servicio."""
        self._disponible = bool(estado)

    # ---- métodos abstractos que cada servicio debe sobrescribir ----
    @abstractmethod
    def costo_base(self, horas: float) -> float:
        """Costo sin impuestos ni descuentos para la duración dada."""

    @abstractmethod
    def validar_parametros(self, horas: float) -> None:
        """Valida la duración y las reglas propias del servicio."""

    # ---- método sobrecargado (variantes mediante parámetros opcionales) ----
    def calcular_costo(self, horas: float, impuesto: float = 0.0, descuento: float = 0.0) -> float:
        """Calcula el costo en sus variantes:
        calcular_costo(h)                      -> costo base
        calcular_costo(h, impuesto=0.19)       -> con IVA
        calcular_costo(h, descuento=0.10)      -> con descuento
        calcular_costo(h, 0.19, 0.10)          -> con ambos
        """
        self.validar_parametros(horas)  # polimorfismo: valida según el tipo de servicio
        if not (0 <= impuesto <= 1) or not (0 <= descuento < 1):
            raise CalculoInconsistenteError(
                f"Impuesto ({impuesto}) o descuento ({descuento}) fuera de rango")
        total = self.costo_base(horas) * (1 - descuento) * (1 + impuesto)  # fórmula final
        if total <= 0:
            raise CalculoInconsistenteError(f"Costo calculado inválido: {total}")
        return round(total, 2)

    def describir(self) -> str:
        estado = "disponible" if self._disponible else "NO disponible"
        return f"[{type(self).__name__}] {self._nombre} - ${self._tarifa_hora:,.0f}/h ({estado})"


class ReservaSala(Servicio):
    """Reserva de salas: el costo depende de la capacidad de la sala."""

    def __init__(self, nombre=None, tarifa_hora=None, capacidad=None) -> None:
        super().__init__(nombre, tarifa_hora)
        if not isinstance(capacidad, int) or capacidad <= 0:
            raise ServicioInvalidoError(f"Capacidad de sala inválida: {capacidad!r}")
        self._capacidad = capacidad

    def validar_parametros(self, horas: float) -> None:
        if not isinstance(horas, (int, float)) or not (0 < horas <= 12):
            raise ServicioInvalidoError(f"Una sala se reserva entre 0 y 12 horas, no {horas!r}")

    def costo_base(self, horas: float) -> float:
        recargo = 1.10 if self._capacidad > 20 else 1.0  # 10% extra en salas grandes
        return self._tarifa_hora * horas * recargo

    def describir(self) -> str:
        return super().describir() + f" | Capacidad: {self._capacidad} personas"


class AlquilerEquipo(Servicio):
    """Alquiler de equipos: el costo se multiplica por la cantidad de unidades."""

    def __init__(self, nombre=None, tarifa_hora=None, cantidad=None) -> None:
        super().__init__(nombre, tarifa_hora)
        if not isinstance(cantidad, int) or cantidad <= 0:
            raise ServicioInvalidoError(f"Cantidad de equipos inválida: {cantidad!r}")
        self._cantidad = cantidad

    def validar_parametros(self, horas: float) -> None:
        if not isinstance(horas, (int, float)) or not (0 < horas <= 72):
            raise ServicioInvalidoError(f"Un equipo se alquila entre 0 y 72 horas, no {horas!r}")

    def costo_base(self, horas: float) -> float:
        return self._tarifa_hora * horas * self._cantidad

    def describir(self) -> str:
        return super().describir() + f" | Unidades: {self._cantidad}"


class Asesoria(Servicio):
    """Asesoría especializada: la tarifa sube según el nivel del especialista."""

    _NIVELES = {"junior": 1.0, "senior": 1.5}  # multiplicador por nivel

    def __init__(self, nombre=None, tarifa_hora=None, nivel=None) -> None:
        super().__init__(nombre, tarifa_hora)
        if nivel not in self._NIVELES:
            raise ServicioInvalidoError(f"Nivel de asesor inválido: {nivel!r}")
        self._nivel = nivel

    def validar_parametros(self, horas: float) -> None:
        if not isinstance(horas, (int, float)) or not (0.5 <= horas <= 8):
            raise ServicioInvalidoError(f"Una asesoría dura entre 0.5 y 8 horas, no {horas!r}")

    def costo_base(self, horas: float) -> float:
        return self._tarifa_hora * horas * self._NIVELES[self._nivel]

    def describir(self) -> str:
        return super().describir() + f" | Nivel: {self._nivel}"
