from django.urls import path
from . import views
urlpatterns = [
	path('/add', views.add, name='add'),
    path('/watch', views.watch, name='watch'),
    path('/list', views.listof, name='listof'),
    path('/submit', views.submit, name='submit'),
]