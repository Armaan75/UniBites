from django.db import models
from accounts.models import User

class Cafe(models.Model):
    name = models.CharField(max_length=100)

class FoodItem(models.Model):
    cafe = models.ForeignKey(Cafe, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=6, decimal_places=2)

class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    cafe = models.ForeignKey(Cafe, on_delete=models.CASCADE)
    items = models.ManyToManyField(FoodItem)
    note = models.TextField(blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
