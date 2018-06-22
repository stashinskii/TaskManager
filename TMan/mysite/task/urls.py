from django.conf.urls import url, include
from django.contrib.auth import views as auth_views
from django.contrib.auth.views import login, logout

from task import views

urlpatterns = [
    url(r'^home/$', views.home, name='home'),
    url(r'^home/done/$', views.home_done, name='home_done'),
    url(r'^home/undone/$', views.home_undone, name='home_undone'),
    url(r'^home/process/$', views.home_process, name='home_process'),
    url(r'^login/$', login, {'template_name': 'registration/login.html'}),
    url(r'^logout/$',logout,{'template_name': 'registration/logout.html'}),
    url(r'^register/$', views.register, name='register'),
    url(r'^delete/(?P<id>\d+)/$', views.delete),
    url(r'^status/done/(?P<id>\d+)/$', views.done),
    url(r'^status/undone/(?P<id>\d+)/$', views.undone),
    url(r'^status/begin/(?P<id>\d+)/$', views.begin)

]
