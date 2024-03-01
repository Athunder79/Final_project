from typing import Any
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field
from django import forms
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
    


def scorecard(request):
    if request.method == 'POST':
        latitude = request.POST.get('latitude')
        longitude = request.POST.get('longitude')

        def __init__(self, *args, **kwargs):
            super(CoordinatesForm, self).__init__(*args, **kwargs)
            self.helper = FormHelper()
            self.helper.layout = Layout(
                Field('latitude', id="latitude_field_id"),
                Field('longitude', id="longitude_field_id"),
        )
        # Save coordinates to the database
        Coordinates.objects.create(latitude=latitude, longitude=longitude)
        
        return JsonResponse({'message': 'Coordinates saved successfully'}, status=200)
    else:
        return render(request, 'core/scorecard.html')

class CoordinatesForm(forms.ModelForm):
    class Meta:
        model = Coordinates
        fields = ['latitude', 'longitude']

    def __init__(self, *args, **kwargs):
        super(CoordinatesForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Field('latitude', id="latitude"),
            Field('longitude', id="longitude"),
        )  
    
class CoreListView(ListView):
    template_name = 'core/home.html'

    def get_queryset(self):
        return Coordinates.objects.filter(user=self.request.user)
    
    
class CoordinatesCreateView(CreateView):
    model = Coordinates
    form_class = CoordinatesForm
    template_name = 'core/scorecard.html'

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)
    

  



# Create your views here.
