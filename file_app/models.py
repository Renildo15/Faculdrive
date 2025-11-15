from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator

class Tag(models.Model):
    name = models.CharField(max_length = 200)
    class Meta:
        db_table = "tag"
        verbose_name = "Tag"
        verbose_name_plural = "Tags"

    def __str__(self):
        return f"{self.name}"
# Create your models here.
class Archive(models.Model):
    name_file = models.CharField(max_length = 200)
    description = models.TextField()
    file = models.FileField(upload_to ='uploads/%Y/%m/%d/')
    is_public = models.BooleanField(default=False)
    processed = models.BooleanField(default=False)
    upload_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

    tags = models.ManyToManyField(Tag, related_name="files")

    class Meta:
        db_table = "archive"
        verbose_name = "Archive"
        verbose_name_plural = "Archives"

    def __str__(self):
        return f"{self.user.username if self.user else 'Sem usuário'} - {self.name_file}"

class Review(models.Model):
    archive = models.ForeignKey(Archive, on_delete=models.CASCADE, related_name="reviews")
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name="reviews")
    stars = models.IntegerField(
        default=0,
        validators=[MinValueValidator(0), MaxValueValidator(5)]
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "review"
        verbose_name = "Review"
        verbose_name_plural = "Reviews"
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.user.username if self.user else 'Sem usuário'} - {self.archive.name_file} - {self.stars}"