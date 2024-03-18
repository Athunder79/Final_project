from django.urls import path, include
from .views import ShotCreateView, find_golf_courses, start_round, scorecard, hole_details, ScorecardView, next_hole
from . import views
from core import views as view



urlpatterns = [
    path('', views.home, name='core-home'),
    path('scorecard/<int:hole_id>/', scorecard,  name='scorecard'),
    path('scorecard2/<int:hole_id>/', ScorecardView.as_view(),  name='scorecard2'),
    path('find-golf-courses/', find_golf_courses, name='find-golf-courses'),
    path('start-round/', start_round, name='start-round'),
    path('hole-details/<int:course_id>/<int:round_id>/', hole_details, name='hole-details'),
    path('hole-details/<int:course_id>/<int:round_id>/', next_hole, name='next-hole'),
    path('map',view.map, name='map'),
    path('map-shots',view.mapshots, name='map-shots'),

    
]

