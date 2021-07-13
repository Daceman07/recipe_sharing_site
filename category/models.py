from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Category(models.Model):
    title = models.CharField(max_length=255)
    user = models.ForeignKey(User, on_delete=models.CASCADE)


class Recipe(models.Model):
    title = models.CharField(max_length=255)
    picture = models.ImageField(upload_to='recipe/images/', blank=True)
    prep_time = models.CharField(max_length=100)
    cook_time = models.CharField(max_length=100)
    servings = models.IntegerField(blank=True)
    ingredients = models.TextField()
    directions = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
