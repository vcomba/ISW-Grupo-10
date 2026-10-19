from datetime import datetime

from inscripcion_actividades import Visitante

MIERCOLES_10 = datetime(2026, 10, 21, 10, 0)


def datos_validos(**cambios):
    """Solicitud que cumple todos los criterios; cada prueba cambia uno."""
    datos = {
        "actividad": "Safari",
        "horario": MIERCOLES_10,
        "cantidad_personas": 1,
        "visitantes": [Visitante("Ana Perez", "30123456", 25)],
        "acepta_terminos": True,
        "correo": "ana@mail.com",
    }
    datos.update(cambios)
    return datos


def grupo(cantidad):
    return [Visitante(f"Visitante {i}", f"3000000{i}", 30)
            for i in range(cantidad)]
