"""Las seis pruebas de usuario de la US "Inscribirme a actividad"."""
from datetime import datetime

import pytest

from datos_prueba import MIERCOLES_10, datos_validos
from inscripcion_actividades import (
    HorarioNoDisponibleError,
    SinCupoError,
    TallaRequeridaError,
    TerminosNoAceptadosError,
    Visitante,
)


def test_pu1_inscripcion_con_cupo_horario_datos_terminos_y_correo_pasa(
        servicio, correo):
    visitantes = [Visitante("Ana Perez", "30123456", 25, talla="M")]

    inscripcion = servicio.inscribir(**datos_validos(actividad="Tirolesa",
                                                     visitantes=visitantes))

    assert inscripcion.actividad == "Tirolesa"
    assert inscripcion.horario == MIERCOLES_10
    assert inscripcion.cantidad_personas == 1
    assert len(correo.enviados) == 1
    assert correo.enviados[0].destinatario == "ana@mail.com"


def test_pu2_actividad_sin_cupo_para_el_horario_falla(servicio, cupos):
    cupos.registrar("Safari", MIERCOLES_10, 8)

    with pytest.raises(SinCupoError):
        servicio.inscribir(**datos_validos())


@pytest.mark.parametrize("actividad", ["Safari", "Jardiner\u00eda"])
def test_pu3_sin_talle_en_actividad_que_no_lo_requiere_pasa(
        servicio, actividad):
    visitantes = [Visitante("Ana Perez", "30123456", 25)]

    inscripcion = servicio.inscribir(**datos_validos(actividad=actividad,
                                                     visitantes=visitantes))

    assert inscripcion.actividad == actividad


@pytest.mark.parametrize("horario", [
    datetime(2026, 10, 26, 10, 0),   # lunes: parque cerrado
    datetime(2026, 12, 25, 10, 0),   # 25 de diciembre: parque cerrado
    datetime(2027, 1, 1, 10, 0),     # 1 de enero: parque cerrado
    datetime(2026, 10, 21, 8, 0),    # antes del primer turno
    datetime(2026, 10, 21, 18, 0),   # no hay turno a las 18
    datetime(2026, 10, 21, 10, 30),  # los turnos empiezan en hora en punto
])
def test_pu4_horario_con_parque_cerrado_o_actividad_no_disponible_falla(
        servicio, horario):
    with pytest.raises(HorarioNoDisponibleError):
        servicio.inscribir(**datos_validos(horario=horario))


def test_pu5_sin_aceptar_terminos_y_condiciones_falla(servicio):
    with pytest.raises(TerminosNoAceptadosError):
        servicio.inscribir(**datos_validos(acepta_terminos=False))


@pytest.mark.parametrize("actividad", ["Tirolesa", "Palestra"])
def test_pu6_sin_talle_requerido_por_la_actividad_falla(servicio, actividad):
    visitantes = [Visitante("Ana Perez", "30123456", 25)]

    with pytest.raises(TallaRequeridaError):
        servicio.inscribir(**datos_validos(actividad=actividad,
                                           visitantes=visitantes))
