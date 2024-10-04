from django.contrib import admin

# Register your models here.
from .models import Film, Viewing

admin.site.register(Film)
admin.site.register(Viewing)
