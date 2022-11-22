from django.shortcuts import render
import requests
from decimal import Decimal
from decimal import getcontext

from .models import Arduino_Temperature

import firebase_admin
from firebase_admin import firestore
from firebase_admin import credentials


# Create your views here.
# Application Default credentials are automatically created.


# Use a service account.
cred = credentials.Certificate(
    '/media/phuongnguyen/DATA/PythonProjects/openweather/the_weather/weather/openweather.json')

app = firebase_admin.initialize_app(cred)

db = firestore.client()


# Create your views here.

def index(request):

    # Lấy nhiệt độ từ Arduino về

    # api trả về kết quả là nhiệt độ mới nhất của arduino
    api_arduino = 'https://api.thingspeak.com/channels/1867718/feeds.json?api_key=0U6CXNXQPN70JVCQ&results=1'

    temperature = requests.get(api_arduino).json()
    print(temperature)

    last_id = temperature['channel']['last_entry_id']

    count = Arduino_Temperature.objects.filter(id=last_id).count()
    if count == 0:
        latest_temperature = temperature['feeds'][0]
        print('latest_temperature: ', latest_temperature)
        temperature = Arduino_Temperature()
        temperature.id = last_id
        temperature.created_at = latest_temperature['created_at']
        temperature.temperature = latest_temperature['field1']
        temperature.humidity = latest_temperature['field2']

        # Save to Cloud
        doc_ref = db.collection(
            u'arduino_temperature').document(str(temperature.id))
        doc_ref.set({
            u'id': str(temperature.id),
            u'created_at': str(temperature.created_at),
            u'temperature': str(temperature.temperature),
            u'humidity': str(temperature.humidity),
        })

        # MongoDB
        # temperature.save()

        # Mysql DB
        temperature.save(using='mysql_db')

    # if is_saved != None:

    # Arduino_Temperature.objects.contains
    #   cities_ref = db.collection(u'cities_temperature')
    #   docs = cities_ref.stream()
    #   for city in docs:
    #       print(f'{city.id} => {city.to_dict()}')

    #   # cities = TemperatureCity.objects.all()
    list_weather = Arduino_Temperature.objects.using(
        'mysql_db').all().order_by('-id')[:10]

    #   list_weather = []

    #   my_api_key = '3cebd2fe51f0c0bdbd71f6cdba4e1306'
    #   for city in cities:
    #       city_weather = requests.get(url.format(city, my_api_key)).json()

    #       getcontext().prec = 4
    #       temperature = (
    #           Decimal(city_weather['main']['temp']) - 32) * Decimal(5/9)

    #       weather = {
    #           'city': city,
    #           'temperature': temperature,
    #           'description': city_weather['weather'][0]['description'],
    #           'icon': city_weather['weather'][0]['icon']
    #       }
    #       list_weather.append(weather)

    context = {
        'list_weather': list_weather,
        # 'form': form
    }
    return render(request, 'arduino_temperature/index.html', context)
