import socket
import dkim

# ==== CONFIGURACIÓN ====
servidor = "127.0.0.1"
puerto = 25
ip_origen = "124.0.0.1"
remitente = "alberto@buenosdias.com"
destinatario = "roi@buenosdias.com"
asunto = "Prueba fallo DKIM"
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

# Clave auténtica (para probar éxito)
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

# Clave errónea (para probar fallo)
clave_privada_f = b"""-----BEGIN PRIVATE KEY-----
MIIEvAIBADANBgkqhkiG9w0BAQEFAASCBKYwggSiAgEAAoIBAQDdhDpvBQjDD2U9
YLW0UXBi4u30G+gzRTPbJA/ZJnv0mATPCNnbV9b0wEhBJCzIWC5eoczmoIsZM0Us
PMznVkRpkoWT8ZME0BmEjGWQXnqKK3MxWSaFoEWc8aZrzaDf9mD1TsiT7vFRFFDz
HMNGWbf7ZhF8a6bvPzB0ymc7139DvAvLVZYYaUvD7osUIFdXwR+KQVx//Hree5f9
S7mEAN+znTJjMZmM1Yl4RXK2bytIC7EUXN5I0YYmVIOfN/AfBv+l09gDuAIG725E
JpI4X4DsYKnl0gsC5QyMbIs/NC8TqYXo7TCPw8/9HstqHy0328MLM5BEAL3afJ3K
c358WSglAgMBAAECggEATHfKciuzOB7W7Ia3gw0/9irvSL7fe99uRL5gqC4UST23
Hz8ncYQTpL7B0pbpzKlALJO/N3gBPIxJ2zkL5OoPSMB3Uzhn75fkzzBmGR28QHk6
VTU4ypUmosR6lilQWS/kjZoKPKMV887HGP17XYw4KlU0QRaqdFmEYTTDyVEdUiRy
EDfaQhQWb6SA89BFrulCc6FOknkkcAIU19U8BedtFJlicwunJvr8YCkHafKyzhFa
3o9TBXtfDC6aLEoA1ep54agLAA5Ggylr6FMZ7pV6gnj4RBloMCNcxiov0z3unEGH
emZdYtWj52n9FxyA9W3HaBzRy8y6q5wfiUxM9lWWCwKBgQD1/98/+GjY81iPHArg
SWr3tzTwjjW9m3JHGtKAbf9hbbrDjAkscNFIZ5Yi/twtSGHAU6HOUnI+Xvxqnn5A
zH7C44YOfyAsODEKjCs/CDe7huVgVMWTkDY8xHaFgcQTb7UJCRKAvJNTUSQChJbF
BDmSCiIzIS88xEf5CwTAKw6zIwKBgQDmhY+H8WlG1APkaubBB7TKQDDcia5a5J+4
RuHZaoR450ZMgPzqTH89eIYsJYQUt7BP1uECLp4wg1i6MhxOHbZ4RD+Ih+wlv3IX
xVKjr4f7QnFfRO6RPdUcSqsym3/TvRMA5SbZbi96Ki3HXLmxDvIK04rWqjirZdj/
DajeexWwFwKBgFiDebPN0QQHA11y7KLpJ9j8DctkkAeqUAMvroBRk+tdjS7hS0e3
TEZuJ0JuS5Drk2idbwIK/lpc2RwP7UOpkQ7UyR6cNVpT2al+5+ylK1CJaC0yM2k2
IZ3Z3v+IwqFvt0cKAaNatvPqpTdWt90p+QEILmgRT6rgwTjl8w6mL4LbAoGAaaDd
qf8WrFvOBMZvQhgT4XEUcpmsCP4lqbzhFEzYssXW0otwWLQAwdwOLwBpy0x4P71I
kUVnOveUmo0Hp0u6JtWu/xK5RHq6/uVt/o8aEinZ5TuizW61zibw11mlcxJ6OLjH
2m3A14uoOmfktpsQkaFpRv/sw60Bh61sqbVgtLUCgYBAvOWWvwZGudBN1CktGGrm
SXHApRd7Ej2Tl/9Z0fIUa9ERf9I3F0I78WPknTaLL2H+nFFuiuI9HjCqv2JSsSrZ
JNGxzT7KLSdiDehir/nVtnOFk7llJ8ZvU0loCal8F2GzNFfEnkNAqbvb0S4jtXvW
0tj8pTryIURGz035rEL3EA==
-----END PRIVATE KEY-----"""

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












