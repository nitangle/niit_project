from django.conf.urls import url

from . import views

app_name = 'portal'

urlpatterns = [
    url(r'^$',views.HomePageView.as_view(), name="home"),
    url(r'^')
]
