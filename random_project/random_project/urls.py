from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', 'random_app.views.index', name='index'),
    url(r'^refreshing_page/', 'random_app.views.refreshing_page', name='refreshing_page'),
    url(r'^non_refreshing_page/', 'random_app.views.non_refreshing_page', name='non_refreshing_page'),

    url(r'^admin/', include(admin.site.urls)),
)
