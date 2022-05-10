
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import numpy as np
import pandas as pd
import datetime as dt
from django_pandas.io import read_frame
from django_pandas.managers import DataFrameManager

import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'projekt2.settings')
django.setup()
from devices.models import Sector, SectorConsumption

#t_hours = pd.Series(pd.date_range("2022-04-27", periods=24, freq="h"))
#print(t_hours)

aSectors = SectorConsumption.objects.all()

df1 = aSectors.to_dataframe(['date','power_consumption'], index_col='sector')
#aSectors.to_fields()
print(df1)

#df = px.data.stocks()
#fig = px.line(df1, x='date', y=df1.columns,
#              hover_data={"date": "|%B %d, %Y"},
#              title='custom tick labels')
#fig.update_xaxes(
#    dtick="M1",
#    tickformat="%H:%M\n%Y")
#fig.show()

#print(df)