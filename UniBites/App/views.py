from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Cafe, FoodItem, Order, Payment
from .forms import PaymentForm
from django.core.mail import send_mail
from django.conf import settings

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
    return render(request, 'app/order_confirmation.html')

def make_payment(request, order_id):
    order = Order.objects.get(pk=order_id)
    
    selected_food_ids = request.POST.getlist('food')
    note = request.POST.get('note', '')

    selected_food_items = FoodItem.objects.filter(pk__in=selected_food_ids)
    total_price = sum(item.price for item in selected_food_items)

    if request.method == 'POST':
        form = PaymentForm(request.POST)

        if form.is_valid():
            payment = Payment.objects.create(
                user=request.user,
                order=order,
                amount=order.total_price 
            )

            order.paid = True
            order.save()

            return redirect('app:lastpage')
    else:
        form = PaymentForm()

    return render(request, 'app/payment.html', {'form': form, 'order': order, 'total_price': total_price})

def order_confirmation(request, order_id):
    order = get_object_or_404(Order, pk=order_id)

    # Rest of your view logic
    total_price = order.total_price
    
    selected_food_ids = request.POST.getlist('food')
    note = request.POST.get('note', '')

    selected_food_items = FoodItem.objects.filter(pk__in=selected_food_ids)
    total_price = sum(item.price for item in selected_food_items)

    subject = 'Order Confirmation'
    message = f'Hello {order.user.username}, your order has been placed successfully.\n\nOrder details:\nCafe: {order.cafe.name}\nTotal Price: ${total_price}\n\nThank you for your order!'
    from_email = settings.DEFAULT_FROM_EMAIL
    recipient_list = [order.user.email]

    send_mail(subject, message, from_email, recipient_list, fail_silently=True)

    return render(request, 'app/order_confirmation.html', {'order': order, 'total_price': total_price})


def lastpage(request):
    return render(request, 'app/lastpage.html')