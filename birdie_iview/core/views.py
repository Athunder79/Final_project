
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
