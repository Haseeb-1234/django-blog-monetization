from django.db import models

# Create your models here.
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone

class User(AbstractUser):
    is_premium = models.BooleanField(default=False)
    subscription_end = models.DateTimeField(null=True, blank=True)
    bio = models.TextField(max_length=500, blank=True)
    avatar = models.ImageField(upload_to='avatars/', blank=True)
    is_premium = models.BooleanField(default=False)
    premium_since = models.DateTimeField(null=True, blank=True)
    premium_until = models.DateTimeField(null=True, blank=True)
    
    @property
    def has_active_premium(self):
        if self.is_premium and self.premium_until:
            return timezone.now() < self.premium_until
        return self.is_premium
    
    def __str__(self):
        return self.email