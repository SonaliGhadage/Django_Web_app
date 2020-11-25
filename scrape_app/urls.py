from django.urls import path
from . import views

# Mapping our url pattern to this 'views' functions 

urlpatterns = [
    path('', views.home, name="home"),
    path('scrape', views.get_data, name="url"),
]
