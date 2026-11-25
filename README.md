# Software FJ – Sistema Integral de Gestión de Clientes, Servicios y Reservas

Curso Programación (213023) – UNAD – Fase 4. Python, sin base de datos ni librerías externas.

## Ejecución
    python main.py
Genera `software_fj.log` con todos los eventos y errores.

## Módulos
| Archivo | Contenido |
|---|---|
| `entidad.py` | Clase abstracta `Entidad` |
| `cliente.py` | `Cliente` con validaciones y encapsulación |
| `servicios.py` | `Servicio` (abstracta) + `ReservaSala`, `AlquilerEquipo`, `Asesoria` |
| `reserva.py` | `Reserva` (confirmar, cancelar, procesar) |
| `excepciones.py` | Excepciones personalizadas |
| `logger_config.py` | Configuración del log |
| `main.py` | Simulación de 14 operaciones (válidas e inválidas) |
