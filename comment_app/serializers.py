from rest_framework import serializers
from user_app.serializers import UserSerializer
from .models import Comment

class CreateCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ["comment"]


class CommentSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    class Meta:
        model = Comment
        fields = "__all__"