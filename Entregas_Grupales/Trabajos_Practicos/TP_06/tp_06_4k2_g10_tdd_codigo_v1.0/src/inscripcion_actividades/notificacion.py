import re
from typing import Protocol

from inscripcion_actividades.errores import CorreoInvalidoError
from inscripcion_actividades.modelo import Mensaje

FORMATO_CORREO = re.compile(r"[^@\s]+@[^@\s]+\.[^@\s]+")


class ServicioCorreo(Protocol):
    def enviar(self, mensaje: Mensaje) -> None: ...


class GeneradorQR(Protocol):
    def generar(self, contenido: str) -> bytes: ...


def validar_correo(direccion):
    if not FORMATO_CORREO.fullmatch(direccion):
        raise CorreoInvalidoError(direccion)


def armar_confirmacion(inscripcion, destinatario, qr):
    nombres = ", ".join(v.nombre for v in inscripcion.visitantes)
    return Mensaje(
        destinatario=destinatario,
        asunto=f"Inscripci\u00f3n confirmada: {inscripcion.actividad}",
        cuerpo=(f"Actividad: {inscripcion.actividad}\n"
                f"Horario: {inscripcion.horario:%d/%m/%Y %H:%M}\n"
                f"Participantes: {nombres}\n"
                f"C\u00f3digo: {inscripcion.codigo}\n"
                "Present\u00e1 el QR adjunto al llegar a la actividad."),
        qr=qr,
    )
