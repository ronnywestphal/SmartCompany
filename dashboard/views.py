from django.shortcuts import render
from devices.models import *
from django.db.models import Sum
from itertools import chain
from plotly.offline import plot
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import numpy as np
import pandas as pd
import datetime as dt


def dashboard(requests):

    sectors = Sector.objects.all()
    sum_pwr=sum_cost=0
    q_pwr_cst=[]

# --loop through sectors and grab pwr+cost from each
    for x in sectors:
        d = Device.objects.filter(sector_id=x.id)
        for y in d:
            sum_pwr += PowerConsumption.objects.filter(device_id=y.id).last().power_consumed
            sum_cost += PowerConsumption.objects.filter(device_id=y.id).last().cost
        q_pwr_cst.append([sum_pwr, sum_cost])
    
    s_con = SectorConsumption.objects.all()
    s1_time=[]
    s1_pwr=[]
    s1_cost=[]
    for i in s_con.filter(sector__name='Sektor 1').order_by('datetime'):
        s1_time.append(i.datetime.strftime('%H:%M:%S'))
        s1_pwr.append(i.power_consumed)
        s1_cost.append(i.cost)
    s2_time=[]
    s2_pwr=[]
    s2_cost=[]
    for i in s_con.filter(sector__name='Sektor 2').order_by('datetime'):
        s2_time.append(i.datetime)
        s2_pwr.append(i.power_consumed)
        s2_cost.append(i.cost)
    s3_time=[]
    s3_pwr=[]
    s3_cost=[]
    for i in s_con.filter(sector__name='Sektor 3').order_by('datetime'):
        s3_time.append(getattr(i, 'datetime').strftime('%H:%M:%S'))
        s3_pwr.append(i.power_consumed)
        s3_cost.append(i.cost)
    s4_time=[]
    s4_pwr=[]
    s4_cost=[]
    for i in s_con.filter(sector__name='Sektor 4').order_by('datetime'):
        s4_time.append(i.datetime)
        s4_pwr.append(i.power_consumed)
        s4_cost.append(i.cost)
    s1 = Sector.objects.get(name='Sektor 2')
    print(getattr(s1, 'id'))
#---plotly graph--
    def scatter():

        x1 = s1_time 
        y1 = s1_pwr
        y11 = s1_cost
        x2 = s2_time
        y2 = s2_pwr
        y22 = s2_cost
        x3 = s3_time
        y3 = s3_pwr
        y33 = s3_cost
        x4 = s4_time
        y4 = s4_pwr
        y44 = s4_cost
        
        fig = make_subplots(rows=2, cols=2)
       
        t_hours = pd.array(pd.date_range("2022-04-27", periods=24, freq="h").strftime('%Y-%m-%d %H:%M:%S'))
        
        #print(t_hours)
        #t_hours = pd.array['00:00','01:00','02:00','03:00','04:00','05:00','06:00','07:00','08:00','09:00','10:00','11:00','12:00','13:00','14:00','15:00','16:00','17:00','18:00','19:00','20:00','21:00','22:00','23:00']
        t_hourss = [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23]
        #df = pd.DataFrame({'x_data':x1, 'y_data':y1})
        fig.add_trace(
            go.Scatter(x=x1, y=y1, name="Power S1", mode='lines', marker_color='black'),
            row=1,col=1
            
        )
        '''fig.add_trace(
            go.Bar(x=y11, y=y11, row=1,col=1,name="Cost S1", marker_color= 'black', opacity=0.3),
            
        )'''
        fig.add_trace(
            go.Scatter(x=x2, y=y2,name="Power S2", mode='lines', marker_color= 'blue'),
            row=1,col=2
        )
        '''fig.add_trace(
            go.Bar(x=y11, y=y22, row=1,col=2, name="Cost S2", marker_color= 'blue', opacity=0.3),
            
        )'''
        fig.add_trace(
            go.Scatter(x=x3, y=y3, name="Power S3", mode='lines', marker_color='yellow'),
            row=2,col=1
        )
        '''fig.add_trace(
            go.Bar(x=y11, y=y33, row=2,col=1, name="Cost S3", marker_color= 'yellow', opacity=0.3),
            
        )'''
        fig.add_trace(
            go.Scatter(x=x4, y=y4, name="Power S4", mode='lines', marker_color= 'green'),
            row=2,col=2
        )
        '''fig.add_trace(
            go.Bar(x=y11, y=y44, row=2,col=2, name="Cost S4", marker_color= 'green', opacity=0.3),
            
        )'''
        '''myRange=[0,24]
        for ax in fig['layout']:
            if ax[:23]=='xaxis':
                fig['layout'][ax]['range']=myRange'''
        fig.update_xaxes(showgrid=False, gridcolor='black', showticklabels=True)
        fig.update_yaxes(showgrid=True, gridcolor='rgba(230,230,230,0.85)', rangemode='tozero')
        fig.update_layout(width=1800, height=650, 
                            plot_bgcolor='rgba(240,240,240,0.75)',
                            hovermode='x unified', hoverlabel=dict(bgcolor='rgba(250,250,250,0.85)',
                                                                        font=dict(color='black')))
        
        fig.update_yaxes(title_text="<b>Power Consumption</b> kWh")

        #fig.update_yaxes(title_text="<b>Price per kWh</b> Kr/kWh", 
        
        plot_div = plot(fig, output_type='div', include_plotlyjs=False)
        return plot_div

    sector1 = Sector.objects.get(name='Sektor 1')
    sector2 = Sector.objects.get(name='Sektor 2')
    sector3 = Sector.objects.get(name='Sektor 3')
    sector4 = Sector.objects.get(name='Sektor 4')
    dev_sec_1 = Device.objects.filter(sector__name=sector1.name)
    dev_sec_2 = Device.objects.filter(sector__name=sector2.name)
    dev_sec_3 = Device.objects.filter(sector__name=sector3.name)
    dev_sec_4 = Device.objects.filter(sector__name=sector4.name)
    return render(requests, 'dashboard/dashboard.html',
        {
            'q_pwr_cst': q_pwr_cst,
            'plot_sectors': scatter(),
            'sectors': list(sectors),
            'dev_sec_1': list(dev_sec_1),
            'dev_sec_2': list(dev_sec_2),
            'dev_sec_3': list(dev_sec_3),
            'dev_sec_4': list(dev_sec_4),
            
        }
    )


def sector_consumption(pk,sum_pwr,sum_cost):
    obj = SectorConsumption.objects.create(
        sector_id = pk,
        datetime = dt.datetime.now(),
        power_consumed = sum_pwr,
        cost = sum_cost
    )
    return obj