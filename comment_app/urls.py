from django.urls import path
from .views import *

urlpatterns = [
    path("add/<int:archive_id>/", create_comment_view, name="comment_create"),
    path("<int:archive_id>/comments/", get_all_comments, name="comment_create"),
    path("<int:comment_id>/reply/", create_reply_comment_view, name="reply_create"),
]