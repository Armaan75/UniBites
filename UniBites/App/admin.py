from django.contrib import admin
from .models import Cafe, FoodItem, Order



@admin.register(Cafe)
class CafeAdmin(admin.ModelAdmin):
    list_display = ('name',)

@admin.register(FoodItem)
class FoodItemAdmin(admin.ModelAdmin):
    list_display = ('name', 'cafe', 'price')

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('user', 'cafe', 'timestamp')


