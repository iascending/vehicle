from django.views import generic
from django.http import HttpResponseForbidden
from django.urls import reverse_lazy
from django.shortcuts import render
from django.db.models import Q
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin

from services.models import TyreRecord, ServiceRecord
from services.forms import FileUploadForm, TyreServiceForm
from django.core.mail import EmailMessage

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

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.save()
        title = str(self.object.car) + " serviced"
        email = EmailMessage(title, '', to=['email@address.yourreminder.sendto'])
        email.send()
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

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.save()
        title = str(self.object.car) + " tyres serviced"
        email = EmailMessage(title, '', to=['email@address.yourreminder.sendto'])
        email.send()
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
