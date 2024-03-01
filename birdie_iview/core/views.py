from django.http import JsonResponse
from django.shortcuts import render
from django.views.generic import CreateView, ListView
from .forms import ShotForm
from .models import Shot

def home(request):
    if request.method == 'POST':
        latitude = request.POST.get('latitude')
        longitude = request.POST.get('longitude')
        
        # Save coordinates to the database
        Shot.objects.create(latitude=latitude, longitude=longitude)
        
        return JsonResponse({'message': 'Coordinates saved successfully'}, status=200)
    else:
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
