import pytz
from django.conf import settings
from django.shortcuts import render, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.views.generic import (CreateView, DeleteView, DetailView, FormView,
                                  TemplateView, UpdateView, View)
from bills.models import Bill
from contacts.models import Contact
from common.models import User
from common.access_decorators_mixins import (MarketingAccessRequiredMixin,
                                             SalesAccessRequiredMixin,
                                             marketing_access_required,
                                             sales_access_required)
from bills.forms import BillForm

# Create your views here.
class BillsListView(SalesAccessRequiredMixin, LoginRequiredMixin, TemplateView):
    model = Bill
    context_object_name = "bills_list"
    template_name = "bills.html"

    def get_queryset(self):
        queryset = self.model.objects.all()
        if self.request.user.role != "ADMIN" and not self.request.user.is_superuser:
            queryset = queryset.filter(
                Q(created_by=self.request.user)).distinct()

        request_post = self.request.POST
        if request_post:
            if request_post.get('name'):
                queryset = queryset.filter(
                    name__icontains=request_post.get('name'))
            if request_post.get('contact'):
                queryset = queryset.filter(
                    contacts__name__contains=request_post.get('contact'))
        return queryset.distinct()

    def get_context_data(self, **kwargs):
        context = super(BillsListView, self).get_context_data(**kwargs)
        context["bills_list"] = self.get_queryset()
        context["users"] = User.objects.filter(
            is_active=True)
        #context["industries"] = INDCHOICES
        context["per_page"] = self.request.POST.get('per_page')

        search = False
        #if (
        #    self.request.POST.get('name') or self.request.POST.get('city') or
        #    self.request.POST.get('industry') or self.request.POST.get('tag')
        #):
        if (
            self.request.POST.get('name') or self.request.POST.get('contact')
        ):
            search = True

        context["search"] = search

        TIMEZONE_CHOICES = [(tz, tz) for tz in pytz.common_timezones]
        context["timezones"] = TIMEZONE_CHOICES
        context["settings_timezone"] = settings.TIME_ZONE

        return context

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        return self.render_to_response(context)

    def post(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        return self.render_to_response(context)

class CreateBillView(SalesAccessRequiredMixin, LoginRequiredMixin, CreateView):
    model = Bill
    form_class = BillForm
    template_name = "create_bill.html"

    def dispatch(self, request, *args, **kwargs):
        if self.request.user.role == 'ADMIN' or self.request.user.is_superuser:
            self.users = User.objects.filter(is_active=True).order_by('email')
        elif request.user.google.all():
            self.users = []
        else:
            self.users = User.objects.filter(role='ADMIN').order_by('email')
        return super(
            CreateBillView, self).dispatch(request, *args, **kwargs)

    def get_form_kwargs(self):
        kwargs = super(CreateBillView, self).get_form_kwargs()
        kwargs.update({"bill": True})
        kwargs.update({"request_user": self.request.user})
        # if self.request.user.role != "ADMIN" and not self.request.user.is_superuser:
        #     kwargs.update({"request_user": self.request.user})
        return kwargs

    def post(self, request, *args, **kwargs):
        self.object = None
        form = self.get_form()
        print("get POST request")
        if form.is_valid():
            return self.form_valid(form)

        return self.form_invalid(form)

    def form_valid(self, form):
        # Save Account
        print("[create account]valid form")
        account_object = form.save(commit=False)
        account_object.created_by = self.request.user
        account_object.contact.update({'bill':account_object.amount})
        account_object.save()

        if self.request.POST.get("savenewform"):
            return redirect("bills:new_bill")

        return redirect("bills:list")

    def form_invalid(self, form):
        print("[create account]invalid form")
        print(form.errors)
        if self.request.is_ajax():
            return JsonResponse({'error': True, 'errors': form.errors})
        return self.render_to_response(
            self.get_context_data(form=form)
        )

    def get_context_data(self, **kwargs):
        context = super(CreateBillView, self).get_context_data(**kwargs)
        context["bill_form"] = context["form"]
        context["users"] = self.users

        # context["contact_count"] = Contact.objects.count()
        if self.request.user.role == 'ADMIN' or self.request.user.is_superuser:
            context["contacts"] = Contact.objects.all()
        
        if self.request.user.role != "ADMIN" and not self.request.user.is_superuser:
            context["contacts"] = Contact.objects.filter(Q(created_by=self.request.user))
        context["contact_count"] = context["contacts"].count()
        return context

class BillUpdateView(SalesAccessRequiredMixin, LoginRequiredMixin, UpdateView):
    model = Bill
    form_class = BillForm
    template_name = "create_bill.html"

    def dispatch(self, request, *args, **kwargs):
        self.users = User.objects.filter(is_active=True).order_by('email')
        return super(BillUpdateView, self).dispatch(
            request, *args, **kwargs)

    def get_form_kwargs(self):
        kwargs = super(BillUpdateView, self).get_form_kwargs()
        kwargs.update({"bill": True})
        kwargs.update({"request_user": self.request.user})
        # if self.request.user.role != "ADMIN" and not self.request.user.is_superuser:
        #     kwargs.update({"request_user": self.request.user})
        return kwargs

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)

        return self.form_invalid(form)

    def form_valid(self, form):
        # Save Account
        account_object = form.save(commit=False)
        account_object.save()
        

        if self.request.is_ajax():
            data = {'success_url': reverse_lazy(
                'bills:list'), 'error': False}
            return JsonResponse(data)
        return redirect("bills:list")

    def form_invalid(self, form):
        if self.request.is_ajax():
            return JsonResponse({'error': True, 'errors': form.errors})
        return self.render_to_response(
            self.get_context_data(form=form)
        )

    def get_context_data(self, **kwargs):
        context = super(BillUpdateView, self).get_context_data(**kwargs)
        context["bill_obj"] = self.object
        if self.request.user.role != "ADMIN" and not self.request.user.is_superuser:
            if (self.request.user != context['bill_obj'].created_by ):
                raise PermissionDenied
        context["bill_form"] = context["form"]
        if self.request.user.role != "ADMIN" and not self.request.user.is_superuser:
            self.users = self.users.filter(Q(role='ADMIN') | Q(id__in=[self.request.user.id,]))
        context["users"] = self.users
        context["contact_count"] = Contact.objects.count()
        context['edit_view'] = True
        print(context)
        return context

class BillDeleteView(SalesAccessRequiredMixin, LoginRequiredMixin, DeleteView):
    model = Bill
    template_name = 'view_bill.html'

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        if self.request.user.role != "ADMIN" and not self.request.user.is_superuser:
            if self.request.user != self.object.created_by:
                raise PermissionDenied
        self.object.delete()
        return redirect("bills:list")