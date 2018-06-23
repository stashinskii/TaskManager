from django.conf.urls import url, include
from django.contrib.auth import views as auth_views
from django.contrib.auth.views import login, logout

from task import views

urlpatterns = [
    url(r'^home/$', views.home, name='home'),

    url(r'^login/$', login, {'template_name': 'registration/login.html'}),
    url(r'^logout/$',logout,{'template_name': 'registration/logout.html'}),
    url(r'^register/$', views.register, name='register'),
    url(r'^delete/(?P<id>\d+)/$', views.delete, name='delete'),
    url(r'^view/(?P<id>\d+)/$', views.view, name='view'),
    url(r'^edit/(?P<id>\d+)/$', views.post_edit, name='post_edit'),
    url(r'^search/(?P<tag>[\w\-]+)/$', views.tag_search, name='tag_search'),
    url(r'^add/$', views.add, name='add'),

    # TODO change smth
    url(r'^status/done/(?P<id>\d+)/$', views.done, name='done'),
    url(r'^status/begin/(?P<id>\d+)/$', views.begin, name='begin')

]
