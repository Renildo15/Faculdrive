from django.urls import path
from .views import *

urlpatterns = [
    path("list/all/", list_all_archives_view, name="archives_all"),
    path("list/public/", list_only_public_archives_view, name="archives_public"),
    path("create/", create_archive_view, name="archive_create"),
    path("<int:archive_id>/detail/", get_archive_view, name="archive_detail"),
    path("<int:archive_id>/download/", dowload_archive_view, name="download_file"),
    path("<int:archive_id>/delete/", delete_archive_view, name="archive_delete"),
    path("update/<int:archive_id>/", update_archive_view, name="archive_update"),
    path("create/tag/", create_tag_view, name="tag_create"),
    path("all/tags/", list_all_tags_view, name="tag_all"),
    path("<int:archive_id>/create/review/", create_review_view, name="archive_create_review"),
    path("<int:archive_id>/reviews/", get_reviews_view, name="archive_reviews")
]
