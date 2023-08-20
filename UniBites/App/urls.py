from django.urls import path

from .views import home, cafe_list, food_list, checkout, order_confirmation, make_payment, lastpage

app_name = 'app'
urlpatterns = [
    path('', home, name='home'),
    path('lastpage', lastpage, name='lastpage'),
    path('cafe', cafe_list, name='cafe_list'),
    path('cafe/<int:cafe_id>/', food_list, name='food_list'),
    path('cafe/<int:cafe_id>/checkout/', checkout, name='checkout'),
    path('order_confirmation/<int:order_id>/', order_confirmation, name='order_confirmation'),
    path('make_payment/<int:order_id>/', make_payment, name='make_payment'),
]


