from datetime import datetime

import pytest

from inscripcion_actividades import (
    ActividadInexistenteError,
    CantidadPersonasInvalidaError,
    DatosVisitanteInvalidosError,
    HorarioNoDisponibleError,
    RepositorioCuposEnMemoria,
    ServicioInscripcion,
    SinCupoError,
    TallaRequeridaError,
    TerminosNoAceptadosError,
    Visitante,
)

MIERCOLES_10 = datetime(2026, 10, 21, 10, 0)


def datos_validos(**cambios):
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


@pytest.fixture
def cupos():
    return RepositorioCuposEnMemoria()


@pytest.fixture
def servicio(cupos):
    return ServicioInscripcion(cupos)


def test_inscripcion_exitosa_con_cupo_horario_datos_y_terminos(servicio):
    inscripcion = servicio.inscribir(**datos_validos())

    assert inscripcion.actividad == "Safari"
    assert inscripcion.horario == MIERCOLES_10
    assert inscripcion.cantidad_personas == 1


def test_actividad_fuera_del_listado_falla(servicio):
    with pytest.raises(ActividadInexistenteError):
        servicio.inscribir(**datos_validos(actividad="Paracaidismo"))


def test_actividad_sin_cupo_para_el_horario_falla(servicio, cupos):
    cupos.registrar("Safari", MIERCOLES_10, 8)

    with pytest.raises(SinCupoError):
        servicio.inscribir(**datos_validos())


def grupo(cantidad):
    return [Visitante(f"Visitante {i}", f"3000000{i}", 30)
            for i in range(cantidad)]


def test_cantidad_de_personas_que_supera_el_cupo_restante_falla(
        servicio, cupos):
    cupos.registrar("Safari", MIERCOLES_10, 5)

    with pytest.raises(SinCupoError):
        servicio.inscribir(**datos_validos(cantidad_personas=4,
                                           visitantes=grupo(4)))


def test_cantidad_de_personas_igual_al_cupo_restante_pasa(servicio, cupos):
    cupos.registrar("Safari", MIERCOLES_10, 5)

    inscripcion = servicio.inscribir(**datos_validos(cantidad_personas=3,
                                                     visitantes=grupo(3)))

    assert inscripcion.cantidad_personas == 3


@pytest.mark.parametrize("cantidad, visitantes", [
    (0, []),
    (2, grupo(1)),
    (1, grupo(2)),
])
def test_cantidad_de_personas_invalida_falla(servicio, cantidad, visitantes):
    with pytest.raises(CantidadPersonasInvalidaError):
        servicio.inscribir(**datos_validos(cantidad_personas=cantidad,
                                           visitantes=visitantes))


@pytest.mark.parametrize("visitante", [
    Visitante("", "30123456", 25),
    Visitante("   ", "30123456", 25),
    Visitante("Ana Perez", "", 25),
    Visitante("Ana Perez", "30.123.456", 25),
    Visitante("Ana Perez", "123456", 25),
    Visitante("Ana Perez", "301234567", 25),
    Visitante("Ana Perez", "30123456", -1),
    Visitante("Ana Perez", "30123456", 121),
])
def test_datos_del_visitante_incompletos_o_invalidos_falla(
        servicio, visitante):
    with pytest.raises(DatosVisitanteInvalidosError):
        servicio.inscribir(**datos_validos(visitantes=[visitante]))


@pytest.mark.parametrize("horario", [
    datetime(2026, 10, 26, 10, 0),   # lunes: parque cerrado
    datetime(2026, 12, 25, 10, 0),   # navidad: parque cerrado
    datetime(2027, 1, 1, 10, 0),     # anio nuevo: parque cerrado
    datetime(2026, 10, 21, 8, 0),    # antes del primer turno
    datetime(2026, 10, 21, 18, 0),   # no hay turno a las 18
    datetime(2026, 10, 21, 10, 30),  # los turnos empiezan en hora en punto
])
def test_horario_con_parque_cerrado_o_actividad_no_disponible_falla(
        servicio, horario):
    with pytest.raises(HorarioNoDisponibleError):
        servicio.inscribir(**datos_validos(horario=horario))


def test_sin_aceptar_terminos_y_condiciones_falla(servicio):
    with pytest.raises(TerminosNoAceptadosError):
        servicio.inscribir(**datos_validos(acepta_terminos=False))


@pytest.mark.parametrize("actividad", ["Safari", "Jardin\u00eda"])
def test_sin_talle_en_actividad_que_no_lo_requiere_pasa(servicio, actividad):
    visitantes = [Visitante("Ana Perez", "30123456", 25)]

    inscripcion = servicio.inscribir(**datos_validos(actividad=actividad,
                                                     visitantes=visitantes))

    assert inscripcion.actividad == actividad


@pytest.mark.parametrize("actividad", ["Tirolesa", "Palestra"])
def test_sin_talle_requerido_por_la_actividad_falla(servicio, actividad):
    visitantes = [Visitante("Ana Perez", "30123456", 25)]

    with pytest.raises(TallaRequeridaError):
        servicio.inscribir(**datos_validos(actividad=actividad,
                                           visitantes=visitantes))


def test_talle_inexistente_falla(servicio):
    visitantes = [Visitante("Ana Perez", "30123456", 25, talla="XXXL")]

    with pytest.raises(TallaRequeridaError):
        servicio.inscribir(**datos_validos(actividad="Tirolesa",
                                           visitantes=visitantes))


def test_con_talle_en_actividad_que_lo_requiere_pasa(servicio):
    visitantes = [Visitante("Ana Perez", "30123456", 25, talla="M")]

    inscripcion = servicio.inscribir(**datos_validos(actividad="Tirolesa",
                                                     visitantes=visitantes))

    assert inscripcion.actividad == "Tirolesa"
