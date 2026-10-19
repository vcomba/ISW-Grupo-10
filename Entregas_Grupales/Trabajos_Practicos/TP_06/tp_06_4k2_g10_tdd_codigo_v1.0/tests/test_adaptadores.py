"""Adaptadores reales de correo (SMTP) y codigo QR (imagen PNG)."""
from inscripcion_actividades import Mensaje
from inscripcion_actividades.adaptadores import (
    CorreoSMTP,
    GeneradorQRPNG,
    correo_desde_entorno,
)

FIRMA_PNG = b"\x89PNG\r\n\x1a\n"


class SMTPFalso:
    """Registra lo que haria smtplib.SMTP sin conectarse a la red."""

    instancias = []

    def __init__(self, host, port, timeout):
        self.host, self.port = host, port
        self.tls = False
        self.login_con = None
        self.enviados = []
        SMTPFalso.instancias.append(self)

    def __enter__(self):
        return self

    def __exit__(self, *args):
        return False

    def starttls(self):
        self.tls = True

    def login(self, usuario, clave):
        self.login_con = (usuario, clave)

    def send_message(self, mensaje):
        self.enviados.append(mensaje)


ENTORNO = {
    "SMTP_HOST": "smtp.gmail.com",
    "SMTP_PORT": "587",
    "SMTP_USER": "ecoharmony@gmail.com",
    "SMTP_PASS": "clave-de-aplicacion",
}


def mensaje_de_prueba():
    return Mensaje(destinatario="ana@mail.com",
                   asunto="Inscripcion confirmada: Safari",
                   cuerpo="Actividad: Safari", qr=FIRMA_PNG + b"datos")


def test_generador_qr_devuelve_una_imagen_png():
    imagen = GeneradorQRPNG().generar("ABC123")

    assert imagen.startswith(FIRMA_PNG)


def test_generador_qr_distinto_contenido_genera_distinta_imagen():
    generador = GeneradorQRPNG()

    assert generador.generar("ABC123") != generador.generar("XYZ789")


def test_correo_smtp_se_autentica_con_tls_y_envia_el_mensaje():
    SMTPFalso.instancias.clear()
    correo = CorreoSMTP("smtp.gmail.com", 587, "eco@gmail.com", "clave",
                        smtp=SMTPFalso)

    correo.enviar(mensaje_de_prueba())

    servidor = SMTPFalso.instancias[0]
    assert (servidor.host, servidor.port) == ("smtp.gmail.com", 587)
    assert servidor.tls
    assert servidor.login_con == ("eco@gmail.com", "clave")
    enviado = servidor.enviados[0]
    assert enviado["To"] == "ana@mail.com"
    assert enviado["Subject"] == "Inscripcion confirmada: Safari"


def test_correo_smtp_adjunta_el_qr_como_imagen_png():
    SMTPFalso.instancias.clear()
    correo = CorreoSMTP("smtp.gmail.com", 587, "eco@gmail.com", "clave",
                        smtp=SMTPFalso)

    correo.enviar(mensaje_de_prueba())

    enviado = SMTPFalso.instancias[0].enviados[0]
    imagenes = [parte for parte in enviado.walk()
                if parte.get_content_type() == "image/png"]
    assert len(imagenes) == 1
    assert imagenes[0].get_content() == FIRMA_PNG + b"datos"


def test_correo_desde_entorno_completo_crea_correo_smtp():
    correo = correo_desde_entorno(ENTORNO)

    assert isinstance(correo, CorreoSMTP)


def test_correo_desde_entorno_incompleto_devuelve_none():
    sin_clave = {k: v for k, v in ENTORNO.items() if k != "SMTP_PASS"}

    assert correo_desde_entorno(sin_clave) is None
