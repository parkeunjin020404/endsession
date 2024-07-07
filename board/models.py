from django.db import models
from member.models import CustomUser

# Create your models here.
class Board(models.Model):
    user = models.ForeignKey(CustomUser, null=True, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    body = models.TextField(default="")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
    
class Comment(models.Model):
    user = models.ForeignKey(CustomUser, null=True, on_delete=models.CASCADE)
    board = models.ForeignKey(Board, related_name='comments', on_delete=models.CASCADE)
    comment = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
