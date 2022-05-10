from django.shortcuts import render
from devices.models import *
from devices.views import *
from datetime import time
import datetime as dt
from elspot.models import Price_week
from mqtt_pub import main as publ

def device_auto_PL():
    print("Enter device_auto_PL...")

    price = get_price_now()
    power_query = Device.objects.all()
    powah = 0
    price_avg = Price_week.objects.get(date=dt.date.today())
    if price<price_avg:
        powah = 1
    elif price<(2*price_avg):
        powah = 0.75
    else:
        powah = 0.5

    for pl in power_query:
        Device.objects.filter(id=pl.id).update(
            power_level = powah
        )
    #publ()
    print("...Exit device_auto_PL")
def receive_data(topic, payload):
    #power = decimal.Decimal('%d.%d' % (random.randint(5,10) , random.randint(0,999)))
    #print('0'+str(dt.datetime.now().hour))
    dev_id = Device.objects.first().id
    
    priceNow = get_price_now()
    
    #save_device_consumption(dev_id, payload, priceNow)
    #save_sector_consumption(topic, payload, priceNow)
    
    if dt.datetime.now().minute == time(0).strftime("%M"):
        device_auto_PL()

def price_next_hr():
    tdelta = dt.timedelta(hours=1)
    try:
        priceNow = Price.objects.filter(date=str(dt.date.today())).get(time=str(dt.datetime.now().hour + tdelta)).price
    except:
        priceNow = Price.objects.filter(date=str(dt.date.today())).get(time='0'+str(dt.datetime.now().hour + tdelta)).price
    return priceNow