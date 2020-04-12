from django.shortcuts import render,redirect
from django.contrib import messages

from .forms import UserRegisterForm,UserUpdateForm


def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'{username} hesabı oluşturuldu.Şimdi giriş yapabilirsin')
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'registration/register.html', {'form': form})

