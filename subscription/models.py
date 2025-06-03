from django.db import models

# Create your models here.
from django.db import models
from django.conf import settings
from djstripe.models import Product, Price

class SubscriptionPlan(models.Model):
    name = models.CharField(max_length=100)
    stripe_price_id = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    interval = models.CharField(max_length=20, choices=[
        ('month', 'Monthly'),
        ('year', 'Yearly')
    ])
    features = models.TextField()
    is_active = models.BooleanField(default=True)
    
    def __str__(self):
        return f"{self.name} (${self.price}/{self.interval})"