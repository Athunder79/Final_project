from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field, Div
from django import forms
from .models import Shot, Round, Course, Hole


class ShotForm(forms.ModelForm):
    class Meta:
        model = Shot
        fields = ['latitude', 'longitude', 'club']

    def __init__(self, *args, **kwargs):
        super(ShotForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Field('latitude', id='latitude', css_class='hide-input'),
            Field('longitude', id='longitude', css_class='hide-input'),
            Field('club', id='club'),
    
        )

class HideInput(forms.widgets.Input):
    input_type = 'hidden'

ShotForm.base_fields['latitude'].widget = HideInput()
ShotForm.base_fields['longitude'].widget = HideInput()

class RoundForm(forms.ModelForm):
    class Meta:
        model = Round
        fields = ['course']

    def __init__(self, *args, **kwargs):
        super(RoundForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Field('course', id='course'),
        )

class HoleForm(forms.ModelForm):
    class Meta:
        model = Hole
        fields = ['hole_num', 'hole_par', 'hole_distance']

    def __init__(self, *args, **kwargs):
        super(HoleForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Field('hole_num', id='hole_num'),
            Field('hole_par', id='hole_par'),
            Field('hole_distance', id='hole_distance'),
        )