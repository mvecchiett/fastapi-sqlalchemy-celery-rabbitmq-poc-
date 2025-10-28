# Instrucciones personales – FastAPI POC

**Resumen (1 línea)**  
Backend con **FastAPI + JWT**, **Celery/Redis** (tareas), **RabbitMQ** (eventos), **PostgreSQL**, **Docker Compose** y **CI**. Se levanta con `docker compose up` y se prueba en `/docs`.

## Mapa mental
```
Cliente → FastAPI (API + JWT) → PostgreSQL
             │
             ├─ Celery (background jobs) ← Redis (broker/result)
             │
             └─ Evento `user.created` → RabbitMQ (pub/sub)
```

## Arranque
```bash
docker compose up -d      # levantar todo
docker compose ps         # ver api/worker/db/redis/rabbit Up
```
- API docs: http://localhost:8000/docs  
- RabbitMQ UI: http://localhost:15672  (usuario: guest / clave: guest)

## Smoke test (Swagger)
1) `POST /api/v1/auth/register`
```json
{"email":"demo@example.com","password":"Secret123!"}
```
2) `POST /api/v1/auth/token` → copiar `access_token`  
3) Botón **Authorize** (Bearer) → `GET /api/v1/users/me`

## Ver evento en RabbitMQ
1) UI → **Queues** → *Add a new queue*: `test_events`  
2) **Exchanges** → `events` → *Bindings* → **Add**  
   - Queue: `test_events`  
   - Routing key: `user.created`  
3) Repetir el registro → **Queues → test_events → Get messages** (aparece el mensaje).

## Logs útiles
```bash
docker compose logs -f api
docker compose logs -f worker
```

## Rebuild (si cambié dependencias/Dockerfile)
```bash
docker compose up -d --build
# o, más explícito:
docker compose down
docker compose build --no-cache api worker
docker compose up -d
```

## Troubleshooting rápido
- **/docs se cae** → faltan deps comunes:
  - `email-validator`  (por `EmailStr`)
  - `python-multipart` (por `OAuth2PasswordRequestForm`)
  → agregarlas a `requirements.txt` y rebuild.
- **Puerto 8000 ocupado** → cambiar a `8080:8000` en `docker-compose.yml` o matar proceso.
- **Apagar**:
```bash
docker compose down        # mantiene datos
docker compose down -v     # resetea DB/volúmenes
```

## Frases clave (para explicar)
- “Postgres por simplicidad; con SQL Server uso `pyodbc` y cambio `DATABASE_URL`.”
- “Escalado: replico `worker`s de Celery, agrego gateway/ingress y observabilidad.”
- “Seguridad: OAuth2/JWT, CORS, variables de entorno; en prod HTTPS y manejo de secretos.”

## Comandos frecuentes
```bash
docker compose restart api          # reiniciar solo API
docker compose logs --tail=100 api  # últimos logs de API
docker compose exec api sh          # shell dentro de la API
```
