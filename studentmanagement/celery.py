from celery import Celery

import os

os.environ.setdefault(
    "DJANGO_SETTINGS_MODULE",
    "studentmanagement.settings"
)

app = Celery("studentmanagement")

app.config_from_object(
    "django.conf:settings",
    namespace="CELERY"
)

app.autodiscover_tasks()