from rest_framework.permissions import IsAuthenticated, AllowAny
from drf_spectacular.utils import extend_schema
from rest_framework.decorators import api_view, permission_classes
from .serializers import *
from .utils.token import get_tokens_for_user
from rest_framework import status
from rest_framework.response import Response
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.models import User
from .models import Profile
from decouple import config
from .tasks import send_email_reset_password


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


@extend_schema(
    request=UserChangePasswordSerializer,
    responses={200: UserSerializer}
)
@api_view(["PUT"])
@permission_classes([IsAuthenticated])
def change_password_view(request):
    serializer = UserChangePasswordSerializer(data=request.data)

    if serializer.is_valid():
        user = request.user
        user.set_password(serializer.validated_data["new_password"])
        user.save()

        data = {
            "message": "Senha alterada com sucesso.",
            "user": UserSerializer(user).data,
        }
        return Response(data, status=status.HTTP_200_OK)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@extend_schema(
    request={"application/json": {"type": "object", "properties": {"email": {"type": "string", "format": "email"}}}},
    responses={200: {"type": "object", "properties": {"message": {"type": "string"}}}},
)
@api_view(["POST"])
@permission_classes([AllowAny])
def reset_password_request_view(request):
    email = request.data.get("email")
    if not email:
        return Response(
            {"error": "O campo 'email' é obrigatório."},
            status=status.HTTP_400_BAD_REQUEST,
        )
    
    try:
        user = User.objects.get(email=email)
    except User.DoesNotExist:
        return Response(
            {"error": "Usuário com este email não encontrado."},
            status=status.HTTP_404_NOT_FOUND,
        )
    
    token = default_token_generator.make_token(user)
    reset_link = f"http://example.com/reset-password-confirm/?uid={user.pk}&token={token}"
    subject = "Redefinição de senha"
    plain_message = f"Olá {user.first_name},\n\nUse o link abaixo para redefinir sua senha:\n{reset_link}\n\nSe você não solicitou essa alteração, ignore este email."
    from_email = config("EMAIL_HOST_USER")
    email = user.email
    html_message = f"""<p>Olá {user.first_name},</p>
                <p>Use o link abaixo para redefinir sua senha:</p>
                <p><a href="{reset_link}">Redefinir Senha</a></p>
                <p>Se você não solicitou essa alteração, ignore este email.</p>
            """
    send_email_reset_password.delay(
        subject=subject,
        plain_message=plain_message,
        from_email=from_email,
        email=email,
        html_message=html_message,
    )

    return Response(
        {"message": "Instruções para redefinição de senha foram enviadas para o seu email."},
        status=status.HTTP_200_OK,
    )

@extend_schema(
    request=UserResetPasswordConfirmSerializer,
    responses={200: {"type": "object", "properties": {"message": {"type": "string"}}}},
)
@api_view(["POST"])
@permission_classes([AllowAny])
def reset_password_confirm_view(request):
    serializer = UserResetPasswordConfirmSerializer(data=request.data)
    
    if serializer.is_valid():
        email = serializer.validated_data["email"]
        token = serializer.validated_data["token"]

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response(
                {"error": "Usuário com este email não encontrado."},
                status=status.HTTP_404_NOT_FOUND,
            )
        
        if not default_token_generator.check_token(user, token):
            return Response(
                {"error": "Token inválido ou expirado."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        
        user.set_password(serializer.validated_data["new_password"])
        user.save()
        return Response(
            {"message": "Senha redefinida com sucesso."},
            status=status.HTTP_200_OK,
        )
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["PATCH"])
@permission_classes([IsAuthenticated])
def upload_avatar_view(request):
    user = request.user
    profile, created = Profile.objects.get_or_create(user=user)

    avatar = request.FILES.get("avatar")
    if not avatar:
        return Response(
            {"error": "Nenhum arquivo de avatar fornecido."},
            status=status.HTTP_400_BAD_REQUEST,
        )
    
    profile.avatar = avatar
    profile.save()

    return Response(
        {"message": "Avatar atualizado com sucesso."},
        status=status.HTTP_200_OK,
    )


@extend_schema(
    responses={200: UserSerializer}
)
@api_view(["GET"])
@permission_classes([IsAuthenticated])
def who_am_i_view(request):
    user = request.user
    serializer = UserSerializer(user)
    return Response(serializer.data, status=status.HTTP_200_OK)

@extend_schema(
    request=UserUpdateSerializer,
    responses={200: UserSerializer}
)
@api_view(["PUT"])
@permission_classes([IsAuthenticated])
def update_user_view(request):
    user = request.user
    serializer = UserUpdateSerializer(user, data=request.data, partial=True)

    if serializer.is_valid():
        serializer.save()
        return Response(
            {
                "message": "Usuário atualizado com sucesso.",
                "user": UserSerializer(user).data,
            },
            status=status.HTTP_200_OK,
        )
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["DELETE"])
@permission_classes([IsAuthenticated])
def delete_user_view(request):
    user = request.user
    user.delete()
    data = {
        "message": "Usuário deletado com sucesso."
    }

    return Response(data, status=status.HTTP_200_OK)