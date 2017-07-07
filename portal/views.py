from django.core.mail import EmailMultiAlternatives
from django.template.loader import get_template
from django.template import Context
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login as auth_login, authenticate
from django.contrib.auth.views import login, logout
from django.contrib.sites.shortcuts import get_current_site
from django.core.urlresolvers import reverse_lazy

from django.utils.decorators import method_decorator
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_decode
from django.views.generic import ListView, CreateView, RedirectView, FormView, DetailView, TemplateView

from niit_project.tokens import account_activation_token
from .forms import RecipientForm, DonorForm, RegistrationForm, LoginForm
from .models import Recipient, Donor, Ngo, User, UserProfile


class RegistrationView(CreateView):
    form_class = RegistrationForm
    success_url = reverse_lazy('portal:home')
    template_name = 'portal/signup_login.html'

    def form_valid(self, form):
        response = super(RegistrationView, self).form_valid(form)

        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password')

        user = User.objects.get(username=username)
        user.set_password(password)
        user.save()
        user = authenticate(username=username, password=password)

        user.is_active = False
        current_site = get_current_site(self.request)

        subject = 'Activate Your Account'
        context_variables = Context({
            'user': user,
            'domain': current_site.domain,
            'uid': urlsafe_base64_encode(force_bytes(user.pk)),
            'token': account_activation_token.make_token(user),
        })
        plain_text = get_template('portal/account_activation_email.txt')
        html_text = get_template('portal/account_activation_email.html')

        text_content = plain_text.render(context_variables)
        html_content = html_text.render(context_variables)

        email = EmailMultiAlternatives(subject=subject, body=text_content, to=[user.email])
        email.attach_alternative(html_content, "text/html")
        email.send()
        return response


class AccountActivationView(TemplateView):
    template_name = 'portal/account_activation_sent.html'


class AccountActivationFailed(TemplateView):
    template_name = 'portal/account_activation_invalid.html'


class ActivateView(RedirectView):
    def get(self, request, *args, **kwargs):

        try:
            uid = force_text(urlsafe_base64_decode(kwargs.get('uidb64')))
            user = request.POST.get('pass')
            print user
            # user = User.objects.get(pk=uid)

        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None

        if user is not None:

            if account_activation_token.check_token(user, kwargs.get('token')):
                user.is_active = True

                UserProfile.objects.get(username=user.username).email_confirmed = True
                print request.user
                # request.user = user

                # user = authenticate(username=user.username,password='qwas1234')
                # print "check user is", check_user

                auth_login(request, user)
                return redirect(reverse_lazy('portal:home'))
        else:

            redirect(reverse_lazy('portal:activation_failed'))

        return super(ActivateView, self).get(request, *args, **kwargs)


class FundDetailsView(ListView):
    template_name = 'portal/fund_details.html'
    model = Donor

    def get_context_data(self, **kwargs):
        context = super(FundDetailsView, self).get_context_data(**kwargs)
        donors = Donor.objects.all()
        context['donors'] = donors
        return context


class LoginView(FormView):
    template_name = 'portal/signup_login.html'
    success_url = reverse_lazy('portal:home')
    form_class = LoginForm

    def post(self, request, *args, **kwargs):
        username = request.POST.get('username')
        user = User.objects.get(username=username)

        login(request, redirect_field_name=reverse_lazy('portal:home'), template_name='portal/signup_login.html')

        if user.is_authenticated():

            if request.POST.get('remember_me') == True:
                request.session.set_expiry(0)

        return super(LoginView, self).post(request, *args, **kwargs)


class LogoutView(RedirectView):
    """
    Provides users the ability to logout
    """
    url = reverse_lazy('portal:home')

    def get(self, request, *args, **kwargs):
        logout(request)
        return super(LogoutView, self).get(request, *args, **kwargs)


class HomePageView(ListView):
    template_name = 'portal/home_page.html'
    model = Donor

    def get_context_data(self, **kwargs):
        context = super(HomePageView, self).get_context_data(**kwargs)
        # context['top_donors'] = Donor.get_top_donors(self)
        # context['recent_recipients'] = Recipient.get_recipients(self)
        context['top_donors'] = Donor.objects.order_by('-donation_date')[:5]
        context['recent_recipients'] = Recipient.objects.order_by('-date_of_reception')[:5]
        context['total_funds'] = Ngo.objects.all()
        return context


@method_decorator(login_required(redirect_field_name=reverse_lazy('portal:home')), name='dispatch')
class DonorFormView(CreateView):
    form_class = DonorForm
    template_name = "portal/donate.html"

    def get_context_data(self, **kwargs):
        old_context = super(DonorFormView, self).get_context_data(**kwargs)
        context = dict()
        context['donor_form'] = old_context['form']
        return context


@method_decorator(login_required(redirect_field_name=reverse_lazy('portal:home')), name='dispatch')
class RecipientFormView(CreateView):
    form_class = RecipientForm
    template_name = 'portal/ask_for_funds.html'
    success_url = '/portal'

    def get_context_data(self, **kwargs):
        old_context = super(RecipientFormView, self).get_context_data(**kwargs)
        context = dict()
        context['recipient_form'] = old_context['form']
        return context
