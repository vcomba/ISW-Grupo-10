from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen=True)
class Actividad:
    nombre: str
    cupo_maximo: int


CATALOGO = {
    actividad.nombre: actividad
    for actividad in (
        Actividad("Tirolesa", cupo_maximo=10),
        Actividad("Safari", cupo_maximo=8),
        Actividad("Palestra", cupo_maximo=12),
        Actividad("Jardin\u00eda", cupo_maximo=12),
    )
}


class InscripcionError(Exception):
    pass


class ActividadInexistenteError(InscripcionError):
    pass


class SinCupoError(InscripcionError):
    pass


@dataclass
class Visitante:
    nombre: str
    dni: str
    edad: int


@dataclass
class Inscripcion:
    actividad: str
    horario: datetime
    cantidad_personas: int


class RepositorioCuposEnMemoria:
    def __init__(self):
        self._ocupados = {}

    def registrar(self, actividad, horario, cantidad):
        clave = (actividad, horario)
        self._ocupados[clave] = self._ocupados.get(clave, 0) + cantidad

    def ocupados(self, actividad, horario):
        return self._ocupados.get((actividad, horario), 0)


class ServicioInscripcion:
    def __init__(self, cupos):
        self._cupos = cupos

    def inscribir(self, actividad, horario, cantidad_personas, visitantes,
                  acepta_terminos, correo):
        if actividad not in CATALOGO:
            raise ActividadInexistenteError(actividad)
        if self._cupos_disponibles(CATALOGO[actividad], horario) <= 0:
            raise SinCupoError(actividad)
        return Inscripcion(actividad, horario, cantidad_personas)

    def _cupos_disponibles(self, actividad, horario):
        return (actividad.cupo_maximo
                - self._cupos.ocupados(actividad.nombre, horario))
