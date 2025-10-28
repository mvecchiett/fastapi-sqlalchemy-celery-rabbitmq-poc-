# Guía de Troubleshooting - Error "La conexión ha sido reiniciada"

## Diagnóstico del Problema

El error "La conexión ha sido reiniciada" en http://localhost:8000/docs indica que:
- El servidor FastAPI no está corriendo
- El contenedor Docker está fallando
- Hay un problema de configuración

## Pasos de Diagnóstico

### 1. Verificar que Docker Desktop esté corriendo
```bash
docker --version
docker compose version
```

### 2. Verificar estado de los contenedores
```bash
cd C:\DesarrolloPOC\fastapi-sqlalchemy-celery-rabbitmq-poc
docker compose ps
```

**Resultado esperado:** Todos los servicios deben mostrar "Up"
```
NAME                STATUS
adviters_api        Up
adviters_db         Up
adviters_rabbit     Up
adviters_redis      Up
adviters_worker     Up
```

### 3. Ver logs del contenedor API (IMPORTANTE)
```bash
docker compose logs api
```

o para seguir los logs en tiempo real:
```bash
docker compose logs -f api
```

### 4. Si los contenedores no están corriendo
```bash
# Detener todo
docker compose down

# Construir e iniciar
docker compose up --build
```

### 5. Si el contenedor API se está reiniciando constantemente
```bash
# Ver los últimos 50 logs
docker compose logs api --tail=50

# Verificar si hay errores de conexión a la base de datos
docker compose logs api | grep -i error
docker compose logs api | grep -i "connection"
```

## Problemas Comunes y Soluciones

### Problema 1: Puerto 8000 ya está en uso
**Síntoma:** Error "Bind for 0.0.0.0:8000 failed: port is already allocated"

**Solución:**
```bash
# Verificar qué está usando el puerto 8000
netstat -ano | findstr :8000

# Matar el proceso (reemplazar PID con el número que aparece)
taskkill /PID [número] /F

# O cambiar el puerto en docker-compose.yml:
# ports:
#   - "8001:8000"  # Usar puerto 8001 en lugar de 8000
```

### Problema 2: Contenedor de base de datos no está listo
**Síntoma:** Logs muestran "connection refused" o "could not connect to server"

**Solución:**
Agregar health check y depends_on en docker-compose.yml:

```yaml
services:
  api:
    depends_on:
      db:
        condition: service_healthy
  
  db:
    image: postgres:16-alpine
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U app"]
      interval: 5s
      timeout: 5s
      retries: 5
```

### Problema 3: Errores de importación en Python
**Síntoma:** Logs muestran "ModuleNotFoundError" o "ImportError"

**Solución:**
```bash
# Reconstruir la imagen desde cero
docker compose down
docker compose build --no-cache
docker compose up
```

### Problema 4: Variables de entorno no están configuradas
**Síntoma:** Error relacionado con configuración

**Solución:**
Crear archivo `.env` en la raíz del proyecto (aunque docker-compose.yml ya las define):
```
DATABASE_URL=postgresql+psycopg2://app:app@db:5432/app
JWT_SECRET=devsupersecret
REDIS_URL=redis://redis:6379/0
RABBIT_URL=amqp://guest:guest@rabbitmq:5672/
```

### Problema 5: Docker Compose no está actualizado
**Síntoma:** Comando "docker compose" no funciona

**Solución:**
```bash
# Usar docker-compose (con guión) en lugar de docker compose
docker-compose up --build

# O actualizar Docker Desktop a la última versión
```

## Comandos Útiles de Diagnóstico

```bash
# Ver todos los contenedores (incluso detenidos)
docker ps -a

# Ver logs de todos los servicios
docker compose logs

# Entrar al contenedor API para debugging
docker compose exec api /bin/sh

# Verificar conectividad a la base de datos desde el contenedor
docker compose exec api python -c "from database import engine; print(engine.connect())"

# Reiniciar solo el servicio API
docker compose restart api

# Ver uso de recursos
docker stats

# Limpiar todo y empezar de cero
docker compose down -v  # -v elimina los volúmenes
docker compose up --build
```

## Test Manual Rápido

Una vez que los contenedores estén corriendo, probar:

```bash
# 1. Health check
curl http://localhost:8000/health

# 2. Documentación interactiva
# Abrir en navegador: http://localhost:8000/docs

# 3. Registrar usuario de prueba
curl -X POST http://localhost:8000/api/v1/auth/register \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com","password":"Test123!"}'
```

## Script de Diagnóstico Python

Ejecutar el script de diagnóstico:
```bash
cd C:\DesarrolloPOC\fastapi-sqlalchemy-celery-rabbitmq-poc
python diagnose.py
```

## Contacto y Ayuda

Si después de seguir estos pasos el problema persiste:
1. Copia los logs completos: `docker compose logs > logs.txt`
2. Copia el resultado de: `docker compose ps`
3. Comparte esta información para análisis adicional
