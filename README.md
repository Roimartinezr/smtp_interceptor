# smtp_interceptor

Servidor SMTP ligero en Python, usando `aiosmtpd` que intercepta correos y los reenvía a un backend para su procesamiento.

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

# Alternativa

También he subido unos scripts en la carpeta `\scripts` para hacer ciertas acciones más sencillas:

1. `launch_server.ps1` 
Lanza el servidor SMTP y lo pone en escucha en el puerto `25`.

2. `review_server.ps1`
Comprueba los procesos que hay en escucha en el puerto `25` de tu equipo.

3. `stop_server.ps1`
El servidor se debe detener desde el script launcher, pero en caso de haber algún problema, se puede ejecutar este.

4. `launch_client.ps1`
Este script envía un correo al servidor, da la opción de cambiar ciertos parámetros, en caso de darle a ENTER, se utilizarán los valores especificados en `smtp_client.py`

## Configuración necesaria

Para utilizar los scripts hay que hacer un pequeño paso extra:

1. Crear una carpeta (recomiendo llamarla `\shortcuts`) en la que almacenar los accesos directos a estos scripts

2. Ir a cada script > "Más opciones" > "Crear acceso directo"

3. En el acceso directo:
Ir a "Propiedades", y ahí, en la opción que pone "Destino", agregar `C:\Windows\System32\WindowsPowerShell\v1.0\powershell.exe -ExecutionPolicy Bypass -File ` antes de la ruta del archivo, la ruta del archivo es IMPORTANTE que debe de entrecomillarse.

4. Dar permisos de administrador
Los accesos directos de los scripts `launch_server` y `stop_server` necesitan también en en "Propiedades" > "Opciones avanzadas" se les espeficique "Ejecutar como administrador"

De esta manera se pueden usar y modificar los scripts