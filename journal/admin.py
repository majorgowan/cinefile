from django.contrib import admin

# Register your models here.
from .models import Film, Viewing, Follow, ImportedFile

admin.site.register(Film)
admin.site.register(Viewing)
admin.site.register(Follow)
admin.site.register(ImportedFile)