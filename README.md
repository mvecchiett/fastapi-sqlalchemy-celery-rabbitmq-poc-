![CI](https://github.com/mvecchiett/fastapi-sqlalchemy-celery-rabbitmq-poc-/actions/workflows/ci.yml/badge.svg)

# FastAPI POC — FastAPI + SQLAlchemy 2.0 + JWT + Celery/Redis + RabbitMQ + Docker + CI

POC corto para entrevistas. Demuestra API segura, tareas asíncronas, publicación de eventos y pipeline de CI, todo orquestado con Docker Compose.

## Qué demuestra este POC
- API REST en **FastAPI** con **OAuth2/JWT**.
- **SQLAlchemy 2.0** (declarative) + **PostgreSQL**.
- **Celery** sobre **Redis** para tareas en segundo plano.
- Publica evento **`user.created`** en **RabbitMQ**.
- **Docker Compose** para levantar todo local.
- **CI** con **GitHub Actions** (lint + tests).

## Enlaces rápidos
- API Docs: <http://localhost:8000/docs>
- RabbitMQ UI: <http://localhost:15672> (usuario/clave: `guest` / `guest`)

## Requisitos
- **Docker** y **Docker Compose** instalados.

## Cómo ejecutar
```bash
docker compose up --build
# API en http://localhost:8000/docs
```

## Smoke test rápido
1. **Registrar usuario**
    ```bash
    curl -s -X POST http://localhost:8000/api/v1/auth/register       -H "Content-Type: application/json"       -d '{"email":"demo@example.com","password":"Secret123!"}'
    ```
2. **Obtener token**
    ```bash
    curl -s -X POST http://localhost:8000/api/v1/auth/token       -H "Content-Type: application/x-www-form-urlencoded"       -d "username=demo@example.com&password=Secret123!"
    ```
   Copiá el valor de `access_token` de la respuesta.
3. **Consultar perfil (con token)**
    ```bash
    TOKEN=PEGAR_ACCESS_TOKEN_AQUI
    curl -s http://localhost:8000/api/v1/users/me       -H "Authorization: Bearer $TOKEN"
    ```

## Estructura (resumen)
```
app/
  main.py                 # FastAPI app
  routers/
    auth.py               # /auth/register, /auth/token
    users.py              # /users/me
  models.py               # SQLAlchemy models
  schemas.py              # Pydantic models
  database.py             # Engine/Session
  config.py               # Settings (env vars)
  auth_utils.py           # JWT helpers
  deps.py                 # Depends (db, current_user)
  tasks.py                # Celery task: send_welcome_email
  messaging.py            # Publish event to RabbitMQ
  requirements.txt
  Dockerfile
tests/
  test_smoke.py           # sanity test
.github/workflows/
  ci.yml                  # CI (flake8 + pytest)
docker-compose.yml
requests.http             # Requests para VS Code REST Client
README.md
```

## Servicios y puertos
- API (FastAPI): **http://localhost:8000**
- DB (PostgreSQL): **localhost:5432**
- Redis: **localhost:6379**
- RabbitMQ (AMQP): **localhost:5672**
- RabbitMQ UI: **http://localhost:15672** (guest/guest)

## Notas
- Se usa **PostgreSQL** por simplicidad del stack. Migrar a **SQL Server** es factible cambiando `DATABASE_URL` a `mssql+pyodbc` y agregando el driver ODBC en la imagen (idealmente via multi-stage).  
- Para producción, usar **Alembic** para migraciones y endurecer configuración (secrets, CORS, retries, observabilidad).

## Roadmap breve
- [ ] CRUD `accounts` con paginado/filtros.
- [ ] Tests de integración (API + DB).
- [ ] Observabilidad básica (OpenTelemetry).
- [ ] Helm chart para despliegue en Kubernetes (opcional).
