from django.shortcuts import redirect, render
from django.contrib import auth
from django.urls import reverse


def login(request):
    if request.method == 'GET':
        # if request.user.is_authenticated:
        #     return redirect('/')
        return render(request, 'login/login.html')

    if request.method == 'POST':
        username = request.POST.get('username')
        senha = request.POST.get('senha')
        usuario = auth.authenticate(username=username, password=senha)
        if not usuario:
            return redirect('/auth/login')
        else:
            auth.login(request, usuario)
            return redirect(reverse('home'))


def logout(request):
    auth.logout(request)
    return redirect('/auth/login')
