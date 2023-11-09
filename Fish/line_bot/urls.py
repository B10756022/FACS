from django.urls import path
from . import views
from django.conf.urls import url

urlpatterns = [
    #url('^callback', views.callback)
    path('callback', views.callback)
]