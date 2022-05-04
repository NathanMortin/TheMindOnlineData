from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('run_the_code/', views.run_the_code, name='run_the_code'),
]