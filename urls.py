from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index' ),
    path('signup', views.signup, name='signup' ),
    path('weather', views.weather, name='weather' ),
    path('jsonurl', views.jsonurl, name='jsonurl' ),
]