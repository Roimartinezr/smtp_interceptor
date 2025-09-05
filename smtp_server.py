from aiosmtpd.controller import Controller
from email import policy
from email.parser import BytesParser
import base64, requests, os

BACKEND_URL = os.getenv("MAIL_CAPTURE_URL", "http://localhost:8000/api/smtp")

def _collect_overrides(msg):
    # Prioridad: cabeceras → variables de entorno
    o_ip   = msg.get("X-SPF-IP") or os.getenv("TEST_SPF_IP")
    o_helo = msg.get("X-SPF-HELO") or os.getenv("TEST_SPF_HELO")
    o_mfrom= msg.get("X-SPF-MFROM") or os.getenv("TEST_SPF_MFROM")
    block = {}
    if o_ip:   block["client_ip"] = o_ip.strip().strip("[]")
    if o_helo: block["helo"] = o_helo.strip()
    if o_mfrom:block["mail_from"] = o_mfrom.strip()
    return block if block else None

class MailHandler:

    async def handle_DATA(self, server, session, envelope):
        print("\nMensaje entrante...")

        if not envelope.content:
            print("Error: envelope.content es None.")
            return '550 Error en el contenido del mensaje'

        client_ip = session.peer[0]                 # IP real
        helo      = getattr(session, "host_name", "")
        mail_from = envelope.mail_from
        rcpt_tos  = envelope.rcpt_tos[:]

        raw_bytes = envelope.content
        raw_b64   = base64.b64encode(raw_bytes).decode("ascii")

        message = BytesParser(policy=policy.default).parsebytes(raw_bytes)
        headers_pretty = str(message)
        body = (message.get_body(preferencelist=('plain','html')).get_content()
                if message.get_body(preferencelist=('plain','html')) else "")

        payload = {
            "session": {
                "client_ip": client_ip,
                "helo": helo,
                "mail_from": mail_from,
                "rcpt_tos": rcpt_tos
            },
            "raw_b64": raw_b64,
            "headers_pretty": headers_pretty,
            "body_preview": body
        }
        overrides = _collect_overrides(message)
        if overrides:
            payload["test_override"] = overrides

        print(f"Recibido correo de: {message['From']} para: {message['To']}")

        try:
            response = requests.post(BACKEND_URL, json=payload, timeout=5)
            print(f"Enviado a FastAPI, status {response.status_code}")
        except Exception as e:
            print(f"Error al enviar a FastAPI: {e}")

        return "250 OK"


if __name__ == "__main__":
    controller = Controller(
        MailHandler(),
        hostname="localhost",
        port=25
    )
    controller.start()

    print("Servidor SMTP escuchando en puerto 25")
    input("Presiona ENTER para detener...\n")
    controller.stop()
