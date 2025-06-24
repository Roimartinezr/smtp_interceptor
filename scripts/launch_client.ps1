# Ruta al archivo Python (un directorio por encima)
$archivo = "..\smtp_client.py"

# Leer contenido actual del archivo
$contenido = Get-Content $archivo -Raw

# Función auxiliar para hacer reemplazos condicionales
function Reemplazar-SiAplica {
    param (
        [string]$texto,
        [string]$clave,
        [string]$valor
    )
    if (-not [string]::IsNullOrWhiteSpace($valor)) {
        $regex = "$clave\s*=\s*.*"
        return ($texto -replace $regex, "$clave = `"$valor`"")
    }
    return $texto
}

# Pedir datos
$ip_origen    = Read-Host "IP origen (ENTER para no cambiar)"
$remitente    = Read-Host "Remitente (ENTER para no cambiar)"
$destinatario = Read-Host "Destinatario (ENTER para no cambiar)"
$asunto       = Read-Host "Asunto (ENTER para no cambiar)"
$cuerpo       = Read-Host "Cuerpo (ENTER para no cambiar)"

# Aplicar reemplazos solo si hay nuevo valor
$contenido = Reemplazar-SiAplica $contenido "ip_origen"    $ip_origen
$contenido = Reemplazar-SiAplica $contenido "remitente"    $remitente
$contenido = Reemplazar-SiAplica $contenido "destinatario" $destinatario
$contenido = Reemplazar-SiAplica $contenido "asunto"       $asunto
$contenido = Reemplazar-SiAplica $contenido "cuerpo"       $cuerpo

# Guardar cambios
Set-Content -Path $archivo -Value $contenido -Encoding UTF8

# Ejecutar script

# 1. move to server's folder
cd (Split-Path $PSScriptRoot -Parent)

# 2. Comprobar si .venv existe
if (-Not ("$PSScriptRoot\.venv")) {
    Write-Host "Entorno virtual no encontrado. Creando .venv..." -ForegroundColor Yellow
    python -m venv .venv
} else {
    Write-Host "Entorno virtual .venv encontrado." -ForegroundColor Green
}

# 3. Activar entorno virtual
Write-Host "Activando entorno virtual..."
. .\\.venv\\Scripts\\Activate.ps1

# 4. Ejecutar cliente SMTP
Write-Host "`nLanzando envio de correo..."
python smtp_client.py

Pause
