from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field
from django import forms
from .models import Shot

class ShotForm(forms.ModelForm):
    class Meta:
        model = Shot
        fields = ['latitude', 'longitude', 'club']

    def __init__(self, *args, **kwargs):
        super(ShotForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Field('latitude', id='latitude', css_class="hide-input"),
            Field('longitude', id="longitude", css_class="hide"),
            Field('club', id="club")
        )
