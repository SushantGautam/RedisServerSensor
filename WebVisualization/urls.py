from django.shortcuts import render
from django.urls import path

from webViz.models import PySensorData


def RealTimeMapsView(request, ):
    lastdata = PySensorData.objects.using('serveo-server').last()
    return render(request, 'homepage.html', {'lastdata' : lastdata, })



urlpatterns = [
path('', RealTimeMapsView),
]