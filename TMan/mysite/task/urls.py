from django.conf.urls import url, include
from django.contrib.auth import views as auth_views
from django.contrib.auth.views import login, logout

from task import views

urlpatterns = [
    url(r'^home/$', views.home, name='home'),
    url(r'^login/$', login, {'template_name': 'registration/login.html'}),
    url(r'^logout/$',logout,{'template_name': 'registration/logout.html'}),
    url(r'^register/$', views.register, name='register'),

]
