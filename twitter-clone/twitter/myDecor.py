from functools import wraps
from django.shortcuts import redirect

def check_if_user_logged(function):
    @wraps(function)
    def wrap(request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('home')
        else:
            return function(request, *args, **kwargs)
    return wrap
