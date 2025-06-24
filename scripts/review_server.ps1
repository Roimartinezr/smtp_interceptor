Write-Host "`n== Comprobando si el servidor SMTP esta levantado (puerto 25) ==`n"

$salida = netstat -ano | findstr ":25"

if ($salida) {
    Write-Host "Proceso escuchando en el puerto 25:"
    $salida
} else {
    Write-Host "No hay ningun proceso escuchando en el puerto 25."
}

pause