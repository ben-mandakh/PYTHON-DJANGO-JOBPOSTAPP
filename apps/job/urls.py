from django.conf.urls import url
from . import views	

urlpatterns = [
        url(r'^$', views.index),
        url(r'^process$', views.process),
        url(r'^success$', views.success),
        url(r'^login$', views.login),
        url(r'^logout$', views.logout),
        url(r'^jobs/new$', views.job),
        url(r'^jobs/create$', views.jobNew),
        url(r'^shows/(?P<id>\d+)$', views.showOne),
        url(r'^shows/(?P<id>\d+)/edit$', views.update),
        url(r'^shows/(?P<id>\d+)/update$', views.edit),
        url(r'^shows/(?P<id>\d+)/remove$', views.delete),
]