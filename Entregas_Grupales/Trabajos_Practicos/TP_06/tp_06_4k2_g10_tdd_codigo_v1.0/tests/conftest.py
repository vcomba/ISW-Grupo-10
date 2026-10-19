from datetime import datetime

import pytest

from inscripcion_actividades import (
    RepositorioCuposEnMemoria,
    ServicioInscripcion,
)


class CorreoFalso:
    """Doble de prueba: guarda los mensajes en lugar de enviarlos."""

    def __init__(self):
        self.enviados = []

    def enviar(self, mensaje):
        self.enviados.append(mensaje)


class GeneradorQRFalso:
    """Doble de prueba: devuelve un QR predecible a partir del contenido."""

    def generar(self, contenido):
        return f"QR[{contenido}]".encode()


@pytest.fixture
def cupos():
    return RepositorioCuposEnMemoria()


@pytest.fixture
def correo():
    return CorreoFalso()


@pytest.fixture
def ahora():
    return datetime(2026, 10, 20, 8, 0)


@pytest.fixture
def servicio(cupos, correo, ahora):
    return ServicioInscripcion(cupos, correo, GeneradorQRFalso(),
                               reloj=lambda: ahora)
