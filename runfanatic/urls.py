from django.conf.urls.defaults import patterns, url

from apps.runlog.views import RunListView, UserProfileUpdateView

urlpatterns = patterns('apps.runlog.views',
    (r'^$', 'index'),
    (r'^dashboard/$', 'dashboard'),
    url(r'^runs/$',
        RunListView.as_view(
            template_name='runlog/list.html'
        ), name='list'),
    (r'^add/$', 'add'),
    (r'^delete/(\d+)$', 'delete'),
    (r'^calendar/$', 'runcal'),
    url(r'^settings/$', UserProfileUpdateView.as_view(), name='settings'),
)

urlpatterns += patterns('',
    (r'^login/$', 'django.contrib.auth.views.login'),
    (r'^logout/$', 'django.contrib.auth.views.logout', {'next_page': '/'}),
)
