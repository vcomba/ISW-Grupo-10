from dataclasses import dataclass
from datetime import datetime

from inscripcion_actividades.errores import (
    DatosVisitanteInvalidosError,
    TallaRequeridaError,
)

TALLAS = ("XS", "S", "M", "L", "XL", "XXL")
EDAD_MAXIMA = 120


@dataclass(frozen=True)
class Visitante:
    nombre: str
    dni: str
    edad: int
    talla: str | None = None

    def validar_datos(self):
        if not self.nombre.strip():
            raise DatosVisitanteInvalidosError("nombre")
        if not (self.dni.isdigit() and 7 <= len(self.dni) <= 8):
            raise DatosVisitanteInvalidosError("dni")
        if not 0 <= self.edad <= EDAD_MAXIMA:
            raise DatosVisitanteInvalidosError("edad")


@dataclass(frozen=True)
class Actividad:
    nombre: str
    cupo_maximo: int
    requiere_talla: bool = False

    def validar_participante(self, visitante):
        if self.requiere_talla and visitante.talla not in TALLAS:
            raise TallaRequeridaError(visitante.nombre)


@dataclass(frozen=True)
class Inscripcion:
    actividad: str
    horario: datetime
    cantidad_personas: int


CATALOGO = {
    actividad.nombre: actividad
    for actividad in (
        Actividad("Tirolesa", cupo_maximo=10, requiere_talla=True),
        Actividad("Safari", cupo_maximo=8),
        Actividad("Palestra", cupo_maximo=12, requiere_talla=True),
        Actividad("Jardin\u00eda", cupo_maximo=12),
    )
}
