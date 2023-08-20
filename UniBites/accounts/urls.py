from django.urls import path

from .views import login, register, Profile

app_name = 'account'
urlpatterns = [
    path('profile/', Profile.as_view(), name='profile'),

    path('login/', login, name='login'),
    path('register/', register, name='register'),
    # path('logout/', views.logout, name='logout'),

]