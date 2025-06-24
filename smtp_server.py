from aiosmtpd.controller import Controller
from email import policy
from email.parser import BytesParser
import requests
import os

BACKEND_URL = os.getenv("MAIL_CAPTURE_URL", "http://localhost:8000/api/smtp")

class MailHandler:

    async def handle_DATA(self, server, session, envelope):
        print("\nMensaje entrante...")

        if not envelope.content:
            print("Error: envelope.content es None.")
            return '550 Error en el contenido del mensaje'

        parser = BytesParser(policy=policy.default)
        message = parser.parsebytes(envelope.content)

        # Cambiar esto en producción, MUY PELIGROSO SI NO
        # ip_origin = session.peer[0]
        ip_origin = getattr(session, "host_name", session.peer[0])
        headers = str(message)

        content = message.get_body(preferencelist=('plain', 'html'))
        body = content.get_content() if content else ""

        print(f"Recibido correo de: {message['From']} para: {message['To']}")

        try:
            response = requests.post(
                BACKEND_URL,
                json={
                    "from_": message['From'],
                    "to": message['To'],
                    "subject": message['Subject'],
                    "body": body,
                    "ip": ip_origin,
                    "headers": headers
                },
                timeout=5
            )
            print(f"Enviado a FastAPI, status {response.status_code}")
        except Exception as e:
            print(f"Error al enviar a FastAPI: {e}")

        return "250 Message accepted for delivery"


if __name__ == "__main__":
    handler = MailHandler()

    controller = Controller(
        handler=handler,
        hostname="localhost",
        port=25
    )

    controller.start()

    print("Servidor SMTP escuchando en puerto 25")
    input("Presiona ENTER para detener...\n")
    controller.stop()
