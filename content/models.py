from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Category(models.Model):
    name = models.CharField(max_length=50)
    slug = models.SlugField(unique=True)

class Post(models.Model):
    PREMIUM = 'PR'
    FREE = 'FR'
    ACCESS_CHOICES = [
        (PREMIUM, 'Premium'),
        (FREE, 'Free'),
    ]
    
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    content = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    access_level = models.CharField(
        max_length=2,
        choices=ACCESS_CHOICES,
        default=FREE
    )
    featured_image = models.ImageField(upload_to='post_images/')
    
    def __str__(self):
        return self.title