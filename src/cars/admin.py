from django.contrib import admin
from cars.models import Car, Driver, DrivingRecord
from import_export import resources
from import_export.admin import ImportExportModelAdmin

# Register your models here.
class CarResource(resources.ModelResource):
    class Meta:
        model = Car
        skip_unchanged = True
        report_skipped = False

class DriverResource(resources.ModelResource):
    class Meta:
        model = Driver
        skip_unchanged = True
        report_skipped = False

class DrivingRecordResource(resources.ModelResource):
    class Meta:
        model = DrivingRecord
        skip_unchanged = True
        report_skipped = False

class CarAdmin(ImportExportModelAdmin):
    resource_class = CarResource
    list_display  = ('rego', 'make', 'year', 'model', 'transmission')
    list_filter   = ['rego', 'year', 'transmission']
    search_fields = ['rego', 'make', 'year']

class DriverAdmin(ImportExportModelAdmin):
    resource_class = DriverResource
    list_display  = ['name', 'mobile', 'email', 'dept']
    list_filter   = ['name', 'mobile', 'dept']
    search_fields = ['name', 'mobile', 'dept']
    list_editable = ['mobile', 'dept']

class DrivingRecordAdmin(ImportExportModelAdmin):
    resource_class = DrivingRecordResource
    list_display  = ['driver', 'car', 'start_date', 'end_date', 'created_at']
    list_filter   = ['driver', 'car', 'created_at']
    search_fields = ['driver', 'car']
    list_editable = ['start_date', 'end_date']

admin.site.register(Car, CarAdmin)
admin.site.register(Driver, DriverAdmin)
admin.site.register(DrivingRecord, DrivingRecordAdmin)
