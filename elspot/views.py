from django.shortcuts import render
from plotly.offline import plot
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import numpy as np
from devices.models import Price
import datetime as dt
import decimal

from elspot.models import Price_week

def update_elspot(flag):
# --get date/time/price-------------------------------
    aDat = Price.objects.last()
    aDatweek = Price_week.objects.last()
    date_field = getattr(aDat, 'date')
    
    date_field_week = getattr(aDatweek, 'date')
    lista = request_elspot()
    

    price_avg=0
    only_time = request_time(lista)
    only_price = request_price(lista) 
    if date_field.day==dt.date.today().day: 
        
        print(date_field.day)
        print(dt.date.today().day)
    else:
        for t,p in zip(only_time,only_price):
            tmp = Price.objects.create(
                time = t,
                price = p 
            )
            tmp.save()
    
    try: 
        date_field_week.day==dt.date.today().day
        print(date_field_week.day)
    except:    
        for p in only_price:
            price_avg += decimal.Decimal(p)
        price_avg/=24
        tmp = Price_week.objects.create(
            date=dt.date.today(),
            price=price_avg
        )
        tmp.save()
        print(price_avg)
    if flag == 0:
        superlist=[only_time,only_price,date_field,price_avg]
        return superlist

def getPrices(request):
    time_price_date = update_elspot(0)

    def graph_price():
        x1 = np.asarray(time_price_date[0])
        y1 = np.asarray(time_price_date[1], np.dtype(float))
        y2 = np.asarray(time_price_date[3], np.dtype(float))
        
        fig = px.bar(x=x1,y=y1, labels={'x': 'Time', 'y': "Price (öre/kWh)"})
        
        fig.update_layout(title=str(time_price_date[2]), width=1600, height=630, bargap=0.5,
                            yaxis=dict(showgrid=True, zeroline=True, gridcolor='rgba(230,230,230,0.85)'), 
                            plot_bgcolor='rgba(240,240,240,0.75)',
                            hovermode='x unified', xaxis=dict(showgrid=False),
                                hoverlabel=dict(bgcolor='rgba(255,255,255,0.45)',
                                            font=dict(color='black', size=15)))
                                            #add date as title?
        
        fig.update_traces(marker_color='DarkSlateGrey', opacity=0.7)
     
        plot_div = plot(fig, output_type='div', include_plotlyjs=False)
        return plot_div    

    return render(request, 'elspot/getprices.html', {
        'plot_price': graph_price(),
        'only_times': list(time_price_date[0]),
        'only_prices': list(time_price_date[1]),
    })
# ----------------------------------------------------
import requests
from bs4 import BeautifulSoup

# --scrape elspot.nu----------------------------------
def request_elspot():
    page = requests.get('https://elspot.nu/dagens-spotpris/timpriser-pa-elborsen-for-elomrade-se3-stockholm/')
    parsed_info = BeautifulSoup(page.content, 'html.parser')
    aSection = parsed_info.find(id="elspot-history")
    
    lista = aSection.find_all('td')
    return lista

# --filter prices ------
def request_price(lista):
    price_str = lista[1::2]
    all_price = looping_loui(price_str,0,0)
    only_price = looping_loui(all_price,0,2)
    price_tmp = []
    for item in only_price:
        price_tmp.append(item.replace(",","."))
    return price_tmp

# --filter timestamps -
def request_time(lista):
    time_str = lista[0::2]
    all_time = looping_loui(time_str,0,0)
    only_time = looping_loui(all_time,1,2)
    return list(only_time)

# --looping for filters-------
def looping_loui(aList,s1,s3):

    newList = []
    if s3==0:
        for item in aList:
            newList.append(item.text.split())  
    else: 
        for item in aList:
            newList += item[s1::s3]
    return newList
