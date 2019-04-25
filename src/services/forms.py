from django import forms
from services.models import ServiceRecord, TyreRecord

class FileUploadForm(forms.ModelForm):
    class Meta:
        model  = ServiceRecord
        fields = '__all__'
    # def __init__(self, *args, **kwargs):
    #     current_driver = kwargs.pop('driver')
    #     super(FileUploadForm, self).__init__(*args, **kwargs)
    #     self.fields['car'].queryset = Car.objects.filter(rego__exact=self.request.)

class TyreServiceForm(forms.ModelForm):
    class Meta:
        model  = TyreRecord
        fields = '__all__'
