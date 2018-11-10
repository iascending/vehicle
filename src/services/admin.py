from django.contrib import admin
from services.models import TyreRecord, ServiceRecord
from import_export import resources
from import_export.admin import ImportExportModelAdmin

# Register your models here.
class ServiceRecordResource(resources.ModelResource):
    class Meta:
        model = ServiceRecord
        skip_unchanged = True
        report_skipped = False

class ServiceRecordAdmin(ImportExportModelAdmin):
    resource_class = ServiceRecordResource
    list_display  = ['car', 'last_service_at', 'next_service_at', 'last_odometer_reading', 'next_odometer_reading', 'last_service_provider', 'service_report', 'file_upload_date']
    list_filter   = ['car', 'last_service_at', 'next_service_at', 'last_odometer_reading', 'next_odometer_reading', 'last_service_provider', 'service_report', 'file_upload_date']
    search_fields = ['car', 'last_service_at', 'next_service_at', 'last_odometer_reading', 'next_odometer_reading', 'last_service_provider', 'service_report', 'file_upload_date']
    list_editable = ['last_service_at', 'next_service_at', 'last_odometer_reading', 'next_odometer_reading', 'last_service_provider', 'service_report']

# Register your models here.
class TyreServiceRecordResource(resources.ModelResource):
    class Meta:
        model = TyreRecord
        skip_unchanged = True
        report_skipped = False

class TyreServiceRecordAdmin(ImportExportModelAdmin):
    resource_class = TyreServiceRecordResource
    list_display  = ['car', 'service_type', 'tyre_position', 'number', 'last_service_at', 'service_report']
    list_filter   = ['car', 'service_type', 'tyre_position', 'number', 'last_service_at', 'service_report']
    search_fields = ['car', 'service_type', 'tyre_position', 'number', 'last_service_at', 'service_report']
    list_editable = ['service_type', 'tyre_position', 'number', 'last_service_at', 'service_report']

admin.site.register(ServiceRecord, ServiceRecordAdmin)
admin.site.register(TyreRecord, TyreServiceRecordAdmin)
