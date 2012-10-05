from tastypie.authentication import SessionAuthentication
from tastypie.authorization import DjangoAuthorization
from tastypie.resources import ALL, ModelResource

from apps.runlog.models import Run


class RunResource(ModelResource):
    class Meta:
        queryset = Run.objects.all();
        resource_name = 'run'
        authentication = SessionAuthentication()
        authorization = DjangoAuthorization()
        filtering = {
                'date': ALL
                }

        def obj_create(self, bundle, request=None, **kwargs):
            return super(RunResource, self).object_create(bundle, request,
                    user=request.user)

        def apply_authorization_limits(self, request, object_list):
            return object_list.filter(user=request.user)
