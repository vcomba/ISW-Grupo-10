from datetime import datetime

from inscripcion_actividades.calendario import CalendarioParque
from inscripcion_actividades.errores import (
    ActividadInexistenteError,
    CantidadPersonasInvalidaError,
    HorarioNoDisponibleError,
    SinCupoError,
    TerminosNoAceptadosError,
)
from inscripcion_actividades.modelo import CATALOGO, Inscripcion


class ServicioInscripcion:
    def __init__(self, cupos, calendario=CalendarioParque(),
                 catalogo=CATALOGO, reloj=datetime.now):
        self._cupos = cupos
        self._calendario = calendario
        self._catalogo = catalogo
        self._reloj = reloj

    def inscribir(self, actividad, horario, cantidad_personas, visitantes,
                  acepta_terminos, correo):
        elegida = self._buscar_actividad(actividad)
        self._validar_horario(horario)
        self._validar_cantidad(elegida, horario, cantidad_personas,
                               visitantes)
        for visitante in visitantes:
            visitante.validar_datos()
            elegida.validar_participante(visitante)
        if not acepta_terminos:
            raise TerminosNoAceptadosError(actividad)
        return Inscripcion(actividad, horario, cantidad_personas)

    def _buscar_actividad(self, nombre):
        if nombre not in self._catalogo:
            raise ActividadInexistenteError(nombre)
        return self._catalogo[nombre]

    def _validar_horario(self, horario):
        if not self._calendario.turno_disponible(horario):
            raise HorarioNoDisponibleError(horario)
        if horario <= self._reloj():
            raise HorarioNoDisponibleError(horario)

    def _validar_cantidad(self, actividad, horario, cantidad, visitantes):
        if cantidad < 1 or cantidad != len(visitantes):
            raise CantidadPersonasInvalidaError(cantidad)
        if self._cupos_disponibles(actividad, horario) < cantidad:
            raise SinCupoError(actividad.nombre)

    def _cupos_disponibles(self, actividad, horario):
        return (actividad.cupo_maximo
                - self._cupos.ocupados(actividad.nombre, horario))
