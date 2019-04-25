from __future__ import absolute_import, unicode_literals
from celery import shared_task

from django.core.mail import send_mail
from vehicle import settings

@shared_task
def send_email_async(subject, plain_message, html_message):
    email_from = settings.email_notification_from
    email_to   = settings.email_notification_to
    send_mail(subject, plain_message, email_from, email_to, html_message=html_message)
