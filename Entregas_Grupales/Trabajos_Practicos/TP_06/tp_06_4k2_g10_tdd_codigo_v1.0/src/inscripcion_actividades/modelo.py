import re
from dataclasses import dataclass
from datetime import datetime

from inscripcion_actividades.errores import (
    DatosVisitanteInvalidosError,
    EdadMinimaError,
    TallaRequeridaError,
)

TALLAS = ("XS", "S", "M", "L", "XL", "XXL")
EDAD_MAXIMA = 120
LARGO_NOMBRE = (2, 60)
# Palabras de letras (con acentos) separadas por espacio, apostrofo, guion
# o punto de abreviatura; sin numeros ni simbolos.
FORMATO_NOMBRE = re.compile(r"[^\W\d_]+(?:[ '\-.]+[^\W\d_]+)*\.?")
FORMATO_DNI = re.compile(r"[0-9]{7,8}")


@dataclass(frozen=True)
class Visitante:
    """Persona que participa de la actividad."""

    nombre: str
    dni: str
    edad: int
    talla: str | None = None

    def validar_datos(self):
        minimo, maximo = LARGO_NOMBRE
        nombre = self.nombre.strip()
        if not (minimo <= len(nombre) <= maximo
                and FORMATO_NOMBRE.fullmatch(nombre)):
            raise DatosVisitanteInvalidosError("nombre")
        if not FORMATO_DNI.fullmatch(self.dni):
            raise DatosVisitanteInvalidosError("dni")
        if not 0 <= self.edad <= EDAD_MAXIMA:
            raise DatosVisitanteInvalidosError("edad")


@dataclass(frozen=True)
class Actividad:
    """Actividad del parque con sus requisitos para cada participante."""

    nombre: str
    cupo_maximo: int
    requiere_talla: bool = False
    edad_minima: int = 0

    def validar_participante(self, visitante):
        if self.requiere_talla and visitante.talla not in TALLAS:
            raise TallaRequeridaError(visitante.nombre)
        if visitante.edad < self.edad_minima:
            raise EdadMinimaError(visitante.nombre)


@dataclass(frozen=True)
class Inscripcion:
    actividad: str
    horario: datetime
    cantidad_personas: int
    codigo: str = ""
    visitantes: tuple = ()


@dataclass(frozen=True)
class Mensaje:
    """Correo de confirmacion; qr es la imagen del codigo de inscripcion."""

    destinatario: str
    asunto: str
    cuerpo: str
    qr: bytes


CATALOGO = {
    actividad.nombre: actividad
    for actividad in (
        Actividad("Tirolesa", cupo_maximo=10, requiere_talla=True,
                  edad_minima=8),
        Actividad("Safari", cupo_maximo=8),
        Actividad("Palestra", cupo_maximo=12, requiere_talla=True,
                  edad_minima=12),
        Actividad("Jardiner\u00eda", cupo_maximo=12),
    )
}
