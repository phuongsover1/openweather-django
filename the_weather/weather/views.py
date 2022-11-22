from django.shortcuts import render
import requests
from decimal import Decimal
from decimal import getcontext

from .forms import CityForm

from .models import TemperatureCity

import firebase_admin
from firebase_admin import firestore
from firebase_admin import credentials


# Create your views here.
# Application Default credentials are automatically created.


# Use a service account.
# cred = credentials.Certificate(
#     '/media/phuongnguyen/DATA/PythonProjects/openweather/the_weather/weather/openweather.json')

# app = firebase_admin.initialize_app(cred)

# db = firestore.client()


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
        # doc_ref = db.collection(u'cities_temperature').document(new_city.name)
        # doc_ref.set({
        #     u'name': new_city.name,
        # })

    # cities_ref = db.collection(u'cities_temperature')
    # docs = cities_ref.stream()
    # for city in docs:
    #     print(f'{city.id} => {city.to_dict()}')

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
    return render(request, 'weather/index.html', context)
