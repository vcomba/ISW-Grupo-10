import io
import smtplib
from email.message import EmailMessage

import qrcode

VARIABLES_SMTP = ("SMTP_HOST", "SMTP_PORT", "SMTP_USER", "SMTP_PASS")


class GeneradorQRPNG:
    """Genera el codigo QR como imagen PNG."""

    def generar(self, contenido):
        imagen = qrcode.make(contenido.encode("utf-8"))
        salida = io.BytesIO()
        imagen.save(salida, format="PNG")
        return salida.getvalue()


class CorreoSMTP:
    """Envia el mensaje por SMTP con STARTTLS y el QR como adjunto."""

    def __init__(self, host, puerto, usuario, clave, remitente=None,
                 smtp=smtplib.SMTP):
        self._host = host
        self._puerto = puerto
        self._usuario = usuario
        self._clave = clave
        self._remitente = remitente or usuario
        self._smtp = smtp

    def enviar(self, mensaje):
        correo = EmailMessage()
        correo["From"] = self._remitente
        correo["To"] = mensaje.destinatario
        correo["Subject"] = mensaje.asunto
        correo.set_content(mensaje.cuerpo)
        correo.add_attachment(mensaje.qr, maintype="image", subtype="png",
                              filename="qr_inscripcion.png")
        with self._smtp(self._host, self._puerto, timeout=15) as servidor:
            servidor.starttls()
            servidor.login(self._usuario, self._clave)
            servidor.send_message(correo)


def correo_desde_entorno(entorno):
    """CorreoSMTP si estan todas las variables SMTP_*; si no, None."""
    if not all(entorno.get(variable) for variable in VARIABLES_SMTP):
        return None
    return CorreoSMTP(entorno["SMTP_HOST"], int(entorno["SMTP_PORT"]),
                      entorno["SMTP_USER"], entorno["SMTP_PASS"],
                      remitente=entorno.get("SMTP_FROM"))
