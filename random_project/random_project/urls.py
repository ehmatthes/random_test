from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', 'random_app.views.index', name='index'),
    url(r'^other/', 'random_app.views.other', name='other'),

    url(r'^admin/', include(admin.site.urls)),
)
