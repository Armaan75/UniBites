from django.shortcuts import render
from .models import Cafe, FoodItem
# Create your views here.
def home(request):
    return render(request, 'app/home.html')

def cafe_list(request):
    cafes = Cafe.objects.all()
    return render(request, 'app/cafe_list.html', {'cafes': cafes})

def food_list(request, cafe_id):
    cafe = Cafe.objects.get(pk=cafe_id)
    food_items = FoodItem.objects.filter(cafe=cafe)
    return render(request, 'app/food_list.html', {'cafe': cafe, 'food_items': food_items})

def checkout(request, cafe_id):
    if request.method == 'POST':
        selected_food_ids = request.POST.getlist('food')
        note = request.POST.get('note', '')
        cafe = Cafe.objects.get(pk=cafe_id)
        selected_food_items = FoodItem.objects.filter(pk__in=selected_food_ids)
        total_price = sum(item.price for item in selected_food_items)
        return render(request, 'app/checkout.html', {'cafe': cafe, 'selected_food_items': selected_food_items, 'total_price': total_price, 'note': note})
