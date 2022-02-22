from django.http import HttpResponse
from django.shortcuts import redirect
from django.contrib import messages

def dla_zalogowanych(view_func):
    def wrapper_func(request, *args, **kwargs):
        if request.user.is_authenticated:
            return view_func(request, *args, **kwargs)
        else:
            messages.warning(request, 'Aby mieć dostęp do strony musisz się zalogować')
            return redirect('logowanie')

    return wrapper_func 

def dla_niezalogowanych(view_func):
    def wrapper_func(request, *args, **kwargs):
        if request.user.is_authenticated:
            messages.error(request, 'Strona dostępna tylko dla niezalogowanych użytkowników')
            return redirect('index')
        else:
            return view_func(request, *args, **kwargs)
           

    return wrapper_func 



