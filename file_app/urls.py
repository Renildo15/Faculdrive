from django.urls import path
from .views import *

urlpatterns = [
    path("list/all/", list_all_archives_view, name="archives_all"),
    path("list/public/", list_only_public_archives_view, name="archives_public"),
    path("create/", create_archive, name="archive_create"),
    path("detail/<int:archive_id>", get_archive, name="archive_detail"),
    path("download/<int:archive_id>/", dowload_archive_view, name="download_file"),
    path("delete/<int:archive_id>/", delete_archive_view, name="archive_delete"),
    path("update/<int:archive_id>/", update_archive_view, name="archive_update"),
    path("create/tag/", create_tag_view, name="tag_create"),
    path("all/tags/", list_all_tags_view, name="tag_all")
]
