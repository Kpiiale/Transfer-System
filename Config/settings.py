import os
from dotenv import load_dotenv

load_dotenv()

RABBITMQ_HOST = os.getenv("RABBITMQ_HOST", "localhost")
RABBITMQ_PORT = int(os.getenv("RABBITMQ_PORT", 5672))
RABBITMQ_USER = os.getenv("RABBITMQ_USER", "guest")
RABBITMQ_PASSWORD = os.getenv("RABBITMQ_PASSWORD", "guest")

EXCHANGE_DIRECT = "exchange_transactions"
EXCHANGE_FANOUT = "exchange_notifications"
EXCHANGE_TOPIC = "exchange_alerts"

QUEUE_TRANSACTIONS = "queue_transactions"
QUEUE_NOTIFICATIONS = "queue_notifications"
QUEUE_ALERTS = "queue_alerts"
