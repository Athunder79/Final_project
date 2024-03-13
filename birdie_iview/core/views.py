
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import CreateView, ListView
from django.conf import settings
from .forms import ShotForm, RoundForm, HoleForm
from .models import Shot, Course, Round, Clubs, Hole
import googlemaps
from django.shortcuts import render


# Create your views here.

def home(request):
        

  
        return render(request, 'core/home.html')
    
def start_round(request):
    if request.method == 'POST':
        course_id = request.POST.get('course')
        course = get_object_or_404(Course, pk=course_id)
        
        # Assign the current user to the user field of the Round object
        round = Round.objects.create(user=request.user, course=course)
        
        # Redirect to the scorecard page with course and round IDs included in the URL
        return redirect('hole-details', course_id=course.id, round_id=round.id)
    else:
        form = RoundForm()
        return render(request, 'core/start_round.html', {'form': form})

@login_required
def scorecard(request, hole_id):
    hole = get_object_or_404(Hole, pk=hole_id)
    shot = Shot.objects.filter(hole=hole)
    hole_num = hole.hole_num

    # Get the number of shots for the current hole
    shot_count = Shot.objects.filter(hole=hole).count()+1

    score = shot_count - hole.hole_par
    
    if request.method == 'POST':
        latitude = request.POST.get('latitude')
        longitude = request.POST.get('longitude')
        club_id = request.POST.get('club')

        if club_id is None:
            return JsonResponse({'error': 'Club ID is required'}, status=400)
        
        # Get the Clubs instance based on the provided ID
        club = get_object_or_404(Clubs, pk=club_id)
        # Save cshot info to the database
        Shot.objects.create(
            latitude=latitude,
            longitude=longitude,
            hole=hole,
            club=club,
            shot_num_per_hole=shot_count,
            course=hole.course,
            round=hole.round,
            hole_num = hole.hole_num,
            hole_par = hole.hole_par,
            user=request.user  # Assign the user to the Shot object
        )

        print (hole.hole_distance)
        
        return redirect('scorecard', hole_id=hole_id)
    else:
        form = ShotForm()
        # Get data for each hole
   

    return render(request, 'core/scorecard.html', {
        'form': form, 
        'hole_num': hole_num, 
        'shot': shot, 
        'hole': hole, 
        'shot_count': shot_count,
        'score': score,
       
        })

def find_golf_courses(request):
    gmaps = googlemaps.Client(key=settings.GOOGLE_MAPS_API_KEY)
    # Assuming coordinates of a location (you can get it from the user's input or any other source)
    location = (53.3498053, -6.2603097)
    radius = 10000  # Define a search radius in meters

    # Search for golf courses nearby
    places = gmaps.places_nearby(location, radius=radius, type='golf_course', keyword='golf course')

    # Process the results
    golf_courses = []
    if 'results' in places:
        for place in places['results']:
            name = place['name']
            address = place['vicinity']
            rating = place.get('rating')
            latitude = place['geometry']['location']['lat']
            longitude = place['geometry']['location']['lng']

            # Append golf course data to the list
            golf_courses.append({
                'name': name,
                'address': address,
                'rating': rating,
                'latitude': latitude,
                'longitude': longitude
            })

            # Save the golf courses to the database
            course, created = Course.objects.get_or_create(
                name=name,
                address=address,
                rating=rating,
                latitude=latitude,
                longitude=longitude
            )

    return render(request, 'core/find_golf_courses.html', {'golf_courses': golf_courses})

@login_required
def hole_details(request, course_id, round_id):
    round_obj = get_object_or_404(Round, pk=round_id)
    course_obj = get_object_or_404(Course, pk=course_id)

    if request.method == 'POST':
        form = HoleForm(request.POST)
        if form.is_valid():
            hole = form.save(commit=False)
            hole.course = course_obj
            hole.round = round_obj
            hole.save()

            # Redirect to the scorecard view passing the course_id, round_id, and hole_id
            return redirect('scorecard',  hole_id=hole.id)
    else:
        form = HoleForm()

    return render(request, 'core/hole_details.html', {'form': form})

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
    template_name = 'core/hole_details.html'

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)