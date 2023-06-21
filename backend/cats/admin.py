from django.contrib import admin

from .models import Achievement, Cat, AchievementCat

models = [Achievement, AchievementCat, Cat]
admin.site.register(models)
