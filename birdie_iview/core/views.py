from typing import Any
from django.db.models.query import QuerySet
from django.shortcuts import render
from django.http import HttpResponse,JsonResponse
from .models import Coordinates
from django.views.generic import CreateView, DetailView,ListView


def home(request):
    if request.method == 'POST':
        latitude = request.POST.get('latitude')
        longitude = request.POST.get('longitude')
        
        # Save coordinates to the database
        Coordinates.objects.create(latitude=latitude, longitude=longitude)
        
        return JsonResponse({'message': 'Coordinates saved successfully'}, status=200)
    else:
        return render(request, 'core/home.html')
    

class CoreListView(ListView):
    template_name = 'core/home.html'

    def get_queryset(self):
        return Coordinates.objects.filter(user=self.request.user)
    
    
class CoordinatesCreateView(CreateView):
    model = Coordinates
    fields = ['latitude', 'longitude']
    template_name = 'core/home.html'

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)   



# Create your views here.
