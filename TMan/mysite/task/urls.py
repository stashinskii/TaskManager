from django.conf.urls import url, include
from django.contrib.auth import views as auth_views

from task import views

urlpatterns = [
    url(r'^home/$', views.home, name='home')
]
