from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_not_required
from django.shortcuts import render, redirect


def me(request):
    return render(request, 'me.html')


@login_not_required
def user_login(request):
    if request.method == 'POST':
        username = request.POST['login']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('index')
        else:
            return render(request, 'login.html', {'error': 'Неверное имя пользователя или пароль.'})
    else:
        return render(request, 'login.html')


def user_logout(request):
    logout(request)
    return redirect('login')
