from django import forms
from .models import PowerConsumption, Device


class Receive_data(forms.Form):
    class Meta:
        model = PowerConsumption
        fields = ['power_consumed']

class update_powerlevel(forms.ModelForm):
    class Meta:
        model = Device
        fields = ['power_level']
