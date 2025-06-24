# stop_smtp.ps1
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

Pause
