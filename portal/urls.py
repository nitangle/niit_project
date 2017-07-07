from django.conf.urls import url

from . import views

app_name = 'portal'

urlpatterns = [
    url(r'^$', views.HomePageView.as_view(), name="home"),
    url(r'^donate$', views.DonorFormView.as_view(), name="donate"),
    url(r'^ask_for_funds$', views.RecipientFormView.as_view(), name="ask_for_funds"),
    url(r'^signup', views.RegistrationView.as_view(), name="signup"),
    url(r'^fund_details', views.FundDetailsView.as_view(), name="fund_details"),
    url(r'^account_activation_sent/$', views.AccountActivationView.as_view(), name='account_activation_sent'),
    url(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        views.ActivateView.as_view(), name='activate'),
    url(r'^activation_failed', views.AccountActivationFailed.as_view(), name='activation_failed'),
    url(r'^login', views.LoginView.as_view(), name="login"),
    url(r'^logout', views.LogoutView.as_view(), name="logout")

]
