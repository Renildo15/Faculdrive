from rest_framework.decorators import api_view, permission_classes
from drf_spectacular.utils import extend_schema
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser
from rest_framework import status
from rest_framework.response import Response
from file_app.models import Archive
from rest_framework.pagination import PageNumberPagination
from .serializers import CreateCommentSerializer, CommentSerializer
from .models import Comment

# Create your views here.

class CommentPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = "page_size"


@extend_schema(
    request=CreateCommentSerializer,
    responses={201: CommentSerializer}
)
@api_view(["POST"])
@permission_classes([IsAuthenticated])
def create_comment_view(request, archive_id):
    archive = get_object_or_404(Archive, id = archive_id)
    serializer = CreateCommentSerializer(data=request.data)

    if not archive.is_public:
        return Response(
            {"message": "Você não tem permissão para comentar neste arquivo."},
            status=status.HTTP_403_FORBIDDEN,
        )

    if serializer.is_valid():
        comment = serializer.save(user=request.user, archive=archive)
        data = {"message": "Comentário adicionado!", "comment":CommentSerializer(comment).data}
        return Response(data, status=status.HTTP_201_CREATED)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
@api_view(["GET"])
@permission_classes([AllowAny])
def get_all_comments(request, archive_id):
    archive = get_object_or_404(Archive, id = archive_id)
    comments = Comment.objects.filter(archive=archive).order_by("-created_at")

    paginator = CommentPagination()
    paginated_comments = paginator.paginate_queryset(comments, request)
    serializer = CommentSerializer(paginated_comments, many=True)

    return paginator.get_paginated_response(serializer.data)