from django.urls import path
from .views import *

urlpatterns = [
    path("list/all/", list_all_archives_view, name="archives_all"),
    path("list/public/", list_only_public_archives_view, name="archives_public"),
    path("create/", create_archive, name="archive_create"),
    path("detail/<int:archive_id>", get_archive, name="archive_detail")
]
