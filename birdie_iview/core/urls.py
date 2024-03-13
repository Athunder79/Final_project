from django.urls import path
from .views import ShotCreateView, find_golf_courses, start_round
from . import views

urlpatterns = [
    path('', views.home, name='core-home'),
    path('scorecard/<int:hole_id>/', views.scorecard,  name='scorecard'),
    path('find-golf-courses/', find_golf_courses, name='find-golf-courses'),
    path('start-round/', views.start_round, name='start-round'),
    path('hole-details/<int:course_id>/<int:round_id>/', views.hole_details, name='hole-details'),
    
]

