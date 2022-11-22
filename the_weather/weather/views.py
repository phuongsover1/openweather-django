from django.shortcuts import render
import requests
from decimal import Decimal
from decimal import getcontext
from django.utils import timezone
from datetime import datetime

from .forms import CityForm

from .models import TemperatureCity

import firebase_admin
from firebase_admin import firestore
from firebase_admin import credentials


# Create your views here.


def index(request):
    url = 'http://api.openweathermap.org/data/2.5/weather?q={}&units=imperial&appid={}'

    print('request: ', request)
    if request.method == 'POST':
        form = CityForm(request.POST)
        # validate and save if the data is validate
        # form.save()

        new_city = TemperatureCity()
        new_city.name = form.data.get('name')
        new_city.save(using='mysql_db')

    form = CityForm()

    # cities = TemperatureCity.objects.all()
    cities = TemperatureCity.objects.using('mysql_db').all()

    list_weather = []

    my_api_key = '3cebd2fe51f0c0bdbd71f6cdba4e1306'
    for city in cities:
        city_weather = requests.get(url.format(city, my_api_key)).json()

        getcontext().prec = 4
        temperature = (
            Decimal(city_weather['main']['temp']) - 32) * Decimal(5/9)

        weather = {
            'city': city,
            'temperature': temperature,
            'description': city_weather['weather'][0]['description'],
            'icon': city_weather['weather'][0]['icon']
        }
        list_weather.append(weather)

    context = {
        'list_weather': list_weather,
        'form': form
    }

    time = datetime('2020-10-31 12:00:00+01:00')
    print(time)
    return render(request, 'weather/index.html', context)
