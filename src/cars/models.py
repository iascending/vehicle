import os
from functools import partial
from django import forms
from django.db import models
from django.db.models import Q
from django.urls import reverse

# Create your models here.
YEARS  = [(str(x), str(x)) for x in range(2008, 2020)]
class Car(models.Model):

    def get_contract_upload_path(instance, filename):
        file_name, file_extension = os.path.splitext(filename)
        return 'contracts/{0}_{1}{2}'.format(instance.rego, instance.lease_start_date, file_extension)

    make               = models.CharField(max_length=128)
    year               = models.CharField(max_length=32, choices=YEARS, default='2016')
    model              = models.CharField(max_length=128)
    type               = models.CharField(max_length=256)
    color              = models.CharField(max_length=64, default='White')
    rego               = models.CharField(max_length=128, unique=True)
    engine_no          = models.CharField(max_length=256, unique=True)
    vin                = models.CharField(max_length=256, unique=True)
    transmission       = models.CharField(max_length=256)
    options            = models.CharField(max_length=256, blank=True)
    maintenance_status = models.CharField(max_length=256)
    lease_start_date   = models.DateField(default='2018-02-14')
    lease_term         = models.PositiveIntegerField(default=36)
    rental             = models.DecimalField(max_digits=10, decimal_places=2, default=1500)
    distance_restrict  = models.DecimalField(max_digits=10, decimal_places=2, default=210000)
    start_odometer     = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    excess_kmcharge    = models.DecimalField(max_digits=10, decimal_places=2, default=0.12)
    default_interest   = models.DecimalField(max_digits=10, decimal_places=2, default=0.18)
    LESSOR_CHOICES     = ( ('S', 'Street Fleet'), ('P', 'PRS Owned'), )
    lessor             = models.CharField(max_length=8, choices=LESSOR_CHOICES, default='S')
    STATUS_CHOICES     = ( ('A', 'Active'), ('S', 'In Service'), ('I', 'In Idle'), )
    status             = models.CharField(max_length=8, choices=STATUS_CHOICES, default='A')
    rego_exp           = models.DateField(default='2019-06-30')
    insurer            = models.CharField(max_length=128, default='AAMI')
    policy_num         = models.CharField(max_length=128, default='P12345678')
    insurance_exp      = models.DateField(default='2019-06-30')
    fuel_efficiency    = models.DecimalField(max_digits=10, decimal_places=2, default=10)
    contract           = models.FileField(upload_to=get_contract_upload_path)
    file_upload_date   = models.DateField(auto_now=True)

    def __str__(self):
        return self.rego


    # def get_absolute_url(self):
    #     return reverse("cars:single_car", kwargs={"pk": self.pk})

    class Meta:
        ordering = ['rego']


class Driver(models.Model):
    name         = models.CharField(max_length=128)
    mobile       = models.CharField(max_length=32, unique=True)
    license      = models.CharField(max_length=128, default=1234567890)
    email        = models.CharField(max_length=256, null=True, default=None)
    DEPT_CHOICES = (
                      ('BG', 'Brown Goods'),
                      ('WG', 'White Goods'),
                      ('BL', 'Billing Team'),
                      ('AC', 'Accountants'),
                      ('CC', 'Call Center'),
                      ('IT', 'IT Department'),
                      ('MG', 'Management'),
                      ('SP', 'Spare Parts'),
                      ('HHP', 'Mobile Phones'),
                      ('BDM', 'Business Development'),
                   )
    dept       = models.CharField(max_length=8, choices=DEPT_CHOICES, default='BG')

    class Meta:
        unique_together = ('name', 'mobile', 'dept')
        ordering = ['name']

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("cars:single_driver", kwargs={"pk": self.pk})

class DrivingRecord(models.Model):
    driver      = models.ForeignKey(Driver, on_delete=models.CASCADE,related_name='driving_records')
    car         = models.ForeignKey(Car, on_delete=models.CASCADE, related_name='working_records')
    start_date  = models.DateTimeField()
    end_date    = models.DateTimeField(null=True, blank=True, editable=True)
    note        = models.CharField(max_length=512, blank=True, null=True, default="")
    created_at  = models.DateTimeField(auto_now=True)

    def get_absolute_url(self):
        return reverse("cars:drivingrecord_list")

    def clean(self):
        qs_stm_two_dates = Q(start_date__range=(self.start_date, self.end_date))|Q(end_date__range=(self.start_date, self.end_date))|(Q(start_date__lte=self.start_date) & Q(end_date__gte=self.end_date))
        qs_old_end_empty = DrivingRecord.objects.filter(car=self.car).exclude(pk=self.pk).filter(end_date__isnull=True)

        if not self.start_date:
            raise forms.ValidationError("start_date can not leave blank.")
        if self.end_date:
            if self.start_date > self.end_date:
                raise forms.ValidationError("end_date must be later than start_date.")

        if qs_old_end_empty:
            if self.end_date:
                qs_two_dat_exist = DrivingRecord.objects.filter(car=self.car).exclude(pk=self.pk).filter(qs_stm_two_dates)
                qs_old_ept_new_exist = qs_two_dat_exist | qs_old_end_empty.filter(Q(start_date__lte=self.end_date))
                if qs_old_ept_new_exist:
                    raise forms.ValidationError("Records already exist, datetime interval conflicts")
                # else:
                #     return self.full_clean()
            else:
                raise forms.ValidationError("Records already exist, please fill up end_date first")
        else:
            if self.end_date:
                qs_two_dat_exist = DrivingRecord.objects.filter(car=self.car).exclude(pk=self.pk).filter(qs_stm_two_dates)
                if qs_two_dat_exist:
                    raise forms.ValidationError("Records already exist, datetime interval conflicts")
                # else:
                #     return self.full_clean()
            else:
                qs_new_end_empty = DrivingRecord.objects.filter(car=self.car).exclude(pk=self.pk).filter(end_date__gte=self.start_date)
                if qs_new_end_empty:
                    raise forms.ValidationError("Records already exist, datetime interval conflicts")
                # else:
                #     return self.full_clean()

    class Meta:
        ordering = ['car', '-start_date']
