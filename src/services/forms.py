from django import forms
from services.models import ServiceRecord, TyreRecord

class FileUploadForm(forms.ModelForm):
    class Meta:
        model  = ServiceRecord
        fields = '__all__'

class TyreServiceForm(forms.ModelForm):
    class Meta:
        model  = TyreRecord
        fields = '__all__'
