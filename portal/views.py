from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.views.generic import ListView, DetailView, FormView
from .forms import RecipientForm, DonorForm
from .models import Recipient, Donor, Ngos


class HomePageView(ListView):
    template_name = 'portal/home_page.html'

    def get_context_data(self, **kwargs):
        context = super(HomePageView, self).get_context_data(**kwargs)
        context['top_donors'] = Donor.get_top_donors()
        context['recent_recipients'] = Recipient.get_recipients()
        return context


class TotalFundView(ListView):
    template_name = 'portal/total_funds.html'

    def get_context_data(self, **kwargs):
        context = super(TotalFundView, self).get_context_data(**kwargs)
        context['total_funds'] = Ngos.objects.all()


class DonorFormView(FormView):
    form_class = DonorForm
    template_name = "portal/donate.html"


class RecipientFormView(FormView):
    form_class = RecipientForm
    template_name = 'portal/ask_for_funds.html'
