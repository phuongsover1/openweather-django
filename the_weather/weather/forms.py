from django.forms import ModelForm, TextInput
from .models import TemperatureCity


class CityForm(ModelForm):
    class Meta:
        model = TemperatureCity
        fields = ['name']

        widget = {
            'name': TextInput(attrs={'class': 'input', 'placeholder': 'City Name'}),
        }
