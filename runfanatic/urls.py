from django.conf.urls.defaults import patterns, url

from apps.runlog.views import RunListView, UserProfileUpdateView

urlpatterns = patterns('apps.runlog.views',
    url(r'^$', 'index', name='index'),
    url(r'^dashboard/$', 'dashboard', name='dashboard'),
    url(r'^runs/$',
        RunListView.as_view(
            template_name='runlog/list.html'
        ), name='list'),
    url(r'^add/$', 'add', name='add'),
    url(r'^delete/(\d+)$', 'delete', name='delete'),
    url(r'^calendar/$', 'runcal', name='calendar'),
    url(r'^settings/$', UserProfileUpdateView.as_view(), name='settings'),
    url(r'^user/(?P<username>[\w.@+-]+)', 'public_profile',
        name='public_profile'),
)

urlpatterns += patterns('',
    url(r'^login/$', 'django.contrib.auth.views.login', name='login'),
    url(r'^logout/$', 'django.contrib.auth.views.logout', {'next_page': '/'},
        name='logout'),
)
