from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
from social import views
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', include('social.urls', namespace="social")),
    # url(r'^exprolife/', include('exprolife.foo.urls')),

    #logout URL: domain.com/logout
    url(r'^logout/$', 'django.contrib.auth.views.logout',
                          {'next_page': '/'}),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # enable the admin:
    url(r'^admin/', include(admin.site.urls)),

    url(r'^ajax/', include('ajax.urls', namespace="ajax")),

    #see the profile of members in the public (with privileges ):domain.com/firstName.lastName
    url(r'^(?P<first_name>\w+).(?P<last_name>\w+)(.)?(?P<queueNumber>\d+)?/$', views.nameDetailIndex, name="FLSocial"),

    #same but with user_id:domain.com/10052
    url(r'^(?P<user_id>\d+)/$', views.idDetailIndex, name="IDSocial"),

    #dedicated link for each competence: domain.com/Competence/title.id
    url(r'^Competence/(?P<competence_title>[\w \d]+).(?P<competence_id>\d+)', views.competenceLoader, name="comSocial"),

    #dedicated link for each post: domain.com/Post/title.id
    url(r'^Post/(?P<post_title>[\w \d]+).(?P<post_id>\d+)', views.postLoader, name="postSocial"),
)
