from django.http import HttpResponse


def index(request):
    return HttpResponse("<h1>Welcome to Django!</h1><p>This is a simple Django application created with pipenv.</p>")