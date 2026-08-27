from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings


@shared_task(bind=True, max_retries=3)
def send_welcome_message(self, name, email):

    try:

        send_mail(
            "Welcome to Our Platform",

            f"""
Hello {name},

Welcome to our platform!

Your registration has been successfully completed.

Regards,
Your Team
""",

            settings.DEFAULT_FROM_EMAIL,
            [email],

            fail_silently=False,
        )

        return f"Email sent to {email}"

    except Exception as exc:
        raise self.retry(
            exc=exc,
            countdown=60
        )