# smtp_interceptor

Servidor SMTP ligero en Python que intercepta correos enviados a `@buenosdias.com` y los reenvía a un backend FastAPI para su procesamiento.

## Uso

0.1. Crear entorno:

```bash
python -m venv .venv
```

0.2. Meterse en el entorno:
```bash
.\.venv\Scripts\activate
```

1. Instala dependencias:

```bash
pip install -r requirements.txt
```

2. Ejecuta el servidor como administrador (para usar el puerto 25) o cambia a otro como 1025:

```bash
python smtp_server.py
```

3. Define la URL del backend con la variable `MAIL_CAPTURE_URL` si no, es `http://localhost:8000/api/capture`.

## Requisitos

- Python 3.8+
- `aiosmtpd`
- `requests`