from django.conf.urls import patterns, url
from ajax import views

urlpatterns = patterns('',
	url(r'^search/$', views.autocompleteModel, name='index'),

	)