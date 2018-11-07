from django.views import generic
from django.http import HttpResponseForbidden
from django.urls import reverse_lazy
from django.utils import timezone
from django.shortcuts import render
from django.db.utils import OperationalError
from django.core.exceptions import PermissionDenied
from django.db.models import F, Q, Max, When, Case, Value, CharField
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin

from cars.forms import NewCarCreateForm
from cars.models import Car, Driver, DrivingRecord
from services.models import ServiceRecord

from django.contrib.auth import get_user_model
User = get_user_model()

class NewCar(LoginRequiredMixin, generic.CreateView):
    form_class = NewCarCreateForm
    success_url = reverse_lazy('cars:car_list')
    template_name = "cars/car_form.html"

    def user_perm_check(self, request):
        if request.user.has_perm('cars.add_car'):
            # self.object = self.get_object()
            return True
        return False

    def dispatch(self, request, *args, **kwargs):
        if not self.user_perm_check(request):
            raise PermissionDenied
        return super(NewCar, self).dispatch(request, *args, **kwargs)

    # def form_valid(self, form):
    #     self.object = form.save(commit=False)
    #     self.object.save()
    #     return super().form_valid(form)

class NewDriver(LoginRequiredMixin, generic.CreateView):
    fields = '__all__'
    model  = Driver
    template_name = 'cars/driver_form.html'

    def user_perm_check(self, request):
        if request.user.has_perm('cars.add_driver'):
            return True
        return False

    def dispatch(self, request, *args, **kwargs):
        if not self.user_perm_check(request):
            raise PermissionDenied
        return super(NewDriver, self).dispatch(request, *args, **kwargs)

    # def form_valid(self, form):
    #     self.object = form.save(commit=False)
    #     self.object.save()
    #     return super().form_valid(form)

class NewDrivingRecord(LoginRequiredMixin, generic.CreateView):
    fields = '__all__'
    model  = DrivingRecord
    template_name = 'cars/newdrivingrecord_form.html'

    def user_perm_check(self, request):
        if request.user.has_perm('cars.add_drivingrecord'):
            return True
        return False

    def dispatch(self, request, *args, **kwargs):
        if not self.user_perm_check(request):
            raise PermissionDenied
        return super(NewDrivingRecord, self).dispatch(request, *args, **kwargs)

    # def form_valid(self, form):
    #     self.object = form.save(commit=False)
    #     self.object.save()
    #     return super().form_valid(form)

class DrivingRecordUpdate(LoginRequiredMixin, generic.UpdateView):
    model = DrivingRecord
    fields = ['driver', 'car', 'start_date', 'end_date']
    template_name_suffix = '_update_form'

    def user_perm_check(self, request):
        if request.user.has_perm('cars.change_drivingrecord'):
            # self.object = self.get_object()
            return True
        return False

    def dispatch(self, request, *args, **kwargs):
        if not self.user_perm_check(request):
            raise PermissionDenied
        return super(DrivingRecordUpdate, self).dispatch(
            request, *args, **kwargs)

class DrivingRecordDelete(LoginRequiredMixin, generic.DeleteView):
    model = DrivingRecord
    success_url = reverse_lazy('cars:drivingrecord_list')

    def user_perm_check(self, request):
        if request.user.has_perm('cars.delete_drivingrecord'):
            # self.object = self.get_object()
            return True
        return False

    def dispatch(self, request, *args, **kwargs):
        if not self.user_perm_check(request):
            raise PermissionDenied
        return super(DrivingRecordDelete, self).dispatch(
            request, *args, **kwargs)

class ListCars(generic.ListView):
    paginate_by = 100
    default_ordering = 'rego'

    def get_queryset(self):
        query = self.request.GET.get('search')
        order_by = self.request.GET.get('order_by', self.default_ordering)
        max_set_driving = Car.objects.values('rego').prefetch_related('working_records').annotate(
                               latest_start_date=Max(F('working_records__start_date')),
                               latest_service_date=Max(F('service_history__last_service_at'))   )
        q_statement = Q()
        for pair in max_set_driving:
            q_statement |= (Q(rego__exact=pair['rego'])) & (Q(latest_start_date=pair['latest_start_date'])) \
                          & (Q(latest_service_date=pair['latest_service_date']))

        qs = Car.objects.prefetch_related('working_records').annotate(
                  latest_start_date= Max(F('working_records__start_date')),
                  latest_end_date  = F('working_records__end_date'),
                  current_driver = F('working_records__driver__name'),
                  latest_service_date = Max(F('service_history__last_service_at')),
                  latest_odometer_reading = F('service_history__last_odometer_reading'),
                 ).filter(q_statement).order_by(order_by)
        for item in qs:
            if (item.latest_end_date):
                if (item.latest_end_date <= timezone.now()):
                    item.current_driver = ''

        if query is not None:
            search_condition = Q(rego__icontains=query)|Q(current_driver__icontains=query)|Q(make__icontains=query)
            return qs.filter(search_condition)
        else:
            return qs

    def get_context_data(self, **kwargs):
        context = super(ListCars, self).get_context_data(**kwargs)
        paginator = Paginator(self.get_queryset(), self.paginate_by)

        page = self.request.GET.get('page')

        try:
            cars_page = paginator.page(page)
        except PageNotAnInteger:
            cars_page = paginator.page(1)
        except EmptyPage:
            cars_page = paginator.page(paginator.num_pages)

        context['car_list'] = cars_page
        return context

class ListDriver(generic.ListView):
    paginate_by = 100
    default_ordering = 'name'

    def get_queryset(self):
        query = self.request.GET.get('search')
        order_by = self.request.GET.get('order_by', self.default_ordering)
        max_set = Driver.objects.values('mobile').prefetch_related('driving_records').annotate(
                      latest_start_date=Max(F('driving_records__start_date')) )

        q_statement = Q()
        for pair in max_set:
            q_statement |= (Q(mobile__exact=pair['mobile'])) & (Q(latest_start_date=pair['latest_start_date']))

        qs = Driver.objects.prefetch_related('driving_records').annotate(
                 latest_start_date= Max(F('driving_records__start_date')),
                 current_car = F('driving_records__car__rego'),
               ).filter(q_statement).order_by(order_by)

        if query is not None:
            search_condition = Q(current_car__icontains=query)|Q(name__icontains=query)|Q(mobile__icontains=query)
            return qs.filter(search_condition)
        else:
            return qs

    def get_context_data(self, **kwargs):
        context = super(ListDriver, self).get_context_data(**kwargs)
        paginator = Paginator(self.get_queryset(), self.paginate_by)
        page = self.request.GET.get('page')
        try:
            drivers_page = paginator.page(page)
        except PageNotAnInteger:
            drivers_page = paginator.page(1)
        except EmptyPage:
            drivers_page = paginator.page(paginator.num_pages)
        context['driver_list'] = drivers_page
        return context

class ListDrivingRecord(generic.ListView):
    paginate_by = 100
    default_ordering = '-start_date'
    template_name = 'cars/drivingrecord_list.html'

    def get_queryset(self):
        query = self.request.GET.get('search')
        order_by = self.request.GET.get('order_by', self.default_ordering)
        qs = DrivingRecord.objects.order_by(order_by)

        if query is not None:
            search_condition = Q(car__rego__icontains=query)|Q(driver__name__icontains=query)|Q(start_date__icontains=query)|Q(end_date__icontains=query)
            return qs.filter(search_condition)
        else:
            return qs

    def get_context_data(self, **kwargs):
        context = super(ListDrivingRecord, self).get_context_data(**kwargs)
        paginator = Paginator(self.get_queryset(), self.paginate_by)
        page = self.request.GET.get('page')
        try:
            drivingrecord_page = paginator.page(page)
        except PageNotAnInteger:
            drivingrecord_page = paginator.page(1)
        except EmptyPage:
            drivingrecord_page = paginator.page(paginator.num_pages)
        context['drivingrecord_list'] = drivingrecord_page
        return context

class SingleCar(generic.DetailView):
    model = Car

class SingleDriver(generic.DetailView):
    model = Driver
