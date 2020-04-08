from django.http import HttpResponse
from django.shortcuts import redirect



def unauthenticated_user(view_func):
    def wrapper_func(request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('home')
        else:
            return view_func(request, *args, **kwargs)
    return wrapper_func




def allowed_users(allowed_roles=[]):
    def decorater(view_fun):
        def wrapper_func(request, *args, **kwargs):

            group = None

            if request.user.groups.exists():
                group = request.user.groups.all()[0].name

            if group in allowed_roles:
                return view_fun(request, *args, **kwargs)
            else:
                return HttpResponse("You are not Autherised to view this page")
        return wrapper_func
    return decorater

def admin_only(view_func):
    def wrapper_function(request, *args, **kwags):
        group = None
        if request.user.groups.exists():
            group = request.user.groups.all()[0].name
        if group == 'customer':
            return redirect('user_page')
        if group == 'admin':
            return view_func(request, *args, **kwags)
    return wrapper_function