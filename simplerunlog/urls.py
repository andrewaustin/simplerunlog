from django.conf.urls.defaults import patterns
from apps.runlog.models import Run
from django.views.generic import ListView

urlpatterns = patterns('apps.runlog.views',
    ('^$', 'index'),
    ('^runs/$',
        ListView.as_view(
            queryset = Run.objects.order_by('-date'),
            template_name ='runlog/list.html')),
    (r'^add/$', 'add'),
    (r'^delete/(\d+)$', 'delete'),
)

