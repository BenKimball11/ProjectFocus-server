from django.db import models
from django.contrib.auth.models import User


class Super(models.Model):

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    email = models.CharField(max_length=50)
