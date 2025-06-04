import asyncio

from celery import Celery


from email_utils import send_remedy_email


celery_app = Celery("email_tasks",
                    broker="redis://localhost:6379/0",  # or use RabbitMQ
                    backend="redis://localhost:6379/0"
                    )

@celery_app.task
def send_remedy_email_task(to_email: str, pdf_path: str):
    asyncio.run(send_remedy_email(to_email, pdf_path))