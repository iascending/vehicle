import os
from django.db import models

# Create your models here
class ServiceRecord(models.Model):

    def get_contract_upload_path(instance, filename):
        file_name, file_extension = os.path.splitext(filename)
        return 'reports/{0}_{1}{2}'.format(instance.car, instance.last_service_at, file_extension)

    car = models.ForeignKey('cars.car', on_delete=models.CASCADE, related_name='service_history')
    last_service_at = models.DateField(default='2018-11-05')
    next_service_at = models.DateField(default='2019-02-20')
    last_odometer_reading=models.PositiveIntegerField(default=15000)
    next_odometer_reading=models.PositiveIntegerField(default=30000)
    last_service_provider=models.CharField(max_length=256, default='Volkwagon Glen Waverley')
    service_report=models.FileField(upload_to=get_contract_upload_path)
    file_upload_date=models.DateField(auto_now_add=True)

class TyreRecord(models.Model):

    def get_contract_upload_path(instance, filename):
        file_name, file_extension = os.path.splitext(filename)
        return 'reports/{0}_{1}{2}'.format(instance.car, instance.last_service_at, file_extension)

    car = models.ForeignKey('cars.car', on_delete=models.CASCADE, related_name='tyre_history')
    SERVICE_CHOICES  = ( ('Repair', 'Repaired'), ('Replace', 'Replaced'), )
    service_type     = models.CharField(max_length=32, choices=SERVICE_CHOICES, default='Repair')
    POSITION_CHOICES = ( ('FL', 'Front Left'), ('FR', 'Front Right'),
                         ('RL', 'Rear Left'),  ('RR', 'Rear Right'),
                         ('FT', 'Front Two'),  ('RT', 'Rear Two'), ('A', 'All'),
                       )
    tyre_position    = models.CharField(max_length=32, choices=POSITION_CHOICES, default='A')
    number           = models.PositiveIntegerField(default=4)
    last_service_at  = models.DateField(default='2018-11-05')
    service_report   = models.FileField(upload_to=get_contract_upload_path)
    file_upload_date = models.DateField(auto_now_add=True)
