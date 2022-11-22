from django.shortcuts import render
import requests
from datetime import datetime,timedelta
from zoneinfo import ZoneInfo

from .models import Arduino_Temperature

from firebase_admin import firestore
from google.cloud import firestore


# Create your views here.
# Application Default credentials are automatically created.


# Use a service account.
db = firestore.Client(project='openweather-369402')


# Create your views here.

def index(request):

    # Lấy nhiệt độ từ Arduino về

    # api trả về kết quả là nhiệt độ mới nhất của arduino
    api_arduino = 'https://api.thingspeak.com/channels/1867718/feeds.json?api_key=0U6CXNXQPN70JVCQ&results=1'

    temperature = requests.get(api_arduino).json()

    last_id = temperature['channel']['last_entry_id']

    count = Arduino_Temperature.objects.filter(id=last_id).count()
    if count == 0:
        latest_temperature = temperature['feeds'][0]
        print('latest_temperature: ', latest_temperature)
        temperature = Arduino_Temperature()
        temperature.id = last_id

        # điều chỉnh lại ngày giờ
        # created_at_split_str = latest_temperature['created_at'].split()[:-1]  # Bỏ chữ Z ở cuối
        created_at_split_str = list(latest_temperature['created_at'])[:-1]  # Bỏ chữ Z ở cuối
        created_at_split_str = ''.join(created_at_split_str)
        separator = ''
        created_at_split_str = separator.join(created_at_split_str).split('T')
        date_split = created_at_split_str[0].split('-')

        print('date_split: ', date_split)

        hours_minutes_seconds_split = created_at_split_str[1].split(':')
        print('hours_minutes_seconds_split: ', hours_minutes_seconds_split)

        date_split_int = list(map(lambda x: int(x), date_split))
        hours_minutes_seconds_split_int = list(map(
            lambda x: int(x), hours_minutes_seconds_split))

        new_created_at = datetime(date_split_int[0],
                                  date_split_int[1],
                                  date_split_int[2],
                                  hours_minutes_seconds_split_int[0],
                                  hours_minutes_seconds_split_int[1],
                                  hours_minutes_seconds_split_int[2],
                                  tzinfo=ZoneInfo(key='Etc/GMT+7'))
        new_created_at = new_created_at.replace(tzinfo=ZoneInfo(key='Etc/GMT-7'))
        new_created_at = new_created_at + timedelta(hours=7)
        print('new created at: ', new_created_at)
        temperature.created_at = new_created_at
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
        temperature.save()

        # Mysql DB
        # temperature.save(using='mysql_db')

    # Mongo db
    list_weather = Arduino_Temperature.objects.all().order_by('-id')[:5]

    # Mysql
    # list_weather = arduino_temperature.objects.using(
    #     'mysql_db').all().order_by('-id')[:10]

    context = {
        'list_weather': list_weather,
    }
    return render(request, 'arduino_temperature/index.html', context)
