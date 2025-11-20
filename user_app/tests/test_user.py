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