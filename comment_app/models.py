from django.db import models
from django.contrib.auth.models import User
from file_app.models import Archive

# Create your models here.
class Comment(models.Model):
	comment = models.TextField()
	created_at = models.DateTimeField(auto_now_add=True)
	user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
	archive = models.ForeignKey(Archive, on_delete=models.CASCADE, related_name="comments")
	parent = models.ForeignKey(
        "self", on_delete=models.CASCADE, null=True, blank=True, related_name="replies"
    )
	likes = models.ManyToManyField(User, related_name="liked_comments", blank=True)
	class Meta:
		db_table = "comment"
		verbose_name = "Comment"
		verbose_name_plural = "Comments"
		ordering = ["-created_at"]
	def __str__(self):
		return f"{self.user.username if self.user else 'Sem usuário'} - {self.comment}"
	@property
	def likes_count(self):
		return self.likes.count()
	@property
	def is_reply(self):
		return self.parent is not None
