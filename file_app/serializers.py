
from rest_framework import serializers

from file_app.models import Archive, Tag
from user_app.serializers import UserSerializer

class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = "__all__"

class CreateTagSerializer(TagSerializer):
    class Meta(TagSerializer.Meta):
        fields = ["name"]

class CreateArchiveSerializer(serializers.ModelSerializer):
    file = serializers.FileField(required=True)
    tags = TagSerializer(many=True)
    class Meta:
        model = Archive
        fields = ["name_file", "file", "description", "tags"]

    def create(self, validated_data):
        tags_data = validated_data.pop('tags', [])
        archive = Archive.objects.create(**validated_data)
        for tag_data in tags_data:
            tag, _ = Tag.objects.get_or_create(**tag_data)
            archive.tags.add(tag)
        return archive

    def update(self, instance, validated_data):
        tags_data = validated_data.pop("tags", None)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        if tags_data is not None:
            instance.tags.clear()
            for tag_data in tags_data:
                tag, _ = Tag.objects.get_or_create(**tag_data)
                instance.tags.add(tag)

        return instance

class ArchiveSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    tags = TagSerializer(many=True)
    class Meta:
        model = Archive
        fields = "__all__"
