from django.conf.urls import patterns, url
from ajax import views

urlpatterns = patterns('',
    #when search box in psychograph is typed autocompleteModel will call
    url(r'^search/$', views.autocompleteModel, name='ajaxSearch'),

    #when email appearance in register form is valid then must check in DB that is unique or not
    url(r'emailCheck/$', views.checkEmailInDB, name='ajaxEmailCheck'),

    #check that is fileds that in refister form is valid or not
    url(r'registercheck/$', views.registerCheck, name='ajaxRegisterCheck'),

    #check that is valid fileds in board from fields and then send isOK signal to DOM with js
    url(r'postboardcheck/$', views.postBoardCheck, name='ajaxPostBoardCheck'),

    #get posts that related to the current user and send them to DOM
    url(r'getposts/$', views.getPosts, name='ajaxBoardPostsCheck')
    )