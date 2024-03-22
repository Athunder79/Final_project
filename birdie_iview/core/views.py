from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse
from typing import Any
from django.http import JsonResponse, HttpResponseForbidden
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import CreateView, ListView
from django.conf import settings
from .forms import ShotForm, RoundForm, HoleForm
from .models import Shot, Course, Round, Clubs, Hole
import googlemaps
import json



# Create your views here.

def home(request):
        

  
        return render(request, 'core/home.html')

# course and round details
@login_required
def start_round(request):
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

    print(round_id)
    

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

    print(running_scores)


    for hole in holes:
        hole.shot_count = shots.filter(hole=hole).count()
        total_par += hole.hole_par
        print(total_par)
        total_shots += hole.shot_count
        print(total_shots)
        running_scores.append(total_shots - total_par)
        print(running_scores)
   

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
def next_hole(request, hole_id):
    hole = get_object_or_404(Hole, pk=hole_id)
    course_id = hole.course.id
    round_id = hole.round.id

    return redirect(reverse('hole-details', args=[course_id, round_id]))


def find_golf_courses(request):
    gmaps = googlemaps.Client(key=settings.GOOGLE_MAPS_API_KEY)
    key = settings.GOOGLE_MAPS_API_KEY

   # get the user's current location
    location = gmaps.geolocate()
    user_location = (location['location']['lat'], location['location']['lng'])
    user_lat = location['location']['lat']
    user_lng = location['location']['lng']
    radius = 10000  # Define a search radius in meters

    print(user_lat, user_lng)

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
                        'latitude',
                        'longitude',
                        'club',
                        'created_at',
                        'shot_distance',
                        'round_id'

                        ))
  
    return JsonResponse (result_list, safe=False)

# remove this view
class ScorecardView(LoginRequiredMixin, ListView):
    template_name = 'core/scorecard2.html'
    context_object_name = 'data'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = ShotForm()
        context['holes'] = Hole.objects.all()
        context['clubs'] = Clubs.objects.all()
        context['courses'] = Course.objects.all()
        context['rounds'] = Round.objects.all()
        context['shots'] = Shot.objects.filter(user=self.request.user)
        return context

    def get_queryset(self):
        return Shot.objects.filter(user=self.request.user)

    def post(self, request, *args, **kwargs):
        if 'submit_shot' in request.POST:
            return self.submit_shot(request)
        else:
            # Handle other POST requests here
            return super().get(request, *args, **kwargs)

    def submit_shot(self, request):
        form = ShotForm(request.POST)
        if form.is_valid():
            hole_id = form.cleaned_data['hole']
            hole = get_object_or_404(Hole, pk=hole_id)

            # Get the number of shots for the current hole
            shots = Shot.objects.filter(hole=hole)
            shot_count = shots.count() 
            current_shot = shot_count + 1

            # Calculate score
            score = shot_count - hole.hole_par

            latitude = form.cleaned_data['latitude']
            longitude = form.cleaned_data['longitude']
            club = form.cleaned_data['club']

            if club is None:
                return JsonResponse({'error': 'Club ID is required'}, status=400)

            # Save shot info to the database
            shot = form.save(commit=False)
            shot.user = request.user
            shot.course = hole.course
            shot.round = hole.round
            shot.hole = hole.hole_num
            shot.shot_num_per_hole = shot_count
            print(shot.user, shot.course, shot.round, shot.hole, shot.shot_num_per_hole, shot.club, shot.latitude, shot.longitude)
            shot.save()

            return redirect('scorecard2', hole_id=hole_id)
        else:
            # Handle invalid form
            return render(request, self.template_name, {'form': form})

# remove this view 
class ScoreListView(LoginRequiredMixin,ListView):
    context_object_name = 'data'
    def get_context_data(self, **kwargs):
            context = super().get_context_data(**kwargs)
            context['shot'] = Shot.objects.filter(user=self.request.user)
            context['round'] = Round.objects.filter(user=self.request.user)
            context['hole'] = Hole.objects.filter(round__user=self.request.user)
            context['course'] = Course.objects.filter(round__user=self.request.user)
        
            return context        
       
    def get_queryset(self):
        # Override the get_queryset method 
        return Shot.objects.none()

class CoreListView(ListView):
    template_name = 'core/home.html'

    def get_queryset(self):
        return Shot.objects.filter(user=self.request.user)
    
class ShotCreateView(CreateView):
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