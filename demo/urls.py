from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('result_backend', views.result_backend, name='result_backend'),
    path('result_backend/remove_task/<task_id>', views.remove_task, name='remove_task'),
]