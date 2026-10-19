class InscripcionError(Exception):
    """Base de todos los motivos por los que se rechaza una inscripcion."""


class ActividadInexistenteError(InscripcionError):
    pass


class HorarioNoDisponibleError(InscripcionError):
    pass


class CantidadPersonasInvalidaError(InscripcionError):
    pass


class SinCupoError(InscripcionError):
    pass


class DatosVisitanteInvalidosError(InscripcionError):
    pass


class TallaRequeridaError(InscripcionError):
    pass


class TerminosNoAceptadosError(InscripcionError):
    pass
