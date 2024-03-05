from django.urls import path
from .views import ShotCreateView
from . import views

urlpatterns = [
    path('', views.home, name='core-home'),
    path('scorecard/', ShotCreateView.as_view(), name='scorecard-create'),
    
]

