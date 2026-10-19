"""Demo web: formulario que usa ServicioInscripcion."""
from datetime import datetime

import pytest

from inscripcion_actividades import RepositorioCuposEnMemoria
from inscripcion_actividades.web import crear_app


@pytest.fixture
def cliente(correo, generador_qr):
    app = crear_app(cupos=RepositorioCuposEnMemoria(), correo=correo,
                    generador_qr=generador_qr,
                    reloj=lambda: datetime(2026, 10, 20, 8, 0))
    app.testing = True
    return app.test_client()


def formulario(**cambios):
    datos = {
        "actividad": "Safari",
        "fecha": "2026-10-21",
        "hora": "10",
        "cantidad": "1",
        "nombre_0": "Ana Perez",
        "dni_0": "30123456",
        "edad_0": "25",
        "talla_0": "",
        "correo": "ana@mail.com",
        "acepta_terminos": "on",
    }
    datos.update(cambios)
    return {k: v for k, v in datos.items() if v is not None}


def test_la_pagina_principal_muestra_el_formulario_con_las_actividades(
        cliente):
    respuesta = cliente.get("/")

    html = respuesta.get_data(as_text=True)
    assert respuesta.status_code == 200
    for actividad in ("Tirolesa", "Safari", "Palestra", "Jardiner\u00eda"):
        assert actividad in html


def test_inscripcion_valida_muestra_confirmacion_qr_y_correo(
        cliente, correo):
    respuesta = cliente.post("/inscribir", data=formulario())

    html = respuesta.get_data(as_text=True)
    assert respuesta.status_code == 200
    assert "Inscripci\u00f3n confirmada" in html
    assert "data:image/png;base64," in html
    assert "ana@mail.com" in html
    assert len(correo.enviados) == 1


def test_inscripcion_rechazada_muestra_el_motivo(cliente, correo):
    respuesta = cliente.post("/inscribir",
                             data=formulario(acepta_terminos=None))

    html = respuesta.get_data(as_text=True)
    assert respuesta.status_code == 422
    assert "t\u00e9rminos y condiciones" in html
    assert correo.enviados == []


def test_dni_repetido_muestra_el_motivo(cliente, correo):
    respuesta = cliente.post("/inscribir", data=formulario(
        cantidad="2", nombre_1="Juan Gomez", dni_1="30123456", edad_1="30"))

    assert respuesta.status_code == 422
    assert "DNI distinto" in respuesta.get_data(as_text=True)
    assert correo.enviados == []


@pytest.mark.parametrize("campo, valor", [
    ("edad_0", "25.5"), ("edad_0", "-"), ("cantidad", "1e3"),
    ("hora", "25"), ("fecha", "2026-02-30"), ("actividad", "Bungee"),
])
def test_valores_raros_en_el_formulario_se_rechazan(cliente, correo, campo,
                                                    valor):
    respuesta = cliente.post("/inscribir", data=formulario(**{campo: valor}))

    assert respuesta.status_code == 422
    assert correo.enviados == []


def test_formulario_incompleto_muestra_error_sin_romper(cliente):
    respuesta = cliente.post("/inscribir", data=formulario(edad_0="abc"))

    assert respuesta.status_code == 422
    assert "Complet\u00e1" in respuesta.get_data(as_text=True)


def test_si_falla_el_envio_del_correo_se_informa_y_no_se_confirma(
        generador_qr):
    class CorreoCaido:
        def enviar(self, mensaje):
            raise OSError("sin conexion")

    app = crear_app(cupos=RepositorioCuposEnMemoria(), correo=CorreoCaido(),
                    generador_qr=generador_qr,
                    reloj=lambda: datetime(2026, 10, 20, 8, 0))

    respuesta = app.test_client().post("/inscribir", data=formulario())

    assert respuesta.status_code == 502
    assert "correo" in respuesta.get_data(as_text=True)


def test_sin_variables_smtp_se_muestra_vista_previa_del_correo(
        monkeypatch):
    for variable in ("SMTP_HOST", "SMTP_PORT", "SMTP_USER", "SMTP_PASS"):
        monkeypatch.delenv(variable, raising=False)
    cliente = crear_app().test_client()

    respuesta = cliente.post("/inscribir",
                             data=formulario(fecha="2030-01-02"))

    html = respuesta.get_data(as_text=True)
    assert respuesta.status_code == 200
    assert "Modo demostraci" in html
    assert "data:image/png;base64," in html
