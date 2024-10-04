from django.db import models

from django.contrib.auth.models import AbstractUser

# Create your models here.
# custom user
class JUser(AbstractUser):
    # identical to normal User class (for now)
    pass
