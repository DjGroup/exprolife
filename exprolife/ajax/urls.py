from django.conf.urls import patterns, url
from ajax import views

urlpatterns = patterns('',
    #when search box in psychograph is typed autocompleteModel will call
    url(r'^search/$', views.autocompleteModel, name='ajaxSearch'),

    #when email appearance in register form is valid then must check in DB that is unique or not
    url(r'emailCheck/$', views.checkEmailInDB, name='ajaxEmailCheck'),

    url(r'registercheck/$', views.registerCheck, name='ajaxRegisterCheck'),

    )