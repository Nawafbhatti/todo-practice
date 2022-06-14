from django.db import models
from django.contrib.auth.models import User

class task(models.Model):
    name = models.CharField(max_length=255)
    title = models.CharField(max_length=255)
    bio = models.CharField(max_length=255)

    user = models.ForeignKey(User, on_delete = models.CASCADE)

    def __str__(self):
        return self.name
