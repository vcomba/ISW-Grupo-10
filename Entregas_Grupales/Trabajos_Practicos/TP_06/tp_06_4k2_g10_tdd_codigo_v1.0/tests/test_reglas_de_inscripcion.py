"""Casos de borde de cada criterio de aceptacion, surgidos durante TDD."""
from datetime import datetime

import pytest

from datos_prueba import MIERCOLES_10, datos_validos, grupo
from inscripcion_actividades import (
    ActividadInexistenteError,
    CantidadPersonasInvalidaError,
    CorreoInvalidoError,
    DatosVisitanteInvalidosError,
    EdadMinimaError,
    HorarioNoDisponibleError,
    ServicioInscripcion,
    SinCupoError,
    TallaRequeridaError,
    TerminosNoAceptadosError,
    Visitante,
)


# Criterio: actividad del listado y con cupo para el horario

def test_actividad_fuera_del_listado_falla(servicio):
    with pytest.raises(ActividadInexistenteError):
        servicio.inscribir(**datos_validos(actividad="Paracaidismo"))


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


def test_inscripcion_exitosa_ocupa_los_lugares_del_horario(servicio, cupos):
    servicio.inscribir(**datos_validos(cantidad_personas=3,
                                       visitantes=grupo(3)))

    assert cupos.ocupados("Safari", MIERCOLES_10) == 3


def test_cuando_se_completa_el_cupo_la_siguiente_inscripcion_falla(servicio):
    servicio.inscribir(**datos_validos(cantidad_personas=8,
                                       visitantes=grupo(8)))

    with pytest.raises(SinCupoError):
        servicio.inscribir(**datos_validos())


def test_inscripcion_rechazada_no_ocupa_lugares(servicio, cupos):
    with pytest.raises(TerminosNoAceptadosError):
        servicio.inscribir(**datos_validos(acepta_terminos=False))

    assert cupos.ocupados("Safari", MIERCOLES_10) == 0


# Criterio: horario dentro de los disponibles

@pytest.mark.parametrize("ahora", [
    datetime(2026, 10, 21, 10, 0),   # el turno ya empezo
    datetime(2026, 10, 21, 11, 30),  # el turno ya termino
])
def test_horario_que_ya_comenzo_falla(servicio):
    with pytest.raises(HorarioNoDisponibleError):
        servicio.inscribir(**datos_validos(horario=MIERCOLES_10))


# Criterio: indicar la cantidad de personas

@pytest.mark.parametrize("cantidad, visitantes", [
    (0, []),
    (2, grupo(1)),
    (1, grupo(2)),
])
def test_cantidad_de_personas_invalida_falla(servicio, cantidad, visitantes):
    with pytest.raises(CantidadPersonasInvalidaError):
        servicio.inscribir(**datos_validos(cantidad_personas=cantidad,
                                           visitantes=visitantes))


# Criterio: nombre, DNI, edad y talle de cada persona

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


def test_talle_inexistente_falla(servicio):
    visitantes = [Visitante("Ana Perez", "30123456", 25, talla="XXXL")]

    with pytest.raises(TallaRequeridaError):
        servicio.inscribir(**datos_validos(actividad="Tirolesa",
                                           visitantes=visitantes))


@pytest.mark.parametrize("actividad, edad", [
    ("Tirolesa", 7),
    ("Palestra", 11),
])
def test_visitante_menor_a_la_edad_minima_de_la_actividad_falla(
        servicio, actividad, edad):
    visitantes = [Visitante("Leo Perez", "50123456", edad, talla="S")]

    with pytest.raises(EdadMinimaError):
        servicio.inscribir(**datos_validos(actividad=actividad,
                                           visitantes=visitantes))


@pytest.mark.parametrize("actividad, edad", [
    ("Tirolesa", 8),
    ("Palestra", 12),
    ("Safari", 3),
])
def test_visitante_con_la_edad_minima_de_la_actividad_pasa(
        servicio, actividad, edad):
    visitantes = [Visitante("Leo Perez", "50123456", edad, talla="S")]

    inscripcion = servicio.inscribir(**datos_validos(actividad=actividad,
                                                     visitantes=visitantes))

    assert inscripcion.actividad == actividad


# Criterio: correo con la informacion de la inscripcion y un QR

def test_inscripcion_exitosa_envia_un_correo_con_la_informacion_y_un_qr(
        servicio, correo):
    inscripcion = servicio.inscribir(**datos_validos())

    assert len(correo.enviados) == 1
    mensaje = correo.enviados[0]
    assert mensaje.destinatario == "ana@mail.com"
    assert "Safari" in mensaje.asunto
    assert "Safari" in mensaje.cuerpo
    assert "21/10/2026 10:00" in mensaje.cuerpo
    assert "Ana Perez" in mensaje.cuerpo
    assert inscripcion.codigo in mensaje.cuerpo
    assert mensaje.qr == f"QR[{inscripcion.codigo}]".encode()


def test_inscripcion_rechazada_no_envia_correo(servicio, correo):
    with pytest.raises(TerminosNoAceptadosError):
        servicio.inscribir(**datos_validos(acepta_terminos=False))

    assert correo.enviados == []


@pytest.mark.parametrize("direccion", ["", "ana", "ana@", "@mail.com"])
def test_correo_de_contacto_invalido_falla(servicio, direccion):
    with pytest.raises(CorreoInvalidoError):
        servicio.inscribir(**datos_validos(correo=direccion))


class CorreoCaido:
    def enviar(self, mensaje):
        raise ConnectionError("servidor de correo no disponible")


def test_si_falla_el_envio_del_correo_no_se_ocupan_lugares(
        cupos, generador_qr, ahora):
    servicio = ServicioInscripcion(cupos, CorreoCaido(), generador_qr,
                                   reloj=lambda: ahora)

    with pytest.raises(ConnectionError):
        servicio.inscribir(**datos_validos())

    assert cupos.ocupados("Safari", MIERCOLES_10) == 0
