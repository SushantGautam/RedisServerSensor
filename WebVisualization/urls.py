from django.shortcuts import render
from django.urls import path


def HomePage(request):
    return render(request, 'homepage.html')



urlpatterns = [
path('', HomePage),
]