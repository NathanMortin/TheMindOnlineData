from django.urls import path, re_path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('run_the_code/', views.run_the_code, name='run_the_code'),
    path('show_the_results/', views.show_the_results, name="show_the_results"),
    path('show_the_results/record_filename<str:record_filename>', views.show_the_results, name="show_the_results"),
    path('results/', views.results, name="results"),
    path('results/record_filename<str:record_filename>', views.results, name="results"),
    path('analyzer/', views.analyzer),
    path('upload/', views.upload)
]

