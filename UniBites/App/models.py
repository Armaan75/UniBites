from django.db import models
from accounts.models import User

class Cafe(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class FoodItem(models.Model):
    cafe = models.ForeignKey(Cafe, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=6, decimal_places=2)

    def __str__(self):
        return self.name

class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    cafe = models.ForeignKey(Cafe, on_delete=models.CASCADE)
    items = models.ManyToManyField(FoodItem)
    note = models.TextField(blank=True)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)  # Add this field
    timestamp = models.DateTimeField(auto_now_add=True)



class Payment(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_DEFAULT, default=None, null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_DEFAULT, default=None, null=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    timestamp = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Payment for Order #{self.order.id} by {str(self.user)}"