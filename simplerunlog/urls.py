from django.conf.urls.defaults import patterns
from django.views.generic import ListView
from django.views.generic.simple import direct_to_template

from apps.runlog.models import Run

urlpatterns = patterns('apps.runlog.views',
    (r'^$', 'index'),
    (r'^dashboard/$', 'dashboard'),
    (r'^runs/$',
        ListView.as_view(
            queryset = Run.objects.order_by('-date'),
            template_name ='runlog/list.html')),
    (r'^add/$', 'add'),
    (r'^delete/(\d+)$', 'delete'),
)

urlpatterns += patterns('',
    (r'^login/$', 'django.contrib.auth.views.login'),
    (r'^logout/$', 'django.contrib.auth.views.logout'),
)

