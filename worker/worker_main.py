import asyncio
import sentry_sdk
from worker.sentry.config import *
from worker.emails.rabbitmq import RabbitMQHandler

# Initialize Sentry
sentry_sdk.init(
    dsn=DSN_SENTRY,
    environment=ENVIRONMENT,
    traces_sample_rate=1.0,
)

if __name__ == "__main__":
    rabbit = RabbitMQHandler()
    asyncio.run(rabbit.consume())
    print("\n[*] Worker is launching")
