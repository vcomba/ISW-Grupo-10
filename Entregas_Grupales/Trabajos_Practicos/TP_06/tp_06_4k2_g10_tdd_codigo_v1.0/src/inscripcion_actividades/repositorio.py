class RepositorioCuposEnMemoria:
    """Lugares ocupados por actividad y horario."""

    def __init__(self):
        self._ocupados = {}

    def registrar(self, actividad, horario, cantidad):
        clave = (actividad, horario)
        self._ocupados[clave] = self._ocupados.get(clave, 0) + cantidad

    def ocupados(self, actividad, horario):
        return self._ocupados.get((actividad, horario), 0)
