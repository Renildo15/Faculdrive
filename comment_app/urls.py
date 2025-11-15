from django.urls import path
from .views import *

urlpatterns = [
    path("<int:archive_id>/add/", create_comment_view, name="comment_create"),
    path("<int:archive_id>/comments/", get_all_comments, name="comment_create"),
    path("<int:comment_id>/reply/", create_reply_comment_view, name="reply_create"),
    path("<int:comment_id>/delete/", delete_comment_view, name="comment_delete"),
    path("<int:comment_id>/update/", update_comment_view, name="comment_update")
]