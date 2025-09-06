import socket

# Configura aquÃ­ tus valores personalizados
servidor = "127.0.0.1"
puerto = 25
ip_origen = "124.0.0.1"
remitente = "alberto@buenosdias.com"
destinatario = "roi@buenosdias.com"
asunto = "jyrdsuinuih"
cuerpo = "llllllllllllllllllllllllllllllll"

# Crear conexiÃ³n TCP
with socket.create_connection((servidor, puerto)) as s:
    def recibir():
        print(s.recv(1024).decode())

    def enviar(comando):
        print(f">>> {comando.strip()}")
        s.sendall((comando + "\r\n").encode())

    recibir()  # banner inicial
    enviar(f"HELO {ip_origen}"); recibir()
    enviar(f"MAIL FROM:<{remitente}>"); recibir()
    enviar(f"RCPT TO:<{destinatario}>"); recibir()
    enviar("DATA"); recibir()

    # Enviar cuerpo completo
    enviar(f"Subject: {asunto}")
    enviar(f"From: {remitente}")
    enviar(f"To: {destinatario}")
    enviar("Content-Type: text/plain; charset=utf-8")
    enviar("")  # lÃ­nea en blanco
    for linea in cuerpo.splitlines():
        enviar(linea)
    enviar("."); recibir()

    enviar("QUIT"); recibir()




























