import datetime
from django.db import models
from django.conf import settings


# Create your models here.
class Film(models.Model):
    tmdb = models.IntegerField(unique=True)
    title = models.CharField(max_length=64)
    original_title = models.CharField(max_length=64, blank=True)
    release_date = models.DateField(blank=True)
    year = models.IntegerField()
    director = models.CharField(max_length=32, blank=True)
    starring = models.CharField(max_length=128, blank=True)
    overview = models.CharField(max_length=1024, blank=True)

    def __repr__(self):
        return f"({self.year}) {self.title} [{self.director}]"


class Viewing(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE,
                             related_name="viewings")
    private = models.BooleanField(default=False)
    film = models.ForeignKey(Film, on_delete=models.PROTECT,
                             related_name="viewings")
    date = models.DateField(default=datetime.date.today)
    location = models.CharField(max_length=32, blank=True)
    cinema_or_tv = models.CharField(max_length=7, blank=True)
    video_medium = models.CharField(max_length=9, blank=True)
    tv_channel = models.CharField(max_length=16, blank=True)
    streaming_platform = models.CharField(max_length=16, blank=True)
    cinema = models.CharField(max_length=32, blank=True)
    comments = models.TextField(max_length=4096, blank=True)

    def __repr__(self):
        return f"({self.user}) {self.film.title}"


class ImportedFile(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE,
                             related_name="imports")
    name = models.CharField(max_length=255)
    date = models.DateField(default=datetime.date.today)
    upload = models.FileField(upload_to="user_imports")