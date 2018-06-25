from django.conf.urls import url, include
from django.contrib.auth import views as auth_views
from django.contrib.auth.views import login, logout

from task import views

urlpatterns = [
    url(r'^$', views.home, name='homepage'),
    url(r'^home/$', views.home, name='home'),
    url(r'^home/(?P<status>\d+)/$', views.home, name='archieve'),
    url(r'^login/$', login, {'template_name': 'registration/login.html'}),
    url(r'^logout/$',logout,{'template_name': 'registration/logout.html'}),
    url(r'^register/$', views.register, name='register'),
    url(r'^delete/(?P<id>\d+)/$', views.delete, name='delete'),
    url(r'^view/(?P<id>\d+)/$', views.view, name='view'),
    url(r'^edit/(?P<id>\d+)/$', views.post_edit, name='post_edit'),
    url(r'^share/(?P<id>\d+)/$', views.share_task, name='share_task'),
    url(r'^search/(?P<tag>[\w\-]+)/$', views.tag_search, name='tag_search'),
    url(r'^add/$', views.add, name='add'),
    url(r'^global_search/(?P<string>[\w\-]+)/$', views.global_search, name='global_search'),
    url(r'^add_subtask/(?P<id>\d+)/$', views.add_subtask, name='add_subtask'),
    url(r'^schedulers/$', views.get_scheduler_list, name='schedulers'),
    url(r'^add_scheduler/$', views.add_scheduler, name='add_scheduler'),
    url(r'^status/done/(?P<id>\d+)/$', views.done, name='done'),
    url(r'^status/begin/(?P<id>\d+)/$', views.begin, name='begin')

]
