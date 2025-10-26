from celery import Celery
from config import settings

app = Celery(__name__, broker=settings.redis_url, backend=settings.redis_url)

@app.task
def send_welcome_email(email: str):
    # Simula una tarea de envío de correo
    return f"Welcome email sent to {email}"
