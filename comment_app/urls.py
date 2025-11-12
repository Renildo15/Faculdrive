from django.urls import path
from .views import *

urlpatterns = [
    path("add/<int:archive_id>/", create_comment_view, name="commente_create"),
    path("<int:archive_id>/comments/", get_all_comments, name="commente_create"),
]