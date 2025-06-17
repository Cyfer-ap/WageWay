from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings
import csv
import os
from datetime import datetime

def send_dynamic_email(subject, to_email, template_name, context):
    try:
        html_message = render_to_string(template_name, context)
        send_mail(
            subject,
            '',  # plain text
            settings.DEFAULT_FROM_EMAIL,
            [to_email],
            html_message=html_message,
            fail_silently=False,
        )
        log_email_to_csv(to_email, subject, template_name, 'sent')
    except Exception as e:
        log_email_to_csv(to_email, subject, template_name, 'failed', str(e))



LOG_FILE_PATH = os.path.join(settings.BASE_DIR, 'emails', 'logs', 'email_logs.csv')


def log_email_to_csv(to_email, subject, template_name, status, error_message=''):
    os.makedirs(os.path.dirname(LOG_FILE_PATH), exist_ok=True)

    file_exists = os.path.isfile(LOG_FILE_PATH)

    with open(LOG_FILE_PATH, mode='a', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        if not file_exists:
            writer.writerow(['Timestamp', 'Recipient', 'Subject', 'Template', 'Status', 'Error'])

        writer.writerow([
            datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            to_email,
            subject,
            template_name,
            status,
            error_message
        ])


