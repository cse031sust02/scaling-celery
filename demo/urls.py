from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('result_backend', views.result_backend, name='result_backend'),
]