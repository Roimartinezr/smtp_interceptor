# launch_server.ps1

Write-Host "`n Iniciando servidor SMTP Python interceptador..." -ForegroundColor Cyan

Write-Host "`nComprobando si hay algun proceso escuchando en el puerto 25..." -ForegroundColor Cyan

# Buscar procesos escuchando en el puerto 25
$connection = Get-NetTCPConnection -LocalPort 25 -State Listen -ErrorAction SilentlyContinue

if ($connection) {
    $SmtpPid = $connection.OwningProcess
    $proc = Get-Process -Id $SmtpPid -ErrorAction SilentlyContinue

    if ($proc) {
        Write-Host "Proceso encontrado: $($proc.Name) (PID: $SmtpPid)" -ForegroundColor Yellow
        try {
            Stop-Process -Id $SmtpPid -Force
            Write-Host "Proceso detenido correctamente." -ForegroundColor Green
        } catch {
            Write-Host "Error al intentar detener el proceso (puede requerir permisos de administrador)." -ForegroundColor Red
        }
    } else {
        Write-Host "El PID $SmtpPid no esta asociado a ningún proceso activo." -ForegroundColor DarkYellow
    }
} else {
    Write-Host "No hay procesos escuchando en el puerto 25. Nada que detener." -ForegroundColor Green
}

# move to server's folder
cd (Split-Path $PSScriptRoot -Parent)

# 1. Comprobar si .venv existe
if (-Not ("$PSScriptRoot\.venv")) {
    Write-Host "Entorno virtual no encontrado. Creando .venv..." -ForegroundColor Yellow
    python -m venv .venv
} else {
    Write-Host "Entorno virtual .venv encontrado." -ForegroundColor Green
}

# 2. Activar entorno virtual
Write-Host "Activando entorno virtual..."
. .\\.venv\\Scripts\\Activate.ps1

# 3. Comprobar dependencias de requirements.txt
try {
    pip check > $null 2>&1
    if ($LASTEXITCODE -ne 0) {
        Write-Host "Instalando dependencias desde requirements.txt..." -ForegroundColor Yellow
        pip install -r requirements.txt
    } else {
        Write-Host "Dependencias ya instaladas." -ForegroundColor Green
    }
} catch {
    Write-Host "Instalando dependencias desde requirements.txt (pip check falló)..." -ForegroundColor Yellow
    pip install -r requirements.txt
}

# 4. Ejecutar servidor SMTP
Write-Host "`nLanzando servidor SMTP..." -ForegroundColor Cyan
python smtp_server.py