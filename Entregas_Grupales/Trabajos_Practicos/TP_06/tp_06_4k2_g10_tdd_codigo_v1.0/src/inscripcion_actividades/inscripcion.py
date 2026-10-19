from dataclasses import dataclass
from datetime import datetime


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
        return Inscripcion(actividad, horario, cantidad_personas)
