from rest_framework import serializers
from user_app.serializers import UserSerializer
from .models import Comment

class CreateCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ["comment"]


class CommentSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    replies = serializers.SerializerMethodField()
    class Meta:
        model = Comment
        fields = ["id", "comment", "created_at", "user", "archive", "replies"]

    def get_replies(self, obj):
        replies = obj.replies.all().order_by("created_at")
        return CommentSerializer(replies, many=True).data