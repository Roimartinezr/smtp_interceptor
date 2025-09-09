import socket
import dkim

# ==== CONFIGURACIÓN ====
servidor = "127.0.0.1"
puerto = 25
ip_origen = "124.0.0.1"
remitente = "alberto@buenosdias.com"
destinatario = "roi@buenosdias.com"
asunto = "jyrdsuinuih"
cuerpo = "llllllllllllllllllllllllllllllll"

selector = b"mail2025"
dominio = b"buenosdias.com"

# ==== CONSTRUIR MENSAJE ====
mensaje = f"""Subject: {asunto}
From: {remitente}
To: {destinatario}
Content-Type: text/plain; charset=utf-8

{cuerpo}
""".encode()

# ==== FIRMAR CON DKIM ====
clave_privada = b"""-----BEGIN PRIVATE KEY-----
MIICeAIBADANBgkqhkiG9w0BAQEFAASCAmIwggJeAgEAAoGBAN2Af97kJLhYK7TD
/buUNMpkYeLU75ocnB+y+t3E/Y5hECc1IAJ6IL7EoRocThtKZPO9vvBBKR0NaHXe
7VEnymhhEPdM06x4XoW/vqf7nHULbZSt7IbKEyv4qJNjNhcX/qIilTsqiuLBc1QE
29xOeXXr/X55kXk9VpTubFM8oRGHAgMBAAECgYEAiUVEeba7xv7lfy5jReeQW8mg
HDpIjyKh4sdBz0RwutcOcq3qu35CYtdq28qk4SbWr3NtLGnFd/rCPSI9wqi9N5E9
6P/RzB6ZLLaeZ485XDlFhBNfrdRIdmnjPkstPxC0jGYxjsCl/xDuIWTnvt+17xrF
VhltjZJWR5yUW8+I3VECQQD6qfrLbFS6PYY4BvFgM3yvLdSjCIQpdVcSh8ngXlce
+gdAOCVeHY1sUxuBiIF0nUJeJzKlIbRCmSWmB+Ww60avAkEA4jeZI5PBNBh+Svr1
uOV6g+JuRFasv3/094Of8Ig0EDc+TlrPYQ43FzwNm43F+BqFbT9RsXTmcXjjkCWY
pAEYqQJBANvvjxU0DTeISh8YwGtXYbxXKy6Nh2DVCzxAFrqeLDUKzpfja64jofX9
CbJjMqs+XIA+Rmqrov2YYHdIkJnmJhMCQQDHZoquOYeMDCsGnMAMAvtDVUwtINmU
041yv6szsltyD7/0AUfbHVSiPmUgQI/IalhCPBYefhTC4PR2Ey3BItZBAkACo/kQ
j2iQYBtzL5DYGnYM2RmiYAlf0wF+S7B9MvHl6LALqhLgWRk9gwHU7/L+aN0QrYfR
A/AIM6LCmTtT4EZ7
-----END PRIVATE KEY-----
"""

firma = dkim.sign(
    mensaje,
    selector=selector,
    domain=dominio,
    privkey=clave_privada,
    include_headers=[b"from", b"to", b"subject"]
)

mensaje_firmado = firma + mensaje

# ==== ENVÍO SMTP ====
with socket.create_connection((servidor, puerto)) as s:
    def recibir():
        print(s.recv(1024).decode())

    def enviar(linea):
        print(f">>> {linea.strip()}")
        s.sendall((linea + "\r\n").encode())

    recibir()  # Banner inicial
    enviar(f"HELO {ip_origen}"); recibir()
    enviar(f"MAIL FROM:<{remitente}>"); recibir()
    enviar(f"RCPT TO:<{destinatario}>"); recibir()
    enviar("DATA"); recibir()

    # Enviar mensaje firmado línea por línea
    for linea in mensaje_firmado.decode().splitlines():
        enviar(linea)
    enviar("."); recibir()

    enviar("QUIT"); recibir()


