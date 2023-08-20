from django.contrib import admin
from .models import Cafe, FoodItem, Order, Payment

@admin.register(Cafe)
class CafeAdmin(admin.ModelAdmin):
    list_display = ('name',)

@admin.register(FoodItem)
class FoodItemAdmin(admin.ModelAdmin):
    list_display = ('name', 'cafe', 'price')

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('user', 'cafe', 'timestamp')


class PaymentAdmin(admin.ModelAdmin):
    list_display = ('user', 'order', 'amount', 'timestamp')
    list_filter = ('timestamp',)
    search_fields = ('user__username', 'order__id')

admin.site.register(Payment, PaymentAdmin)