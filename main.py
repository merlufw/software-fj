"""Simulación de 14 operaciones del sistema Software FJ (sin base de datos).

Ejecutar con:  python main.py
Cada error se captura, se registra en software_fj.log y el programa continúa.
"""
from cliente import Cliente
from excepciones import SoftwareFJError
from logger_config import obtener_logger
from reserva import Reserva
from servicios import AlquilerEquipo, Asesoria, ReservaSala

log = obtener_logger()

# Listas internas que reemplazan a una base de datos
clientes, servicios, reservas = [], [], []


def ejecutar(numero: int, titulo: str, operacion) -> None:
    """Ejecuta una operación de la simulación aislando cualquier error."""
    print(f"\n--- Operación {numero}: {titulo} ---")
    log.info("Operación %s: %s", numero, titulo)
    try:
        resultado = operacion()
    except SoftwareFJError as error:  # errores propios del dominio
        log.error("Operación %s falló: %s (causa: %r)", numero, error, error.__cause__)
        print(f"  [ERROR CONTROLADO] {type(error).__name__}: {error}")
    except Exception as error:  # cualquier error inesperado también se controla
        log.critical("Operación %s: error inesperado: %r", numero, error)
        print(f"  [ERROR INESPERADO] {error!r}")
    else:
        print(f"  [OK] {resultado}")
    finally:
        log.debug("Operación %s finalizada", numero)


# ---- Definición de las operaciones ----
def op_cliente_valido():
    c = Cliente("Ana María Pérez", "1098765432", "ana.perez@correo.com", "3001234567")
    clientes.append(c)
    return c


def op_cliente_correo_invalido():
    return Cliente("Carlos Ruiz", "1012345678", "carlos-sin-arroba")


def op_cliente_sin_documento():
    return Cliente(nombre="Luis Gómez", email="luis@correo.com")  # falta 'documento'


def op_servicio_sala():
    s = ReservaSala("Sala Ejecutiva", 80000, 25)
    servicios.append(s)
    return s


def op_servicio_equipo():
    s = AlquilerEquipo("Proyectores HD", 15000, 4)
    servicios.append(s)
    return s


def op_servicio_asesoria():
    s = Asesoria("Asesoría en Python", 60000, "senior")
    servicios.append(s)
    return s


def op_servicio_tarifa_invalida():
    return Asesoria("Asesoría gratis", -5, "junior")


def op_reserva_exitosa():
    r = Reserva(clientes[0], servicios[0], 3)
    reservas.append(r)
    if not r.confirmar():
        raise RuntimeError("No se pudo confirmar")
    r.procesar(impuesto=0.19, descuento=0.10)  # variante con IVA y descuento
    return r


def op_reserva_duracion_invalida():
    return Reserva(clientes[0], servicios[1], 500)  # supera las 72 h permitidas


def op_reserva_servicio_no_disponible():
    servicios[2].cambiar_disponibilidad(False)
    r = Reserva(clientes[0], servicios[2], 2)
    reservas.append(r)
    return f"confirmada={r.confirmar()} | {r}"  # confirmar() devuelve False y registra el error


def op_procesar_sin_confirmar():
    r = Reserva(clientes[0], servicios[1], 10)
    reservas.append(r)
    return f"costo={r.procesar()} | {r}"  # no está confirmada: operación no permitida


def op_cancelar_dos_veces():
    r = Reserva(clientes[0], servicios[1], 5)
    reservas.append(r)
    primera, segunda = r.cancelar(), r.cancelar()
    return f"primera={primera}, segunda={segunda}"


def op_calculo_inconsistente():
    r = Reserva(clientes[0], servicios[1], 4)
    reservas.append(r)
    r.confirmar()
    costo = r.procesar(impuesto=0.19, descuento=1.5)  # descuento imposible
    return f"costo={costo} | {r}"


def op_reserva_tipo_incorrecto():
    return Reserva("no soy un cliente", servicios[0], 2)


def main() -> None:
    log.info("===== INICIO DE LA SIMULACIÓN =====")
    operaciones = [
        ("Registrar cliente válido", op_cliente_valido),
        ("Registrar cliente con correo inválido", op_cliente_correo_invalido),
        ("Registrar cliente sin documento (parámetro faltante)", op_cliente_sin_documento),
        ("Crear servicio ReservaSala", op_servicio_sala),
        ("Crear servicio AlquilerEquipo", op_servicio_equipo),
        ("Crear servicio Asesoría", op_servicio_asesoria),
        ("Crear asesoría con tarifa inválida", op_servicio_tarifa_invalida),
        ("Reserva exitosa confirmada y procesada", op_reserva_exitosa),
        ("Reserva con duración inválida", op_reserva_duracion_invalida),
        ("Confirmar reserva de servicio no disponible", op_reserva_servicio_no_disponible),
        ("Procesar reserva sin confirmar", op_procesar_sin_confirmar),
        ("Cancelar una reserva dos veces", op_cancelar_dos_veces),
        ("Procesar con descuento inconsistente", op_calculo_inconsistente),
        ("Crear reserva con cliente de tipo incorrecto", op_reserva_tipo_incorrecto),
    ]
    for numero, (titulo, funcion) in enumerate(operaciones, start=1):
        ejecutar(numero, titulo, funcion)

    print("\n=== RESUMEN FINAL (polimorfismo: describir()) ===")
    for entidad in [*clientes, *servicios, *reservas]:
        print(" ", entidad)  # str() llama a describir() de cada clase
    log.info("===== FIN DE LA SIMULACIÓN: el sistema siguió activo =====")


if __name__ == "__main__":
    main()
