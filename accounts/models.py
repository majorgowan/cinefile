from django.db import models

from django.contrib.auth.models import AbstractUser

# Create your models here.
# custom user
class JUser(AbstractUser):
    # for making user's file private
    private = models.BooleanField(default=False)
    displayname = models.CharField(max_length=32, blank=True)
