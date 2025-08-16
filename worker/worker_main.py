import asyncio
from worker.emails.rabbitmq import RabbitMQHandler

if __name__ == "__main__":
    rabbit = RabbitMQHandler()
    asyncio.run(rabbit.consume())
    print("\n[*] Worker is launching")
