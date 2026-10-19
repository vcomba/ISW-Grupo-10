from dataclasses import dataclass

LUNES = 0


@dataclass(frozen=True)
class CalendarioParque:
    """Dias de apertura del parque y turnos de una hora de las actividades.

    ultimo_turno es la hora de inicio del ultimo turno (17 a 18 hs).
    """

    dias_cerrados: frozenset = frozenset({LUNES})
    feriados_cerrados: frozenset = frozenset({(12, 25), (1, 1)})
    primer_turno: int = 9
    ultimo_turno: int = 17

    def parque_abierto(self, fecha):
        return (fecha.weekday() not in self.dias_cerrados
                and (fecha.month, fecha.day) not in self.feriados_cerrados)

    def es_turno_valido(self, horario):
        return (self.primer_turno <= horario.hour <= self.ultimo_turno
                and horario.minute == 0 and horario.second == 0)

    def turno_disponible(self, horario):
        return self.parque_abierto(horario) and self.es_turno_valido(horario)
