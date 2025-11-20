from django.urls import path
from .views import *

urlpatterns = [
    path("register/", register_user_view, name="register_user"),
    path("change-password/", change_password_view, name="change_password"),
    path("reset-password-request/", reset_password_request_view, name="reset_password_request"),
    path("reset-password-confirm/", reset_password_confirm_view, name="reset_password_confirm"),
    path("profile/avatar-upload/", upload_avatar_view, name="upload_avatar"),
    path("whoami/", who_am_i_view, name="who_am_i"),
    path("update/", update_user_view, name="update_user"),
    path("delete/", delete_user_view, name="delete_user"),
]