from django.urls import path
from .views import CoordinatesCreateView
from . import views

urlpatterns = [
    path('', views.home, name='core-home'),
    path('scorecard/', CoordinatesCreateView.as_view(), name='scorecard-create'),
    
]

