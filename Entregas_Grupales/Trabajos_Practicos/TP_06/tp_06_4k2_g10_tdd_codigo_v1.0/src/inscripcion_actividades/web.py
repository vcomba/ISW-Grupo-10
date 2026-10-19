"""Demo web de la US: formulario de inscripcion sobre ServicioInscripcion."""
import base64
import os
from datetime import date, datetime
from zoneinfo import ZoneInfo

from flask import Flask, render_template, request

from inscripcion_actividades.adaptadores import (
    GeneradorQRPNG,
    correo_desde_entorno,
)
from inscripcion_actividades.calendario import CalendarioParque
from inscripcion_actividades.errores import (
    ActividadInexistenteError,
    CantidadPersonasInvalidaError,
    CorreoInvalidoError,
    DatosVisitanteInvalidosError,
    EdadMinimaError,
    HorarioNoDisponibleError,
    InscripcionError,
    SinCupoError,
    TallaRequeridaError,
    TerminosNoAceptadosError,
)
from inscripcion_actividades.modelo import CATALOGO, TALLAS, Visitante
from inscripcion_actividades.notificacion import armar_confirmacion
from inscripcion_actividades.repositorio import RepositorioCuposEnMemoria
from inscripcion_actividades.servicio import ServicioInscripcion

ZONA_HORARIA = ZoneInfo("America/Argentina/Cordoba")
MAXIMO_PERSONAS = 12

MENSAJES = {
    ActividadInexistenteError: "La actividad elegida no existe.",
    HorarioNoDisponibleError: (
        "El horario elegido no est\u00e1 disponible: el parque est\u00e1 "
        "cerrado (lunes, 25/12 y 1/1), no hay turno en ese horario o el "
        "turno ya comenz\u00f3."),
    CantidadPersonasInvalidaError: (
        "La cantidad de personas debe ser al menos una y coincidir con "
        "los participantes cargados."),
    SinCupoError: (
        "No hay cupos suficientes para esa actividad en el horario "
        "elegido."),
    DatosVisitanteInvalidosError: (
        "Revis\u00e1 los datos de los participantes: el nombre es "
        "obligatorio, el DNI debe tener 7 u 8 d\u00edgitos sin puntos y la "
        "edad debe ser v\u00e1lida."),
    TallaRequeridaError: (
        "Esta actividad requiere indicar el talle de vestimenta de cada "
        "participante."),
    EdadMinimaError: (
        "Alg\u00fan participante no alcanza la edad m\u00ednima de la "
        "actividad."),
    TerminosNoAceptadosError: (
        "Deb\u00e9s aceptar los t\u00e9rminos y condiciones de la "
        "actividad."),
    CorreoInvalidoError: "El correo electr\u00f3nico no es v\u00e1lido.",
}
FORMULARIO_INCOMPLETO = (
    "Complet\u00e1 todos los campos del formulario con valores v\u00e1lidos.")
FALLA_CORREO = (
    "No se pudo enviar el correo de confirmaci\u00f3n, por eso la "
    "inscripci\u00f3n no se registr\u00f3. Intent\u00e1 nuevamente.")

TERMINOS_GENERALES = [
    "El participante declara estar en condiciones f\u00edsicas y de salud "
    "para realizar la actividad.",
    "Debe respetar las indicaciones del personal del parque y las normas "
    "de seguridad.",
    "El parque puede reprogramar o suspender la actividad por clima o "
    "seguridad.",
]
TERMINOS_ESPECIFICOS = {
    "Tirolesa": "Uso obligatorio de arn\u00e9s, casco e indumentaria "
                "provista por el parque. Edad m\u00ednima: 8 a\u00f1os.",
    "Safari": "Prohibido descender del veh\u00edculo y alimentar a los "
              "animales.",
    "Palestra": "Uso obligatorio de arn\u00e9s e indumentaria provista por "
                "el parque. Edad m\u00ednima: 12 a\u00f1os.",
    "Jardiner\u00eda": "Uso de guantes provistos por el parque y de "
                       "herramientas bajo supervisi\u00f3n.",
}


class CorreoNoConfigurado:
    """Sin variables SMTP_*: la demo muestra el correo en pantalla."""

    def enviar(self, mensaje):
        pass


def hora_local():
    return datetime.now(ZONA_HORARIA).replace(tzinfo=None)


def leer_formulario(formulario):
    cantidad = int(formulario["cantidad"])
    visitantes = [
        Visitante(formulario[f"nombre_{i}"].strip(),
                  formulario[f"dni_{i}"].strip(),
                  int(formulario[f"edad_{i}"]),
                  formulario.get(f"talla_{i}") or None)
        for i in range(min(max(cantidad, 0), MAXIMO_PERSONAS))
    ]
    horario = datetime.strptime(
        f"{formulario['fecha']} {formulario['hora']}", "%Y-%m-%d %H")
    return {
        "actividad": formulario["actividad"],
        "horario": horario,
        "cantidad_personas": cantidad,
        "visitantes": visitantes,
        "acepta_terminos": formulario.get("acepta_terminos") == "on",
        "correo": formulario["correo"].strip(),
    }


def crear_app(cupos=None, correo=None, generador_qr=None, reloj=hora_local):
    correo = correo or correo_desde_entorno(os.environ)
    envia_correo = correo is not None
    generador_qr = generador_qr or GeneradorQRPNG()
    calendario = CalendarioParque()
    servicio = ServicioInscripcion(
        cupos or RepositorioCuposEnMemoria(),
        correo or CorreoNoConfigurado(), generador_qr,
        calendario=calendario, reloj=reloj)
    app = Flask(__name__)

    def mostrar_formulario(error=None, valores=None, estado=200):
        contexto = {
            "actividades": list(CATALOGO.values()),
            "tallas": TALLAS,
            "horas": range(calendario.primer_turno,
                           calendario.ultimo_turno + 1),
            "hoy": reloj().date().isoformat(),
            "terminos_generales": TERMINOS_GENERALES,
            "terminos_especificos": TERMINOS_ESPECIFICOS,
            "maximo_personas": MAXIMO_PERSONAS,
            "envia_correo": envia_correo,
            "error": error,
            "valores": dict(valores.items()) if valores else {},
        }
        return render_template("formulario.html", **contexto), estado

    @app.get("/")
    def inicio():
        return mostrar_formulario()

    @app.post("/inscribir")
    def inscribir():
        try:
            datos = leer_formulario(request.form)
        except (KeyError, ValueError):
            return mostrar_formulario(FORMULARIO_INCOMPLETO, request.form,
                                      422)
        try:
            inscripcion = servicio.inscribir(**datos)
        except InscripcionError as error:
            return mostrar_formulario(MENSAJES[type(error)], request.form,
                                      422)
        except OSError:
            return mostrar_formulario(FALLA_CORREO, request.form, 502)
        qr = generador_qr.generar(inscripcion.codigo)
        mensaje = armar_confirmacion(inscripcion, datos["correo"], qr)
        return render_template(
            "confirmacion.html", inscripcion=inscripcion, mensaje=mensaje,
            qr_base64=base64.b64encode(qr).decode(),
            envia_correo=envia_correo, anio=date.today().year)

    return app
