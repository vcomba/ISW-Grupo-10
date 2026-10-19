from dataclasses import dataclass
from datetime import datetime

from inscripcion_actividades.calendario import CalendarioParque


@dataclass(frozen=True)
class Actividad:
    nombre: str
    cupo_maximo: int
    requiere_talla: bool = False


TALLAS = ("XS", "S", "M", "L", "XL", "XXL")

CATALOGO = {
    actividad.nombre: actividad
    for actividad in (
        Actividad("Tirolesa", cupo_maximo=10, requiere_talla=True),
        Actividad("Safari", cupo_maximo=8),
        Actividad("Palestra", cupo_maximo=12, requiere_talla=True),
        Actividad("Jardin\u00eda", cupo_maximo=12),
    )
}


class InscripcionError(Exception):
    pass


class ActividadInexistenteError(InscripcionError):
    pass


class SinCupoError(InscripcionError):
    pass


class HorarioNoDisponibleError(InscripcionError):
    pass


class TerminosNoAceptadosError(InscripcionError):
    pass


class TallaRequeridaError(InscripcionError):
    pass


class CantidadPersonasInvalidaError(InscripcionError):
    pass


@dataclass
class Visitante:
    nombre: str
    dni: str
    edad: int
    talla: str | None = None


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
    def __init__(self, cupos, calendario=CalendarioParque()):
        self._cupos = cupos
        self._calendario = calendario

    def inscribir(self, actividad, horario, cantidad_personas, visitantes,
                  acepta_terminos, correo):
        if actividad not in CATALOGO:
            raise ActividadInexistenteError(actividad)
        if not self._calendario.turno_disponible(horario):
            raise HorarioNoDisponibleError(horario)
        if cantidad_personas < 1 or cantidad_personas != len(visitantes):
            raise CantidadPersonasInvalidaError(cantidad_personas)
        if (self._cupos_disponibles(CATALOGO[actividad], horario)
                < cantidad_personas):
            raise SinCupoError(actividad)
        if not acepta_terminos:
            raise TerminosNoAceptadosError(actividad)
        if CATALOGO[actividad].requiere_talla:
            for visitante in visitantes:
                if visitante.talla not in TALLAS:
                    raise TallaRequeridaError(visitante.nombre)
        return Inscripcion(actividad, horario, cantidad_personas)

    def _cupos_disponibles(self, actividad, horario):
        return (actividad.cupo_maximo
                - self._cupos.ocupados(actividad.nombre, horario))
