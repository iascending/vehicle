from django import forms
from cars.models import Car, DrivingRecord
from bootstrap_datepicker_plus import DatePickerInput, DateTimePickerInput

class NewCarCreateForm(forms.ModelForm):
    class Meta:
        model = Car
        fields= '__all__'
        widgets = {
            'lease_start_date': DatePickerInput(format='%Y-%m-%d'),
            'rego_exp':         DatePickerInput(format='%Y-%m-%d'),
            'insurance_exp':    DatePickerInput(format='%Y-%m-%d'),
        }

class NewDrivingRecordForm(forms.ModelForm):
    class Meta:
        model = DrivingRecord
        fields= '__all__'
        widgets = {
            'start_date': DateTimePickerInput(format='%Y-%m-%d %H:%M'),
            'end_date':   DateTimePickerInput(format='%Y-%m-%d %H:%M'),
        }
