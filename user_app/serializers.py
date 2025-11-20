import re

from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from django.core import validators
from django.core.validators import EmailValidator
from rest_framework import serializers

from .validators import *

class UserChangePasswordSerializer(serializers.Serializer):
    new_password = serializers.CharField(write_only=True)
    confirm_password = serializers.CharField(write_only=True)

    def validate_new_password(self, value: str) -> str:
        """
        Hash value passed by user.

        :param value: password of a user
        :return: a hashed version of the password
        """

        pattern = (
            r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$"
        )

        if not re.match(pattern, value):
            raise serializers.ValidationError(
                "O campo 'new_password' deve conter ao menos 8 caracteres, uma letra maiúscula, uma letra minúscula e um número"
            )
        return value
    
    def validate(self, data):
        """
        Check that the new password and confirm password match.

        :param data: dictionary with new_password and confirm_password
        :return: validated data if passwords match
        """

        new = data.get("new_password")
        confirm = data.get("confirm_password")

        if new is None or confirm is None:
            raise serializers.ValidationError(
                "Os campos 'new_password' e 'confirm_password' são obrigatórios."
            )

        if new != confirm:
            raise serializers.ValidationError(
                {"confirm_password": "As senhas não coincidem."}
            )
        return data

class UserResetPasswordConfirmSerializer(serializers.Serializer):
    email = serializers.EmailField(validators=[EmailValidator])
    token = serializers.CharField()
    new_password = serializers.CharField(write_only=True)
    confirm_password = serializers.CharField(write_only=True)

    def validate_new_password(self, value: str) -> str:
        """
        Hash value passed by user.

        :param value: password of a user
        :return: a hashed version of the password
        """

        pattern = (
            r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$"
        )

        if not re.match(pattern, value):
            raise serializers.ValidationError(
                "O campo 'new_password' deve conter ao menos 8 caracteres, uma letra maiúscula, uma letra minúscula e um número"
            )
        return make_password(value)
    
    def validate(self, data):
        """
        Check that the new password and confirm password match.

        :param data: dictionary with new_password and confirm_password
        :return: validated data if passwords match
        """

        if data["new_password"] != data["confirm_password"]:
            raise serializers.ValidationError(
                {"confirm_password": "As senhas não coincidem."}
            )
        return data
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        exclude = ["password", "date_joined", "groups", "user_permissions", "last_login"]


class UserRegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    def validate_password(self, value: str) -> str:
        """
        Hash value passed by user.

        :param value: password of a user
        :return: a hashed version of the password
        """

        pattern = (
            r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$"
        )

        if not re.match(pattern, value):
            raise serializers.ValidationError(
                "O campo 'password' deve conter ao menos 8 caracteres, uma letra maiúscula, uma letra minúscula e um número"
            )
        return make_password(value)

    email = serializers.EmailField(validators=[EmailValidator])
    first_name = serializers.CharField(validators=[validate_first_name])
    last_name = serializers.CharField(validators=[validate_last_name])
    username = serializers.CharField(validators=[validate_username])

    class Meta:
        model = User
        fields = [
            "first_name",
            "last_name",
            "email",
            "username",
            "password",
        ]

        def create(self, validated_data):
            password = validated_data.pop("password")
            user = User(**validated_data)
            user.set_password(password)
            user.save()

            return user

class UserUpdateSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(validators=[EmailValidator])
    first_name = serializers.CharField(validators=[validate_first_name])
    last_name = serializers.CharField(validators=[validate_last_name])
    username = serializers.CharField(validators=[validate_username])

    class Meta:
        model = User
        fields = [
            "first_name",
            "last_name",
            "email",
            "username",
        ]