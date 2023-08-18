from django.shortcuts import render
from .models import Cafe, FoodItem, Order
from django.shortcuts import render, redirect
from django.contrib import messages

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




def order_confirmation(request):
    if request.method == 'POST':
        cafe_id = request.POST.get('cafe_id')
        total_price = request.POST.get('total_price')
        # You can retrieve other data from the form if needed

        # Create an Order instance in the database
        user = request.user
        cafe = Cafe.objects.get(pk=cafe_id)
        order = Order.objects.create(user=user, cafe=cafe, total_price=total_price)  # Include total_price
        
        # Add selected food items to the order
        selected_food_ids = request.POST.getlist('food')
        selected_food_items = FoodItem.objects.filter(pk__in=selected_food_ids)
        order.items.set(selected_food_items)

        # Calculate the total price based on selected food items
        total_price = sum(item.price for item in selected_food_items)
        order.total_price = total_price
        order.save()  # Save the updated total_price to the order instance

        # Send confirmation email (You'll need to implement this)
        # send_order_confirmation_email(order)

        messages.success(request, 'Order placed successfully!')
        return redirect('cafe_list')
