from rest_framework.permissions import IsAuthenticated, AllowAny
from drf_spectacular.utils import extend_schema
from rest_framework.decorators import api_view, permission_classes
from .serializers import *
from.utils.token import get_tokens_for_user
from rest_framework import status
from rest_framework.response import Response

# Create your views here.

@extend_schema(
    request=UserRegisterSerializer,
    responses={201: UserSerializer}
)
@api_view(["POST"])
@permission_classes([AllowAny])
def register_user_view(request):
    serializer = UserRegisterSerializer(data=request.data)

    if serializer.is_valid():
        user = serializer.save()
        tokens = get_tokens_for_user(user)

        data = {
            "message": "Usuário registrado",
            "refresh_token": tokens["refresh"],
            "access_token": tokens["access"],
            "user": UserRegisterSerializer(user).data,
        }
        return Response(data, status=status.HTTP_201_CREATED)