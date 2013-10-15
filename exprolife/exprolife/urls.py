from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
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

    url(r'^ajax/', include('ajax.urls', namespace="ajax"))
)
