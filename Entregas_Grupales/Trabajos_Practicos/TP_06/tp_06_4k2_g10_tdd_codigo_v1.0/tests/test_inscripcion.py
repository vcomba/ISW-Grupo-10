from datetime import datetime

from inscripcion_actividades.inscripcion import (
    ServicioInscripcion,
    Visitante,
)

MIERCOLES_10 = datetime(2026, 10, 21, 10, 0)


def test_inscripcion_exitosa_con_cupo_horario_datos_y_terminos():
    servicio = ServicioInscripcion()

    inscripcion = servicio.inscribir(
        actividad="Safari",
        horario=MIERCOLES_10,
        cantidad_personas=1,
        visitantes=[Visitante("Ana Perez", "30123456", 25)],
        acepta_terminos=True,
        correo="ana@mail.com",
    )

    assert inscripcion.actividad == "Safari"
    assert inscripcion.horario == MIERCOLES_10
    assert inscripcion.cantidad_personas == 1
