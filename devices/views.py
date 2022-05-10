from django.shortcuts import render,redirect

from devices.forms import update_powerlevel
from elspot.views import update_elspot
from .models import *
from dashboard.views import dashboard
import datetime as dt
import random, decimal
from django.db.models import Sum

from mqtt_pub import main as publ

from plotly.offline import plot
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import numpy as np

def get_price_now():
    try: 
        Price.objects.get(date=dt.datetime.today())
        print("elspot no update necessary.")
    except: 
        update_elspot(1)
        print("elspot updated.")
    try:
        priceNow = Price.objects.filter(date=str(dt.date.today())).get(time=str(dt.datetime.now().hour)).price
    except:
        priceNow = Price.objects.filter(date=str(dt.date.today())).get(time='0'+str(dt.datetime.now().hour)).price
    return priceNow

def save_device_consumption(pk, power, priceNow):
    pwr=decimal.Decimal(power)
    new_d_power = PowerConsumption.objects.create(
        device_id = pk,
        datetime = dt.datetime.now(),
        power_consumed = pwr,
        cost = (priceNow*pwr),
    )
    new_d_power.save()
    print("Price now: ", priceNow)

def save_sector_consumption(pk, power, priceNow):
    pwr=decimal.Decimal(power)
    obj = SectorConsumption.objects.create(
        sector_id = pk,
        datetime = dt.datetime.now(),
        power_consumed = pwr,
        cost = (priceNow*pwr),
    )
    obj.save()
    

def sector_consumption(topic):
    s_id = Device.objects.get(id=topic).sector.id
    d = Device.objects.filter(sector_id=s_id)
    sum_pwr=sum_cost=0
    
    for i in d:
        try:
            sum_pwr += PowerConsumption.objects.filter(device_id=i.id).last().power_consumed
            sum_cost += PowerConsumption.objects.filter(device_id=i.id).last().cost
        except:
            pass
    obj = save_sector_consumption(s_id,sum_pwr,sum_cost)
    return obj

def sector_only_consumption(topic, payload):
    priceNow = get_price_now()
    save_sector_consumption(topic, payload, priceNow)

def devices(requests):
    devices = Device.objects.all().order_by('sector')

    return render(requests, 'devices/devices.html',
        {            
            'devices': list(devices),      
        }
    )

def device_PL(request, pk):
    #powerlevel = decimal.Decimal('%d.%d' % (0 , random.randint(0,99)))
    
    powerlevel = Device.objects.get(id=pk)
    sektorid = powerlevel.sector.id
    form = update_powerlevel(instance=powerlevel)
    if request.method == 'POST':
        form = update_powerlevel(request.POST, instance=powerlevel)
        if form.is_valid:
            form.save()
            print("hello")
            #publ()
            return redirect('/devices/device_graph/{}/'.format(sektorid))
        else:
            print("hej")
            form=update_powerlevel()
    
    return render(request, 'devices/update_device.html', {'form': form})

def device_history(request,pk):
    devices = Device.objects.filter(sector__id=pk).order_by('id')
    sector = devices.first().sector
    d_pc = PowerConsumption.objects.filter(device_id=devices.first().id).order_by('datetime')
    #sector = Device.objects.first().sector
    xx1 = []
    yy1 = []
    yy2 = []
    for x in d_pc:
        xx1.append(getattr(x, 'datetime').strftime('%H:%M:%S'))
        yy1.append(getattr(x, 'power_consumed'))
        yy2.append(getattr(x, 'cost'))
    
# --plotly graph--
    def scatter():
        x1 = xx1
        y1 = yy1
        y2 = yy2
        fig = make_subplots(specs=[[{"secondary_y": True}]])
        
        fig.add_trace(
            go.Scatter(x=x1, y=y1, name="Power", mode='lines', marker_color='rgb(25,25,112)'),
            secondary_y=False,
        )
        fig.add_trace(
            go.Scatter(x=x1, y=y2, name="Price", mode='lines', marker_color= 'rgb(189,183,107)', opacity=0.4),
            secondary_y=True,
        )
        t_hours = ['00','01','02','03','04','05','06','07','08','09','10','11','12','13','14','15','16','17','18','19','20','21','22','23']

        fig.update_layout(width=1300, height=700,
                            xaxis=dict(showgrid=False, zeroline=True, gridcolor='black', showticklabels=False),
                            yaxis=dict(showgrid=True, zeroline=True, gridcolor='rgba(240,240,240,0.85)', rangemode='tozero'),
                            yaxis2=dict(showgrid=True, zeroline=True, rangemode='tozero'),
                            plot_bgcolor='rgba(240,240,240,0.5)',
                            #paper_bgcolor='rgba(0,0,0,0)',
                            hovermode='x unified', hoverlabel=dict(bgcolor='rgba(250,250,250,0.85)',
                                                                        font=dict(color='black')))
        
        fig.update_yaxes(title_text="<b>Power Consumption</b> kWh", secondary_y=False)
        fig.update_yaxes(title_text="<b>Price per kWh</b> Kr/kWh", secondary_y=True)
        
        plot_div = plot(fig, output_type='div', include_plotlyjs=False)
        return plot_div


    return render(request, 'devices/device_graph.html',
        {
            'plot': scatter(),
            'devices': devices,
            'device': sector,
            'pwr_cost': list(d_pc)

            
        }
    )