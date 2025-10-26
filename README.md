[![CI](https://github.com/mvecchiett/fastapi-sqlalchemy-celery-rabbitmq-poc-/actions/workflows/ci.yml/badge.svg)](https://github.com/mvecchiett/fastapi-sqlalchemy-celery-rabbitmq-poc-/actions/workflows/ci.yml)

#FastAPI + SQLAlchemy 2.0 + JWT + Celery/Redis + RabbitMQ + Docker + CI

**Qué demuestra este POC**
- API REST en **FastAPI** con **OAuth2/JWT**.
- **SQLAlchemy 2.0** (declarative) + **PostgreSQL**.
- **Celery** sobre **Redis** para tareas en segundo plano.
- Publica `user.created` en **RabbitMQ**.
- **Docker Compose** para levantar todo local.
- **CI** con **GitHub Actions** (lint + tests).

> Nota: Se usa PostgreSQL por simplicidad de stack. Cambiar a SQL Server es factible ajustando `DATABASE_URL` y dependencias (`pyodbc` + ODBC Driver), pero complejiza el contenedor.
> 
## Requisitos
- Docker y Docker Compose.

## Cómo ejecutar
```bash
docker compose up --build
# API en http://localhost:8000/docs
```

## Smoke test rápido
1) **Registrar usuario**
```bash
curl -s -X POST http://localhost:8000/api/v1/auth/register -H "Content-Type: application/json" -d '{"email":"demo@example.com","password":"Secret123!"}'
```
2) **Obtener token**
```bash
curl -s -X POST "http://localhost:8000/api/v1/auth/token" -H "Content-Type: application/x-www-form-urlencoded" -d "username=demo@example.com&password=Secret123!"
```
3) **Consultar perfil (con token)**
```bash
TOKEN=... # pegar access_token
curl -s http://localhost:8000/api/v1/users/me -H "Authorization: Bearer $TOKEN"
```

## Estructura
- `app/` código de la API.
- `app/tasks.py` Celery (ejemplo de tarea `send_welcome_email`).
- RabbitMQ recibe un mensaje `user.created` al registrarse.
- `tests/` prueba simple con `pytest`.
- `.gitlab-ci.yml` pipeline (lint + tests).

## Servicios
- **API**: FastAPI (uvicorn) — http://localhost:8000
- **DB**: PostgreSQL — puerto 5432
- **Redis**: Broker/result Celery — puerto 6379
- **RabbitMQ**: AMQP — puerto 5672; management en http://localhost:15672 (user: guest / pass: guest)

---

## Variables y valores por defecto
Se configuran en `app/config.py` y `docker-compose.yml`:
- `DATABASE_URL=postgresql+psycopg2://app:app@db:5432/app`
- `REDIS_URL=redis://redis:6379/0`
- `RABBIT_URL=amqp://guest:guest@rabbitmq:5672/`

## Link rapidos
- API docs: http://localhost:8000/docs
- RabbitMQ UI: http://localhost:15672 (user/pass: guest / guest)


## Nota sobre seguridad
Este POC es educativo. Para producción: manejo de secrets, HTTPS, rotación de claves, políticas CORS, hardening de contenedores, etc.

