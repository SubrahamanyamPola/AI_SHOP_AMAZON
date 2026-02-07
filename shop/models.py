
from django.db import models
from django.contrib.auth.models import User

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(unique=True)
    def __str__(self): return self.name

class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')
    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image_url = models.URLField(blank=True)
    def __str__(self): return self.name

OVERRIDE_CHOICES = (('auto','Auto'), ('genuine','Genuine'), ('fake','Fake'))

class Review(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    rating = models.PositiveSmallIntegerField(default=5)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    override_label = models.CharField(max_length=8, choices=OVERRIDE_CHOICES, default='auto')
    def __str__(self): return f"{self.product.name} - {self.rating}★"
