from django.shortcuts import render
from django.urls import path

from webViz.models import PySensorData


def HomePage(request):
    lastdata = PySensorData.objects.using('serveo-server').last()
    return render(request, {'lastdata': lastdata, })



urlpatterns = [
path('', HomePage),
]