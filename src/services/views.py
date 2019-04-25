import pdb
from django.views import generic
from django.http import HttpResponseForbidden
from django.urls import reverse_lazy
from django.shortcuts import render
from django.db.models import Q
from django.core.exceptions import PermissionDenied
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from bootstrap_datepicker_plus import DatePickerInput

from services.models import TyreRecord, ServiceRecord
from services.forms import FileUploadForm, TyreServiceForm

# from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from services.tasks import send_email_async

# Create your views here.
class NewService(LoginRequiredMixin, generic.CreateView):
    form_class = FileUploadForm
    success_url = reverse_lazy('services:service_list')
    template_name = "services/new_service.html"

    def user_perm_check(self, request):
        if request.user.has_perm('services.add_servicerecord'):
            return True
        return False

    def dispatch(self, request, *args, **kwargs):
        if not self.user_perm_check(request):
            raise PermissionDenied
        return super(NewService, self).dispatch(request, *args, **kwargs)

    def get_form(self):
        form = super().get_form()
        form.fields['last_service_at'].widget = DatePickerInput(format='%Y-%m-%d')
        form.fields['next_service_at'].widget = DatePickerInput(format='%Y-%m-%d')
        return form

    def get_email_context(self, form):
        subject  = "On vehicle service and maintainance"
        try:
            driver = form.cleaned_data['car'].working_records.latest('start_date').driver.name
        except:
            driver = "nobody"
        try:
            qs = ServiceRecord.objects.filter(car__exact=form.cleaned_data['car']).order_by('-last_service_at')
            prev_date = qs[1].last_service_at
            prev_odos = qs[1].last_odometer_reading
            distance  = int(form.cleaned_data['last_odometer_reading']) - int(prev_odos)
        except:
            prev_date = None
            prev_odos = None
            distance  = None

        context = { 'user': self.request.user,
                    'make': form.cleaned_data['car'].make,
                    'car' : form.cleaned_data['car'].rego,
                    'type': form.cleaned_data['car'].type.lower(),
                    'prev_date': prev_date,
                    'curr_date': form.cleaned_data['last_service_at'],
                    'curr_drvr': driver,
                    'prev_odos': prev_odos,
                    'curr_odos': form.cleaned_data['last_odometer_reading'],
                    'distance':  distance
                  }
        # pdb.set_trace()
        html_message = render_to_string('services/car_service_email.html',
                                         context, request=self.request)
        plain_message= strip_tags(html_message)
        return subject, plain_message, html_message

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.save()
        subject, plain_message, html_message = self.get_email_context(form)
        send_email_async.delay(subject, plain_message, html_message)
        return super().form_valid(form)

class ServiceList(generic.ListView):
    paginate_by = 100
    template_name = 'services/service_list.html'
    context_object_name='service_list'

    def get_queryset(self):
        query = self.request.GET.get('search')
        order_by = self.request.GET.get('order_by')
        if not order_by:
            qs = ServiceRecord.objects.all().order_by('car__rego', '-last_service_at')
        else:
            qs = ServiceRecord.objects.all().order_by(order_by)
        if query is not None:
            search_condition = Q(car__rego__icontains=query)|Q(last_service_at__icontains=query)
            return qs.filter(search_condition)
        else:
            return qs

    def get_context_data(self, **kwargs):
        context = super(ServiceList, self).get_context_data(**kwargs)
        paginator = Paginator(self.get_queryset(), self.paginate_by)
        page = self.request.GET.get('page')
        try:
            servicerecord_page = paginator.page(page)
        except PageNotAnInteger:
            servicerecord_page = paginator.page(1)
        except EmptyPage:
            servicerecord_page = paginator.page(paginator.num_pages)
        context['service_list'] = servicerecord_page
        return context

class NewTyreService(LoginRequiredMixin, generic.CreateView):
    form_class = TyreServiceForm
    success_url = reverse_lazy('services:tyre_service_list')
    template_name = "services/new_tyre_service.html"

    def user_perm_check(self, request):
        if request.user.has_perm('services.add_tyrerecord'):
            return True
        return False

    def dispatch(self, request, *args, **kwargs):
        if not self.user_perm_check(request):
            raise PermissionDenied
        return super(NewTyreService, self).dispatch(request, *args, **kwargs)

    def get_form(self):
        form = super().get_form()
        form.fields['last_service_at'].widget = DatePickerInput(format='%Y-%m-%d')
        return form

    def get_email_context(self, form):
        subject  = "On vehicle tyre repairing and replacing"
        try:
            driver = form.cleaned_data['car'].working_records.latest('start_date').driver.name
        except:
            driver = "nobody"
        try:
            qs = TyreRecord.objects.filter(car__exact=form.cleaned_data['car']).order_by('-last_service_at')
            prev_date = qs[len(qs)-1].last_service_at
        except:
            prev_date = None
        try:
            qs = TyreRecord.objects.filter(car__exact=form.cleaned_data['car']).order_by('-last_service_at')
            tyre_chng = sum([qs[i].number for i in range(len(qs))])
        except:
            tyre_chng = None

        context = { 'user': self.request.user,
                    'make': form.cleaned_data['car'].make,
                    'type': form.cleaned_data['car'].type.lower(),
                    'car' : form.cleaned_data['car'].rego,
                    'prev_date': prev_date,
                    'curr_date': form.cleaned_data['last_service_at'],
                    'curr_drvr': driver,
                    'tyre_chng': tyre_chng
                  }
        # pdb.set_trace()
        html_message = render_to_string('services/tyre_service_email.html',
                                         context, request=self.request)
        plain_message= strip_tags(html_message)
        return subject, plain_message, html_message

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.save()
        subject, plain_message, html_message = self.get_email_context(form)
        send_email_async.delay(subject, plain_message, html_message)
        return super().form_valid(form)

class TyreServiceList(generic.ListView):
    paginate_by = 100
    template_name = 'services/tyre_service_list.html'
    context_object_name='tyre_service_list'

    def get_queryset(self):
        query = self.request.GET.get('search')
        order_by = self.request.GET.get('order_by')
        if not order_by:
            qs = TyreRecord.objects.all().order_by('car__rego', '-last_service_at')
        else:
            qs = TyreRecord.objects.all().order_by(order_by)
        if query is not None:
            search_condition = Q(car__rego__icontains=query)|Q(last_service_at__icontains=query)
            return qs.filter(search_condition)
        else:
            return qs

    def get_context_data(self, **kwargs):
        context = super(TyreServiceList, self).get_context_data(**kwargs)
        paginator = Paginator(self.get_queryset(), self.paginate_by)
        page = self.request.GET.get('page')
        try:
            servicerecord_page = paginator.page(page)
        except PageNotAnInteger:
            servicerecord_page = paginator.page(1)
        except EmptyPage:
            servicerecord_page = paginator.page(paginator.num_pages)
        context['tyre_service_list'] = servicerecord_page
        return context
