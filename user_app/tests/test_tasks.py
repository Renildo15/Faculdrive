import pytest
from unittest.mock import patch
from user_app.tasks import send_email_reset_password


@pytest.mark.django_db
@patch("user_app.tasks.send_mail")
def test_send_email_reset_password(mock_send_mail):
    kwargs = {
        "subject": "Recuperar senha",
        "plain_message": "Seu código é 123456",
        "from_email": "noreply@example.com",
        "email": "user@example.com",
        "html_message": "<p>Seu código é 123456</p>",
    }

    # Executa a task síncrona
    send_email_reset_password(**kwargs)

    mock_send_mail.assert_called_once_with(
        subject=kwargs["subject"],
        message=kwargs["plain_message"],
        from_email=kwargs["from_email"],
        recipient_list=[kwargs["email"]],
        html_message=kwargs["html_message"],
    )
