import pytest
from django.urls import reverse
from django.core.files.uploadedfile import SimpleUploadedFile

@pytest.mark.django_db
def test_upload_avatar_view(api_client, create_user):
    user = create_user()
    api_client.force_authenticate(user=user)

    url = reverse("upload_avatar")
    file = SimpleUploadedFile(
        "avatar.png",
        b"filecontent",
        content_type="image/png"
    )

    response = api_client.patch(url, {"avatar": file}, format='multipart')
    assert response.status_code == 200
    assert response.data["message"] == "Avatar atualizado com sucesso."


@pytest.mark.django_db
def test_who_am_i_view(api_client, create_user):
    user = create_user()
    api_client.force_authenticate(user=user)

    url = reverse("who_am_i")

    response = api_client.get(url)
    assert response.status_code == 200
    assert response.data["username"] == user.username

@pytest.mark.django_db
def test_delete_user_view(api_client, create_user):
    user = create_user()
    api_client.force_authenticate(user=user)

    url = reverse("delete_user")

    response = api_client.delete(url)
    assert response.status_code == 200
    assert response.data["message"] == "Usuário deletado com sucesso."

    # Verify that the user was actually deleted
    with pytest.raises(user.__class__.DoesNotExist):
        user.__class__.objects.get(id=user.id)

@pytest.mark.django_db
def test_delete_user_view_unauthenticated(api_client):
    url = reverse("delete_user")

    response = api_client.delete(url)
    assert response.status_code == 401  # Unauthorized

@pytest.mark.django_db
def test_update_user_view(api_client, create_user):
    user = create_user()
    api_client.force_authenticate(user=user)

    url = reverse("update_user")
    new_data = {
        "first_name": "UpdatedName",
        "last_name": "UpdatedLastName"
    }

    response = api_client.put(url, new_data, format='json')
    assert response.status_code == 200
    assert response.data["message"] == "Usuário atualizado com sucesso."
    assert response.data["user"]["first_name"] == "UpdatedName"
    assert response.data["user"]["last_name"] == "UpdatedLastName"

@pytest.mark.django_db
def test_update_user_view_bad_request(api_client, create_user):
    user = create_user()
    api_client.force_authenticate(user=user)

    url = reverse("update_user")
    bad_data = {
        "email": "not-an-email"
    }

    response = api_client.put(url, bad_data, format='json')
    assert response.status_code == 400

@pytest.mark.django_db
def test_update_user_view_invalid_data(api_client, create_user):
    user = create_user()
    api_client.force_authenticate(user=user)

    url = reverse("update_user")
    invalid_data = {
        "email": "invalidemail"
    }

    response = api_client.put(url, invalid_data, format='json')
    assert response.status_code == 400
    assert "email" in response.data