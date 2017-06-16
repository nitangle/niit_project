from django import forms
from django.utils.timezone import datetime

from .models import Recipient, Donor

# from crispy_forms.helper import FormHelper
# from crispy_forms.layout import Submit


class RecipientForm(forms.ModelForm):
    class Meta:
        model = Recipient
        exclude = ['transaction_date']

class DonorForm(forms.ModelForm):
    class Meta:
        model = Donor


