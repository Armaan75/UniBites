from django.urls import path

from .views import home, cafe_list, food_list, checkout

app_name = 'app'
urlpatterns = [
    path('', home, name='home'),
    path('cafe', cafe_list, name='cafe_list'),
    path('cafe/<int:cafe_id>/', food_list, name='food_list'),
    path('cafe/<int:cafe_id>/checkout/', checkout, name='checkout'),
    path('order_confirmation/', views.order_confirmation, name='order_confirmation'),

]


