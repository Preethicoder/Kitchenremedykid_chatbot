import asyncio

from celery import Celery


from app.email_utils import send_remedy_email


celery_app = Celery(
    "email_tasks",
    broker="redis://redis:6379/0",
    backend="redis://redis:6379/0"
)

@celery_app.task
def send_remedy_email_task(to_email: str, pdf_path: str):
    asyncio.run(send_remedy_email(to_email, pdf_path))