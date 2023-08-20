from django.shortcuts import render
from .models import Cafe, FoodItem, Order, Payment
from django.shortcuts import render, redirect
from django.contrib import messages

from .forms import PaymentForm

from django.core.mail import send_mail
from django.conf import settings

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


def make_payment(request, order_id):
    order = Order.objects.get(pk=order_id)

    if request.method == 'POST':
        form = PaymentForm(request.POST)

        if form.is_valid():
            # Dummy payment process: Create a payment record
            payment = Payment.objects.create(
                user=request.user,
                order=order,
                amount=order.total_price  # In a real system, this would be the actual payment amount
            )

            # Mark the order as paid (you can add a field in the Order model for this)
            order.paid = True
            order.save()

            return redirect('app:order_confirmation', order_id=order_id)
    else:
        form = PaymentForm()

    return render(request, 'app/payment.html', {'form': form, 'order': order})



def checkout(request, cafe_id):
    if request.method == 'POST':
        selected_food_ids = request.POST.getlist('food')
        note = request.POST.get('note', '')
        cafe = Cafe.objects.get(pk=cafe_id)
        selected_food_items = FoodItem.objects.filter(pk__in=selected_food_ids)
        total_price = sum(item.price for item in selected_food_items)
        
        order = Order.objects.create(
            user=request.user,  
            cafe=cafe,
            total_price=total_price,
        )
        order.items.set(selected_food_items)

        subject = 'Order Confirmation'
        message = f'Hello {request.user.username}, your order has been placed successfully.\n\nOrder details:\nCafe: {cafe.name}\nTotal Price: ${total_price}\n\nThank you for your order!'
        from_email = settings.DEFAULT_FROM_EMAIL
        recipient_list = [request.user.email]
        
        send_mail(subject, message, from_email, recipient_list, fail_silently=True)

        return redirect('app:order_confirmation', order_id=order.id)
    else:
        return redirect('app:cafe_list')




def order_confirmation(request, order_id):
    try:
        order = Order.objects.get(pk=order_id)
    except Order.DoesNotExist:
        return redirect('app:cafe_list')  


    subject = 'Order Confirmation'
    message = f'Hello {order.user.username}, your order has been placed successfully.\n\nOrder details:\nCafe: {order.cafe.name}\nTotal Price: ${order.total_price}\n\nThank you for your order!'
    from_email = settings.DEFAULT_FROM_EMAIL
    recipient_list = [order.user.email]

    send_mail(subject, message, from_email, recipient_list, fail_silently=True)

    return render(request, 'app/order_confirmation.html', {'order': order})


