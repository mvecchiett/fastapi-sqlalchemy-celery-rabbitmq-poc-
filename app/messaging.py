import pika
from config import settings

def publish_user_created(email: str):
    try:
        params = pika.URLParameters(settings.rabbit_url)
        connection = pika.BlockingConnection(params)
        channel = connection.channel()
        channel.exchange_declare(exchange='events', exchange_type='topic', durable=True)
        channel.basic_publish(
            exchange='events',
            routing_key='user.created',
            body=email.encode('utf-8'),
            properties=pika.BasicProperties(delivery_mode=2)
        )
        connection.close()
    except Exception as exc:
        # En POC, no romper el flujo si el broker no está listo
        print(f"[WARN] RabbitMQ not available: {exc}")
