from django.contrib import messages, auth
from django.contrib.auth import models
from django.shortcuts import redirect, render
from django.urls.base import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import User
from django.views.generic import UpdateView
from .forms import ProfileForm

def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(username=username, password=password)
        if user is not None:
            auth.login(request, user)
            return redirect('app:home')
        else:
            return redirect('account:login')
    return render(request, 'account/login.html')
    
def register(request):
    if request.method == 'POST':
        first_name = request.POST['first_name']
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']  
        confirm_password = request.POST['confirm_password'] 
        if password == confirm_password:
            if User.objects.filter(username=username).exists():
                messages.error(request, 'Someone with this username already exist!')
                return redirect('account:register')
            else:
                if User.objects.filter(email=email).exists():
                    messages.error(request, 'This Email is already exist')
                    return redirect('account:register')
                else:
                    user = User.objects.create_user(first_name = first_name, username=username, email=email, password=password)
                    user.save()
                    messages.success(request, 'You Successfully Created account')
                    return redirect('account:login')
        else:
            messages.error(request, 'Passwords are not same')

    return render(request, 'account/register.html')


def logout(request):
    if request.method == 'POST':
        auth.logout(request)
        messages.success(request, 'You! successfully Logged out')
        return redirect('account:login')
    return redirect('account:login')

class Profile(UpdateView):
    model = User
    template_name = 'account/profile_update.html'
    form_class = ProfileForm
    success_url = reverse_lazy('account:profile')
    def get_object(self):
        return User.objects.get(pk = self.request.user.pk)

    def get_form_kwargs(self):
        kwargs = super(Profile, self).get_form_kwargs()
        kwargs.update({
            'user': self.request.user
        })
        return kwargs


