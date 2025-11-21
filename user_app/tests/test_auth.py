import pytest
from django.urls import reverse

@pytest.mark.django_db
def test_register_user_view(api_client):
    url = reverse("register_user")
    data = {
        "username": "newuser",
        "email": "newuser@email.com",
        "password": "Senha123!",
        "first_name": "Renildo",
        "last_name": "Rabi",
    }

    response = api_client.post(url, data, format='json')

    print(response.data)

    assert response.status_code == 201
    assert "access_token" in response.data
    assert "refresh_token" in response.data
    assert response.data["user"]["username"] == data["username"]
    assert response.data["user"]["email"] == data["email"]
    assert response.data["user"]["first_name"] == data["first_name"]
    assert response.data["user"]["last_name"] == data["last_name"]

@pytest.mark.django_db
def test_login(api_client, create_user):
    user = create_user()
    url = reverse("token_obtain_pair")
    data = {
        "username": user.username,
        "password": "pass1234",
    }

    response = api_client.post(url, data, format='json')
    assert response.status_code == 200
    assert "access" in response.data

@pytest.mark.django_db
def test_change_password_view(api_client, create_user):
    user = create_user()
    url = reverse("change_password")
    api_client.force_authenticate(user=user)
    data = {
        "new_password": "Senha123!",
        "confirm_password": "Senha123!",
    }

    response = api_client.put(url, data, format='json')

    print(response.data)

    assert response.status_code == 200
    assert response.data["message"] == "Senha alterada com sucesso."

    # Verify that the password was actually changed
    user.refresh_from_db()
    assert user.check_password(data["new_password"])

@pytest.mark.django_db
def test_reset_password_confirm_view(api_client, create_user):
    user = create_user()
    url_request = reverse("reset_password_request")
    url_confirm = reverse("reset_password_confirm")

    # Step 1: Request password reset
    data_request = {
        "email": user.email,
    }
    response_request = api_client.post(url_request, data_request, format='json')
    assert response_request.status_code == 200
    assert response_request.data["message"] == "Instruções para redefinição de senha foram enviadas para o seu email."

    # Simulate receiving the token (in a real scenario, this would be sent via email)
    from django.contrib.auth.tokens import default_token_generator
    from django.utils.http import urlsafe_base64_encode
    from django.utils.encoding import force_bytes

    uid = urlsafe_base64_encode(force_bytes(user.pk))
    token = default_token_generator.make_token(user)

    # Step 2: Confirm password reset
    data_confirm = {
        "uid": uid,
        "token": token,
        "email": user.email,
        "new_password": "Senha123!",
        "confirm_password": "Senha123!",
    }
    response_confirm = api_client.post(url_confirm, data_confirm, format='json')

    print(response_confirm.data)

    assert response_confirm.status_code == 200
    assert response_confirm.data["message"] == "Senha redefinida com sucesso."

    # Verify that the password was actually changed
    user.refresh_from_db()
    assert user.check_password(data_confirm["new_password"])