import re

from rest_framework import serializers


def validate_first_name(first_name):
    if len(first_name) < 3:
        raise serializers.ValidationError(
            "First name must be at least 3 characters long"
        )
    return first_name


def validate_last_name(last_name):
    if len(last_name) < 3:
        raise serializers.ValidationError(
            "Last name must be at least 3 characters long"
        )
    return last_name


def validate_username(username):
    if len(username) < 3:
        raise serializers.ValidationError("Username must be at least 3 characters long")
    return username
