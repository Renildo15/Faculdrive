from celery import shared_task
from django.core.mail import send_mail

@shared_task
def send_email_reset_password(**kwargs):
    subject = kwargs.get("subject")
    plain_message = kwargs.get("plain_message")
    from_email = kwargs.get("from_email")
    email = kwargs.get("email")
    html_message = kwargs.get("html_message")

    # Verificando se todos os parâmetros necessários foram fornecidos
    if not all([subject, plain_message, from_email, email]):
        raise ValueError("Todos os parâmetros são obrigatórios")

    send_mail(
        subject=subject,
        message=plain_message,
        from_email=from_email,
        recipient_list=[email],
        html_message=html_message,
    )