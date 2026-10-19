from dataclasses import dataclass
from datetime import datetime

ACTIVIDADES = ["Tirolesa", "Safari", "Palestra", "Jardineria"]


class InscripcionError(Exception):
    pass


class ActividadInexistenteError(InscripcionError):
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


class ServicioInscripcion:
    def inscribir(self, actividad, horario, cantidad_personas, visitantes,
                  acepta_terminos, correo):
        if actividad not in ACTIVIDADES:
            raise ActividadInexistenteError(actividad)
        return Inscripcion(actividad, horario, cantidad_personas)
