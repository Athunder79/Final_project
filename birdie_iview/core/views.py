
from django.http import JsonResponse
from django.shortcuts import render
from django.views.generic import CreateView, ListView
from django.conf import settings
from .forms import ShotForm
from .models import Shot, Course
import googlemaps
from django.shortcuts import render


# Create your views here.

def home(request):
  return render(request, 'core/home.html')

def scorecard(request):
    if request.method == 'POST':
        latitude = request.POST.get('latitude')
        longitude = request.POST.get('longitude')
        
        # Save coordinates to the database
        Shot.objects.create(latitude=latitude, longitude=longitude)
        
        return JsonResponse({'message': 'Coordinates saved successfully'}, status=200)
    else:
        form = ShotForm()
        return render(request, 'core/scorecard.html', {'form': form})

def find_golf_courses(request):
    gmaps = googlemaps.Client(key=settings.GOOGLE_MAPS_API_KEY)
    location = (53.3498053, -6.2603097)  # Dublin coordinates
    radius = 10000  # 10km radius

    # Search for golf courses nearby
    places = gmaps.places_nearby(location, radius=radius, type='golf_course')

    # Process the results and save to Course model
    golf_courses = []
    if 'results' in places:
        for place in places['results']:
            if 'golf_course' in place.get('types', []):
                course_info = {
                    'name': place['name'],
                    'address': place['vicinity'],
                    'rating': place.get('rating', None),
                   
                    'longitude': place['geometry']['location']['lng'],
                }
                # Check for duplicates based on coordinates
                if not Course.objects.filter(latitude=course_info['latitude'], longitude=course_info['longitude']).exists():
                    golf_courses.append(course_info)
                    # Create and save Course object
                    Course.objects.create(**course_info)
    return render(request, 'core/find_golf_courses.html', {'golf_courses': golf_courses})


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
