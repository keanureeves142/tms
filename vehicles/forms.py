from django import forms
from .models import Vehicle, Driver, Trip, AdhocCost
from django_select2.forms import ModelSelect2Widget


class VehicleForm(forms.ModelForm):
    class Meta:
        model = Vehicle
        fields = '__all__'
        widgets = {
            'vehicle_type': forms.Select(attrs={'class': 'form-control'}),
            'status': forms.Select(attrs={'class': 'form-control'}),
            'vehicle_number': forms.TextInput(attrs={'class': 'form-control'}),
            'avg_speed_per_hour': forms.NumberInput(attrs={'class': 'form-control'}),
            'cost': forms.NumberInput(attrs={'class': 'form-control'}),
            'commission_date': forms.TextInput(attrs={'class': 'form-control datepicker'}),
        }

class DriverForm(forms.ModelForm):
    class Meta:
        model = Driver
        fields = '__all__'
        widgets = {
            'driver_id': forms.TextInput(attrs={'class': 'form-control', 'readonly': 'readonly'}),
            'driver_name': forms.TextInput(attrs={'class': 'form-control'}),
            'salary_pm': forms.TextInput(attrs={'class': 'form-control'}),
            'driver_contact':forms.NumberInput(attrs={'class': 'form-control'}),
            'driver_status': forms.Select(attrs={'class': 'form-control'}),
        }

class TripForm(forms.ModelForm):
    class Meta:
        model = Trip
        fields = [
            'start_point', 'end_point', 'load', 'margin', 'start_time', 'trip_time', 
            'driver_allowance', 'no_restriction_timezone', 'driver'
        ]
        widgets = {
            'start_time': forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'}),
            'trip_time': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'driver_allowance': forms.NumberInput(attrs={'class': 'form-control'}),
            'margin': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'load': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'no_restriction_timezone': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'driver': ModelSelect2Widget(
                model=Driver,
                search_fields=['driver_contact__icontains'],  # Searchable by driver name
                attrs={'class': 'form-control'}
            ),
            #'vehicle': ModelSelect2Widget(
            #    model=Vehicle,
            #    search_fields=['vehicle_number__icontains'],  # Searchable by vehicle number
            #    attrs={'class': 'form-control'}
            #),
        }

class AdhocCostForm(forms.ModelForm):
    class Meta:
        model = AdhocCost
        fields = ['cost', 'cost_type']
        widgets = {
            'cost': forms.NumberInput(attrs={'class': 'form-control'}),
            'cost_type': forms.Select(attrs={'class': 'form-control'}),
        }