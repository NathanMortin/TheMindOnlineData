from django.urls import path, re_path

from . import views

urlpatterns = [
    re_path('^$', views.index, name='index'),
    re_path('^run_the_code/$', views.run_the_code, name='run_the_code'),
    re_path('^showTheResults/$', views.show_the_results),
    # re_path(r'^show_the_results/(?P<input_name>\D+)/', views.show_the_results)
    # re_path(r'showTheResults/(?P<incubator_id>\w+)/$', views.show_the_results, name="showTheResults"),
    # re_path(r'^showTheResults/(?P<input_name>\w+)/$', views.show_the_results, name="showTheResults"),
    # re_path(r'^showTheResults/(?P<input_name>\w+)/$', views.show_the_results, name="showTheResults"),
    # re_path(r'^showTheResults/(?P<input_name>)/$', views.show_the_results, name="showTheResults"),
]

