from django.conf.urls.defaults import patterns, url
from django.views.generic import ListView

from apps.runlog.models import Run

urlpatterns = patterns('apps.runlog.views',
    (r'^$', 'index'),
    (r'^dashboard/$', 'dashboard'),
    url(r'^runs/$',
        ListView.as_view(
            queryset = Run.objects.order_by('-date'),
            template_name ='runlog/list.html'), name='list'),
    (r'^add/$', 'add'),
    (r'^delete/(\d+)$', 'delete'),
    (r'^calendar/$', 'runcal'),
)

urlpatterns += patterns('',
    (r'^login/$', 'django.contrib.auth.views.login'),
    (r'^logout/$', 'django.contrib.auth.views.logout', {'next_page': '/'}),
)

