from django.contrib.auth.models import User

from tastypie import fields
from tastypie.resources import ModelResource, ALL, ALL_WITH_RELATIONS
from tastypie.authorization import Authorization
from apps.survey_browser.models import ParticipantFilter, ParticipantMetaFilter, ParticipantFilterGroup

class UserResource(ModelResource):
    class Meta:
        queryset = User.objects.all()
        resource_name = 'user'
        fields = ['username', 'email', 'first_name', 'last_name', 'last_login']
        allowed_methods = ['get']

class ParticipantFilterGroupResource(ModelResource):
    user = fields.ForeignKey(UserResource, 'user')
    
    class Meta:
        queryset = ParticipantFilterGroup.objects.all()
        resource_name = 'participantfiltergroup'
        authorization= Authorization()
        filtering = {
            'id': ALL,
        }

    def dehydrate(self, bundle):
        bundle.data['nfilters'] = ParticipantFilter.objects.filter(groups = bundle.obj).count() + ParticipantMetaFilter.objects.filter(groups = bundle.obj).count()
        return bundle

    def obj_create(self, bundle, request=None, **kwargs):
        return super(ParticipantFilterGroupResource, self).obj_create(bundle, request, user=request.user)

    def apply_authorization_limits(self, request, object_list):
        return object_list.filter(user=request.user)

class ParticipantFilterResource(ModelResource):
    groups = fields.ToManyField(ParticipantFilterGroupResource, 'groups')
    
    class Meta:
        queryset = ParticipantFilter.objects.filter(groups__name = "DEFAULT")
        resource_name = 'participantfilter'
        authorization= Authorization()
        filtering = {
            'id': ALL,
            'filter_field': ALL,
            'groups': ALL_WITH_RELATIONS,
        }

    def apply_authorization_limits(self, request, object_list):
        return object_list.filter(groups__user=request.user).distinct()

    def obj_create(self, bundle, request=None, **kwargs):
        bundle = super(ParticipantFilterResource, self).obj_create(bundle, request, user=request.user)
        # assure this is assigned to DEFAULT before returning
        if not bundle.obj.groups.filter(name = "DEFAULT").exists():
            default_group = ParticipantFilterGroup.objects.get_or_create(user=request.user, name = "DEFAULT")[0]
            bundle.obj.groups.add(default_group)
            bundle.obj.save()
        return bundle

class ParticipantMetaFilterResource(ModelResource):
    groups = fields.ToManyField(ParticipantFilterGroupResource, 'groups')
    filters = fields.ToManyField(ParticipantFilterResource, 'filters')
    metafilters = fields.ToManyField('survey_browser.api.ParticipantMetaFilterResource', 'metafilters')
    
    class Meta:
        queryset = ParticipantMetaFilter.objects.filter(groups__name = "DEFAULT")
        resource_name = 'participantmetafilter'
        authorization= Authorization()
        filtering = {
            'id': ALL,
            'filters': ALL_WITH_RELATIONS,
            'metafilters': ALL_WITH_RELATIONS,
            'groups': ALL_WITH_RELATIONS,
        }

    def apply_authorization_limits(self, request, object_list):
        return object_list.filter(groups__user=request.user).distinct()
    