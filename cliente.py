"""Clase Cliente con validaciones robustas y datos personales encapsulados."""
import re

from entidad import Entidad
from excepciones import ClienteInvalidoError, ParametroFaltanteError

_PATRON_EMAIL = re.compile(r"^[\w.+-]+@[\w-]+(\.[\w-]+)+$")  # formato básico de correo
_PATRON_NOMBRE = re.compile(r"^[A-Za-zÁÉÍÓÚÜÑáéíóúüñ ]{3,60}$")  # solo letras y espacios


class Cliente(Entidad):
    """Cliente de Software FJ. Los atributos son privados y se validan al asignarlos."""

    def __init__(self, nombre=None, documento=None, email=None, telefono=None) -> None:
        super().__init__()  # obtiene el id de la clase base
        # Se verifica primero que no falten parámetros obligatorios
        faltantes = [n for n, v in (("nombre", nombre), ("documento", documento),
                                    ("email", email)) if v is None]
        if faltantes:
            raise ParametroFaltanteError(f"Faltan parámetros del cliente: {', '.join(faltantes)}")
        self.nombre = nombre  # usa el setter con validación
        self.documento = documento
        self.email = email
        self.telefono = telefono

    #nombre
    @property
    def nombre(self) -> str:
        return self._nombre

    @nombre.setter
    def nombre(self, valor: str) -> None:
        if not isinstance(valor, str) or not _PATRON_NOMBRE.match(valor.strip()):
            raise ClienteInvalidoError(f"Nombre inválido: {valor!r}")
        self._nombre = valor.strip()

    #documento
    @property
    def documento(self) -> str:
        return self._documento

    @documento.setter
    def documento(self, valor) -> None:
        texto = str(valor).strip()
        if not texto.isdigit() or not (6 <= len(texto) <= 12):
            raise ClienteInvalidoError(f"Documento inválido (6 a 12 dígitos): {valor!r}")
        self._documento = texto

    #correo
    @property
    def email(self) -> str:
        return self._email

    @email.setter
    def email(self, valor: str) -> None:
        if not isinstance(valor, str) or not _PATRON_EMAIL.match(valor.strip()):
            raise ClienteInvalidoError(f"Correo electrónico inválido: {valor!r}")
        self._email = valor.strip().lower()

    #teléfono
    @property
    def telefono(self):
        return self._telefono

    @telefono.setter
    def telefono(self, valor) -> None:
        if valor is None:  # el teléfono es opcional
            self._telefono = None
            return
        texto = str(valor).strip()
        if not texto.isdigit() or len(texto) != 10:
            raise ClienteInvalidoError(f"Teléfono inválido (10 dígitos): {valor!r}")
        self._telefono = texto

    def describir(self) -> str:
        return f"Cliente #{self.id}: {self._nombre} | Doc: {self._documento} | {self._email}"
