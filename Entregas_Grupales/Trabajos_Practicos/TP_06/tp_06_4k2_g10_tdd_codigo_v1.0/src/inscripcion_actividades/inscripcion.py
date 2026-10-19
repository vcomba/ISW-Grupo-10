from dataclasses import dataclass
from datetime import datetime

ACTIVIDADES = ["Tirolesa", "Safari", "Palestra", "Jardineria"]
CUPO_MAXIMO = {"Tirolesa": 10, "Safari": 8, "Palestra": 12, "Jardineria": 12}


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
        if actividad not in ACTIVIDADES:
            raise ActividadInexistenteError(actividad)
        disponibles = (CUPO_MAXIMO[actividad]
                       - self._cupos.ocupados(actividad, horario))
        if disponibles <= 0:
            raise SinCupoError(actividad)
        return Inscripcion(actividad, horario, cantidad_personas)
