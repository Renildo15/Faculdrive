
from django.http import FileResponse, Http404
from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser
from rest_framework.decorators import api_view, permission_classes, parser_classes
from rest_framework.parsers import MultiPartParser
from rest_framework.response import Response
from file_app.models import Archive, Tag, Review
from file_app.serializers import ArchiveSerializer, CreateArchiveSerializer, TagSerializer, CreateTagSerializer, CreateReviewSerializer, ReviewSerializer
from file_app.tasks import process_archive_task
from django.db.models import Avg
# Create your views here.
#
@api_view(["GET"])
@permission_classes([IsAdminUser])
def list_all_archives_view(request):
    archives = Archive.objects.all().order_by("upload_at")
    serializer = ArchiveSerializer(archives, many=True)

    data = {"archives": serializer.data}

    return Response(data, status=status.HTTP_200_OK)

@api_view(["GET"])
@permission_classes([AllowAny])
def list_only_public_archives_view(request):
    archives = Archive.objects.filter(is_public=True).order_by("upload_at")
    serializer = ArchiveSerializer(archives, many=True)

    data = {"archives": serializer.data}
    return Response(data, status=status.HTTP_200_OK)


@extend_schema(
    request={
        "multipart/form-data": CreateArchiveSerializer
    },
    responses={201: ArchiveSerializer}
)
@api_view(["POST"])
@permission_classes([IsAuthenticated])
@parser_classes([MultiPartParser])
def create_archive_view(request):
    serializer = CreateArchiveSerializer(data=request.data)
    if serializer.is_valid():
        archive = serializer.save(user=request.user)

        process_archive_task.delay(archive.id)
        return Response(data=serializer.data, status=status.HTTP_201_CREATED)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(["GET"])
@permission_classes([AllowAny])
def get_archive_view(request, archive_id):
    archive = get_object_or_404(Archive, id=archive_id)
    if not archive.is_public and not request.user.is_staff:
        return Response(data={"message": "Você não tem permissão para acessar este arquivo."}, status=status.HTTP_403_FORBIDDEN)
    serializer = ArchiveSerializer(archive)

    return Response({"archive": serializer.data}, status=status.HTTP_200_OK)

@api_view(["GET"])
@permission_classes([IsAuthenticated])
def dowload_archive_view(request, archive_id):
    try:
        archive = Archive.objects.get(id=archive_id)
    except Archive.DoesNotExist:
        raise Http404("Arquivo não encontrado.")

    if not archive.is_public and not request.user.is_staff:
        return Response(data={"message": "Você não tem permissão para acessar este arquivo."}, status=status.HTTP_403_FORBIDDEN)

    if not archive.file:
        raise Http404("Arquivo não disponível.")

    return FileResponse(archive.file.open('rb'), as_attachment=True, filename=archive.file.name)

@api_view(["DELETE"])
@permission_classes([IsAuthenticated])
def delete_archive_view(request, archive_id):
    archive = get_object_or_404(Archive, id=archive_id)
    if archive.user != request.user:
        return Response(data={"message": "Você não tem permissão para acessar este arquivo."}, status=status.HTTP_403_FORBIDDEN)
    if archive.file:
        archive.file.delete(save=False)
    archive.delete()

    return Response(status=status.HTTP_204_NO_CONTENT)

@api_view(["PATCH"])
@permission_classes([IsAuthenticated])
def update_archive_view(request, archive_id):
    archive = get_object_or_404(Archive, id=archive_id)
    if archive.user != request.user:
        return Response(data={"message": "Você não tem permissão para acessar este arquivo."}, status=status.HTTP_403_FORBIDDEN)
    serializer = CreateArchiveSerializer(archive, data=request.data, partial=True)

    if serializer.is_valid():
        serializer.save()
        data = {"message": "Arquivo atualizado com sucesso!"}
        return Response(data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@extend_schema(
    request=CreateTagSerializer,
    responses={201: TagSerializer}
)
@api_view(["POST"])
@permission_classes([IsAuthenticated])
def create_tag_view(request):
    serializer = CreateTagSerializer(data=request.data)
    if request.user.is_staff:
        return Response(data={"message": "Você não tem permissão para está ação."}, status=status.HTTP_403_FORBIDDEN)
    if serializer.is_valid():
        serializer.save()

        return Response(data=serializer.data, status=status.HTTP_201_CREATED)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@extend_schema(
    responses={200: TagSerializer}
)
@api_view(["GET"])
@permission_classes([AllowAny])
def list_all_tags_view(request):
    tags = Tag.objects.all()
    serializer = TagSerializer(tags, many=True)

    data = {"tags": serializer.data}
    return Response(data, status=status.HTTP_200_OK)



@extend_schema(
    request=CreateReviewSerializer,
    responses={201: ReviewSerializer}
)
@api_view(["POST"])
@permission_classes([IsAuthenticated])
def create_review_view(request, archive_id):
    archive = get_object_or_404(Archive, id=archive_id)
    user = request.user


    if Review.objects.filter(archive=archive, user=user).exists():
        return Response(
            {"message": "Você já avaliou este arquivo."},
            status=status.HTTP_400_BAD_REQUEST
        )

    serializer = CreateReviewSerializer(data=request.data)

    if serializer.is_valid():
        serializer.save(archive=archive, user=user)

        return Response(
            {"message": "Avaliação adicionada!"},
            status=status.HTTP_201_CREATED
        )
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(["GET"])
@permission_classes([AllowAny])
def get_reviews_view(request, archive_id):
    reviews = Review.objects.filter(archive_id=archive_id)
    serializer = ReviewSerializer(reviews, many=True)

    avg_stars = reviews.aggregate(avg_stars=Avg("stars"))["avg_stars"]

    return Response(
        {
            "reviews": serializer.data,
            "average": avg_stars if avg_stars else 0
        },
        status=status.HTTP_200_OK
    )