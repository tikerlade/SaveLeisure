from django.http import HttpResponse


def home_view(*args, **kwargs):
    return HttpResponse("<h1> Наконец-то работает !!!</h1>")
