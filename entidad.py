"""Clase abstracta que representa las entidades generales del sistema."""
from abc import ABC, abstractmethod
from itertools import count


class Entidad(ABC):
    """Base abstracta toda entidad tiene un identificador único y puede describirse."""

    _contador = count(1)  # generador compartido de identificadores 1, 2, 3...

    def __init__(self) -> None:
        self._id = next(Entidad._contador)  # asigna el siguiente id disponible

    @property
    def id(self) -> int:
        """Identificador de solo lectura (encapsulación)."""
        return self._id

    @abstractmethod
    def describir(self) -> str:
        """Cada entidad concreta debe devolver una descripción en texto."""

    def __str__(self) -> str:
        return self.describir()  # str(entidad) usa la descripción polimórfica
