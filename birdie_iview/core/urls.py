from django.urls import path
from .views import ShotCreateView, find_golf_courses
from . import views

urlpatterns = [
    path('', views.home, name='core-home'),
    path('scorecard/', ShotCreateView.as_view(), name='scorecard-create'),
    path('find-golf-courses/', find_golf_courses, name='find_golf_courses'),
    
]

