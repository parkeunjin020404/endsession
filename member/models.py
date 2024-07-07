from django.db import models
from django.db.models.fields import CharField
from django.contrib.auth.models import AbstractUser
# Create your models here.

class CustomUser(AbstractUser):
    REQUIRED_FIELDS = []
    email = None
    nickname = models.CharField(max_length=100)
    university = models.CharField(max_length=100)

    def __str__(self):
        return self.username
    
