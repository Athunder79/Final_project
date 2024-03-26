from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.urls import reverse
from typing import Any
from django.http import JsonResponse, HttpResponseForbidden
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import CreateView, ListView
from django.conf import settings
from .forms import ShotForm, RoundForm, HoleForm
from django.db.models import Count, Avg, When, Case
from .models import Shot, Course, Round, Clubs, Hole
import googlemaps
import json


# Create your views here.

def home(request):
    return render(request, 'core/home.html')

# course and round details
@login_required
def start_round(request):
    # Check if the user has added clubs to their bag
    if not Clubs.objects.filter(user=request.user).exists():
        messages.error(request, "You have not added any clubs to your bag. Please add a clubs to continue.")
        return redirect('clubs')

    if request.method == 'POST':
        course_id = request.POST.get('course')
        course = get_object_or_404(Course, pk=course_id)
        
        # Assign the current user to the Round
        round = Round.objects.create(user=request.user, course=course)
        
        # Redirect to the hole details with course and round IDs included in the URL
        return redirect('hole-details', course_id=course.id, round_id=round.id)
    else:
        form = RoundForm()
        return render(request, 'core/start_round.html', {'form': form})

# hole details
@login_required
def hole_details(request, course_id, round_id):
    round_obj = get_object_or_404(Round, pk=round_id)
    course_obj = get_object_or_404(Course, pk=course_id)

    # check if user is the owner of the round
    if round_obj.user != request.user:
        return HttpResponseForbidden("You don't have permission to access this page.")

    next_hole_num = 1  # Initialize next_hole_num variable

    # Get the latest hole number for the current round
    latest_hole = Hole.objects.filter(round=round_obj).order_by('-hole_num').first()
    if latest_hole:
        next_hole_num = latest_hole.hole_num + 1  # Increment the latest hole number by 1

    if request.method == 'POST':
        form = HoleForm(request.POST)
        if form.is_valid():
            hole = form.save(commit=False)
            hole.course = course_obj
            hole.round = round_obj
            hole.save()

            # Redirect to the scorecard view passing the hole_id
            return redirect('scorecard', hole_id=hole.id)
    else:
        initial_data = {'hole_num': next_hole_num}  # Pre-populate the hole number
        form = HoleForm(initial=initial_data)

    return render(request, 'core/hole_details.html', {'next_hole_num': next_hole_num,'form': form})

# shot tracking and scorecard
@login_required
def scorecard(request, hole_id):
    current_hole = get_object_or_404(Hole, pk=hole_id)
    round_obj = current_hole.round
    round_id = round_obj.id
    
    # Google Maps API key
    key = settings.GOOGLE_MAPS_API_KEY

    # check if user is the owner of the round
    if round_obj.user != request.user:
        return HttpResponseForbidden("You don't have permission to access this page.")

    holes = Hole.objects.filter(round=current_hole.round, round__user=request.user)
    shots = Shot.objects.filter(hole__in=holes, user=request.user)
    hole_num = current_hole.hole_num

    # Get the number of shots for the current hole
    shot_count = shots.filter(hole=current_hole).count() 
    current_shot = shot_count + 1
    score = shot_count - current_hole.hole_par

    # Get the number of shots for each hole
    total_par = 0
    total_shots = 0
    running_scores = []

    for hole in holes:
        hole.shot_count = shots.filter(hole=hole).count()
        total_par += hole.hole_par
        total_shots += hole.shot_count
        running_scores.append(total_shots - total_par)

    # Get data from the form
    if request.method == 'POST':
        latitude = request.POST.get('latitude')
        longitude = request.POST.get('longitude')
        club_id = request.POST.get('club')

        if club_id is None:
            return JsonResponse({'error': 'Club ID is required'}, status=400)
        
        # Get the Clubs instance 
        club = get_object_or_404(Clubs, pk=club_id, user=request.user)

        # Save shot info to the database
        Shot.objects.create(
            latitude=latitude,
            longitude=longitude,
            hole=current_hole,
            club=club,
            shot_num_per_hole=shot_count,
            course=current_hole.course,
            round=current_hole.round,
            hole_num=current_hole.hole_num,
            hole_par=current_hole.hole_par,
            user=request.user  

        )
        return redirect('scorecard', hole_id=hole_id,)
    else:
        form = ShotForm(user=request.user)

    return render(request, 'core/scorecard.html', {
        'form': form, 
        'hole_num': hole_num, 
        'shots': shots, 
        'holes': holes,
        'current_hole': current_hole,
        'shot_count': shot_count,
        'score': score,
        'current_shot': current_shot,
        'key': key,
        'round_id': round_id,
        'running_scores': running_scores
    })

# return to hole_details with the course_id and round_id
@login_required
def next_hole(request, hole_id, course_id, round_id):
    # Check if user has added a shot for the current hole
    if not Shot.objects.filter(hole=hole_id).exists():
        messages.error(request, "Hole not played please add a shots to continue.")
        return redirect('scorecard', hole_id=hole_id)
    
    
    hole = get_object_or_404(Hole, pk=hole_id)

    # add end latitude and longitude to the previous shot of the hole
    if request.method == 'POST':
        end_latitude = request.POST.get('end_latitude')
        end_longitude = request.POST.get('end_longitude')
        shot = Shot.objects.filter(hole=hole).order_by('-created_at').first()
        shot.end_latitude = end_latitude
        shot.end_longitude = end_longitude
        shot.save()
    
    # check if it is the last hole of the round and update the round status
    if hole.hole_num == 18:
        round = Round.objects.get(pk=round_id)
        round.round_completed = 'True'
        round.save()

    return redirect(hole_details, course_id=course_id, round_id=round_id)
    
def find_golf_courses(request):
    gmaps = googlemaps.Client(key=settings.GOOGLE_MAPS_API_KEY)
    key = settings.GOOGLE_MAPS_API_KEY

   # get the user's current location
    location = gmaps.geolocate()
    user_location = (location['location']['lat'], location['location']['lng'])
    user_lat = location['location']['lat']
    user_lng = location['location']['lng']
    radius = 10000  # Define a search radius in meters


    # Search for golf courses nearby
    places = gmaps.places_nearby(user_location, radius=radius, type='golf_course', keyword='golf course')
    
    # get distance from user's location to the golf course
    for place in places['results']:
        place['distance'] = gmaps.distance_matrix(user_location, place['geometry']['location'])['rows'][0]['elements'][0]['distance']['text']


    # Process the results
    golf_courses = []
    if 'results' in places:
        for place in places['results']:
            name = place['name']
            address = place['vicinity']
            rating = place.get('rating')
            latitude = place['geometry']['location']['lat']
            longitude = place['geometry']['location']['lng']
            distance = place['distance']
            
            golf_courses.append({
                'name': name,
                'address': address,
                'rating': rating,
                'latitude': latitude,
                'longitude': longitude,
                'distance': distance
            })

            # Save the golf courses to the database
            course, created = Course.objects.get_or_create(
                name=name,
                address=address,
                rating=rating,
                latitude=latitude,
                longitude=longitude
            )

            # Sort the golf courses by distance in ascending order
            golf_courses.sort(key=lambda x: x['distance'])

            context = {
                'key': key,
                'golf_courses': golf_courses,
                'user_lat': user_lat,
                'user_lng': user_lng,
                'user_location': user_location,
            }

    return render(request, 'core/find_golf_courses.html', context)

@login_required
def map(request):
    key = settings.GOOGLE_MAPS_API_KEY
    context = {
        'key':key,
    }
    return render(request, 'core/map.html',context)

#plot shots on the map
@login_required
def mapshots(request):
    # Get the shots details from the database
    result_list = list(Shot.objects\
                .exclude(latitude__isnull=True)\
                .exclude(longitude__isnull=True)\
                .values('id',
                        'shot_num_per_hole',
                        'hole_num', 
                        'latitude',
                        'longitude',
                        'club__club_name',
                        'created_at',
                        'shot_distance',
                        'round_id',
                        'end_latitude',
                        'end_longitude'

                        ))
  
    return JsonResponse (result_list, safe=False)

class ScoreListView(LoginRequiredMixin, ListView):
    template_name = 'core/rounds.html'
    context_object_name = 'data'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['round'] = Round.objects.filter(user=self.request.user)

        # Query to calculate statistics per club for all shots
        shots_per_club_all = (
            Shot.objects.filter(user=self.request.user)
            .values('club__club_name')
            .annotate(total_shots=Count('id'), average_distance=Avg('shot_distance'))
        )
        context['shots_per_club_all'] = shots_per_club_all

        return context

    def get_queryset(self):
        return Shot.objects.filter(user=self.request.user)

class CoreListView(ListView):
    template_name = 'core/home.html'

    def get_queryset(self):
        return Shot.objects.filter(user=self.request.user)
    

    model = Shot
    form_class = ShotForm
    template_name = 'core/scorecard.html'

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)
    
class RoundCreateView(CreateView):
    model = Round
    form_class = RoundForm
    template_name = 'core/start_round.html'

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

class HoleCreateView(CreateView):
    model = Hole
    fields = ['hole_num', 'hole_par', 'hole_distance']
    template_name = 'core/scorecard.html'

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)