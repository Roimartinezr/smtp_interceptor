# launch_server.ps1

Write-Host "`n Iniciando servidor SMTP Python interceptador..." -ForegroundColor Cyan

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

pause