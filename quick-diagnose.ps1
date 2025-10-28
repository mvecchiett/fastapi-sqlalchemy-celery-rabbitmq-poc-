# Script de Diagnóstico FastAPI POC
Write-Host "=== Diagnóstico FastAPI POC ===" -ForegroundColor Cyan

Set-Location "C:\DesarrolloPOC\fastapi-sqlalchemy-celery-rabbitmq-poc"

Write-Host "`n[1] Verificando Docker..."
docker --version

Write-Host "`n[2] Estado de contenedores..."
docker compose ps

Write-Host "`n[3] Logs del API (últimas 30 líneas)..."
docker compose logs api --tail=30

Write-Host "`n[4] Verificando puerto 8000..."
$port = netstat -ano | Select-String ":8000"
if ($port) {
    Write-Host "Puerto 8000 en uso:" -ForegroundColor Yellow
    Write-Host $port
} else {
    Write-Host "Puerto 8000 disponible" -ForegroundColor Green
}

Write-Host "`n[5] Prueba de health check..."
try {
    $response = Invoke-WebRequest -Uri "http://localhost:8000/health" -TimeoutSec 2
    Write-Host "✓ API respondiendo: $($response.Content)" -ForegroundColor Green
} catch {
    Write-Host "❌ API no responde" -ForegroundColor Red
}

Write-Host "`n=== Acciones Recomendadas ===" -ForegroundColor Cyan
Write-Host "Si los contenedores no están corriendo:"
Write-Host "   docker compose up --build"
Write-Host "`nSi están corriendo pero no responde:"
Write-Host "   docker compose restart api"
Write-Host "   docker compose logs -f api"
