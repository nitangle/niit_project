from django import forms

from django.contrib.auth.forms import AuthenticationForm
from .models import Recipient, Donor, UserProfile

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit


class RegistrationForm(forms.ModelForm):
    confirm_password = forms.CharField(widget=forms.PasswordInput)
    class Meta:
        model = UserProfile
        fields = ['first_name', 'last_name', 'username', 'email',
                  'password', 'confirm_password','institute_name', 'company_name',
                  'occupation', 'aadhar_card_no', 'aadhar_card_pic',
                  'pan_card_no','pan_card_pic'
                  ]
        widgets = {'password': forms.PasswordInput}

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if username and not UserProfile.objects.filter(username=username):
            return username
        else:
            raise forms.ValidationError("username already taken", code='invalid')

    # def clean_email(self):
    #     email = self.cleaned_data.get('email')
    #     if email and not UserProfile.objects.filter(email=email):
    #         return email
    #     else:
    #         raise forms.ValidationError("Email address has to be unique", code='invalid')

    def clean(self):
        cleaned_data = super(RegistrationForm, self).clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')

        if password != confirm_password:
            self.add_error('confirm_password', "password does not match")


class LoginForm(AuthenticationForm):
    remember_me = forms.BooleanField(widget=forms.CheckboxInput,required=False)

    class Meta:
        model = UserProfile
        fields = '__all__'
        labels = {
            'username': 'username/email'
        }
    def clean(self):
        cleaned_data = super(LoginForm, self).clean()

        username = cleaned_data.get('username')
        user = UserProfile.objects.get(username=username)
        if not user.email_confirmed:
            raise forms.ValidationError("You are not authorised to login yet!!", code='invalid')


class RecipientForm(forms.ModelForm):
    class Meta:
        model = Recipient
        exclude = ['transaction_date', 'amount_received']

    def __init__(self, *args, **kwargs):
        super(RecipientForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_id = 'recipient-form'
        self.helper.form_class = 'blueForms'
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Submit'))


class DonorForm(forms.ModelForm):
    class Meta:
        model = Donor
        exclude = ['user', 'donation_date']
        labels = {
            'amount_donated': "Amount you wish to donate",
        }

    def __init__(self, *args, **kwargs):
        super(DonorForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_id = 'donor-form'
        self.helper.form_class = 'blueForms'
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Submit'))
