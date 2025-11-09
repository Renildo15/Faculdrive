import re

from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from django.core import validators
from django.core.validators import EmailValidator
from rest_framework import serializers

from .validators import *


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        exclude = ["password", "date_joined", "groups", "user_permissions", "last_login"]


class UserStudentRegisterSerializer(serializers.ModelSerializer):
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
