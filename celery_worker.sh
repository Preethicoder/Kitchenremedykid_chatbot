#!/bin/sh
celery -A app.tasks.email_tasks worker --loglevel=info

