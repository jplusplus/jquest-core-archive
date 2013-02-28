from tastypie import fields
from tastypie.resources import ModelResource, ALL, ALL_WITH_RELATIONS
from tastypie.authentication import BasicAuthentication
from tastypie.authorization import DjangoAuthorization
# Models available from the API
from django.contrib.auth.models import User
from django.utils import translation
from jquest.models import *
# Authentication tools
from django.contrib.auth.hashers import check_password, make_password
from django.conf.urls.defaults import url


def is_digit_id(field, dic):
    """
    Determines if the given field exists in dic and is a digit id 
    """
    return field in dic and ( type(dic[field]) == int or dic[field].isdigit() )

class AdditionalModelResource(ModelResource):
    """ 
    Overrides the default ModelResource class to 
        - add an additional_detail_fields option that adds fields in detail mode
        - overrides the get_fields method to support the 'blank' attribute on model fields
    """

    class Meta:
        additional_detail_fields = {}

    # detail_dehydrate is basically full_dehydrate
    # except we'll loop over the additional_detail_fields
    # and we won't want to do the dehydrate(bundle) at the end
    def detail_dehydrate(self, bundle):
        """
        Given a bundle with an object instance, extract the information from it
        to populate the resource.
        """
        # Dehydrate each field.
        # loop over additional_detail_fields instead
        #for field_name, field_object in self.fields.items():
        for field_name, field_object in self._meta.additional_detail_fields.items():
            # A touch leaky but it makes URI resolution work.
            if getattr(field_object, 'dehydrated_type', None) == 'related':
                field_object.api_name = self._meta.api_name
                field_object.resource_name = self._meta.resource_name

            bundle.data[field_name] = field_object.dehydrate(bundle)

            # Check for an optional method to do further dehydration.
            method = getattr(self, "dehydrate_%s" % field_name, None)

            if method:
                bundle.data[field_name] = method(bundle)

        return bundle

    def dehydrate(self, bundle):
        # detect if detail
        if self.get_resource_uri(bundle) == bundle.request.path:
            # detail detected, include additional fields
            bundle = self.detail_dehydrate(bundle)
        return bundle

    @classmethod
    def get_fields(cls, fields=None, excludes=None):
        """
        Unfortunately we must override this method because tastypie ignores 'blank' attribute
        on model fields.

        Here we invoke an insane workaround hack due to metaclass inheritance issues:
            http://stackoverflow.com/questions/12757468/invoking-super-in-classmethod-called-from-metaclass-new
        """
        this_class = next(c for c in cls.__mro__ if c.__module__ == __name__ and c.__name__ == 'AdditionalModelResource')
        fields = super(this_class, cls).get_fields(fields=fields, excludes=excludes)
        if not cls._meta.object_class:
            return fields
        for django_field in cls._meta.object_class._meta.fields:
            if django_field.blank == True:
                res_field = fields.get(django_field.name, None)
                if res_field:
                    res_field.blank = True
        return fields

class UserResource(AdditionalModelResource):
    
    class Meta:
        excludes = ("last_login")
        queryset = User.objects.all()
        resource_name = 'user'
        always_return_data = True
        filtering = {
            "date_joined": ALL,
            "first_name": ALL,
            "id": ALL,
            "is_active": ALL,
            "is_staff": ALL,
            "is_superuser": ALL,
            "last_name": ALL,            
            "resource_uri": ALL,
            "username": ALL,
            "email": ALL
        }

        ordering = filtering

        additional_detail_fields = {
            'progressions': fields.ToManyField(
                'jquest.api.UserProgressionResource', 
                attribute=lambda bundle: UserProgression.objects.filter(user=bundle.obj),
                full=True, 
                null=True
            )
        }
        
        authentication = BasicAuthentication()
        authorization = DjangoAuthorization()



    def obj_create(self, bundle, request=None, **kwargs):   
        """
            Overide the default obj_create method to save nested resources.
        """          
        bundle = super(UserResource, self).obj_create(bundle, request, **kwargs)      

        # Oauths insertion
        if 'oauths' in bundle.data:
            # The insertion mode is differents accoding the type of the oauths attribut
            oauth_type = type(bundle.data["oauths"])
            # Post request is asking for create several UserOauths at the same time
            if oauth_type == list:
                # For each given UserOauth object
                for o in bundle.data["oauths"]:
                    oauth = UserOauth(**o)
                    oauth.user = bundle.obj
                    oauth.save()        
            # Post request is asking for create an UserOauth at the same time
            elif oauth_type == dict:
                oauth = UserOauth(**bundle.data["oauths"])
                oauth.user = bundle.obj
                oauth.save()

        bundle.obj.set_password(bundle.data.get('password'))         
        bundle.obj.save()         
        return bundle


    def override_urls(self):
        return [
            url(r"^(?P<resource_name>%s)/(?P<pk>\d+?)/check_password/$" % self._meta.resource_name, self.wrap_view('check_password'), name="api_check_password"),            
        ]

    def check_password(self, request, **kwargs):
        """
            Method to verify a raw password against the saved encrypted one (only use through SSL!)
        """
        #TODO: Check the function for a password change with put
        self.method_check(request, allowed=['get'])
        self.is_authenticated(request)
        self.throttle_check(request)

        try:
            obj = self.cached_obj_get(request=request, **self.remove_api_resource_names(kwargs))
        except ObjectDoesNotExist:
            return HttpGone()
        except MultipleObjectsReturned:
            return HttpMultipleChoices("More than one resource is found at this URI.")

        # Validate with password or hash
        # pbkdf2_sha256%2410000%24xQKw5vSgmCRt%24oDa0ljLoPx0aISmQoQeKWDVJ9n7ckZOjc18H8VxRQFA%3D
        if request.GET.get('password'):
            valid = check_password(request.GET.get('password'), obj.password)
        else:
            valid = request.GET.get('hash') == obj.password

        self.log_throttled_access(request)

        bundle = self.build_bundle(obj=obj, request=request)
        bundle = self.full_dehydrate(bundle)
        bundle = self.alter_detail_data_to_serialize(request, bundle)

        #add out result
        bundle.data['password_valid'] = valid
        return self.create_response(request, bundle)



class UserProgressionResource(ModelResource):            
    mission = fields.ToOneField(
        "jquest.api.MissionResource",
        'mission',
        full=False
    )  
    user = fields.ToOneField(
        "jquest.api.UserResource",
        'user',
        full=True
    )  
    class Meta:
        queryset = UserProgression.objects.all()
        resource_name = 'user_progression'
        always_return_data = True

        filtering = {
            "mission": ALL_WITH_RELATIONS,
            "user": ALL_WITH_RELATIONS,
            "state": ALL,
            "points": ALL
        }        

        ordering = filtering
        
        authentication = BasicAuthentication()
        authorization = DjangoAuthorization()

    def getState(self, string):
        states = UserProgression.PROGRESSION_STATES        
        state  = [st for st in states if string == st[0] or string == st[1] ]
        return state[0] if len(state) > 0 else False
        
    def dehydrate_state(self, bundle):                
        # Looks for the state display
        return self.getState(bundle.data["state"])[1]

    def hydrate_state(self, bundle):                
        # Looks for the state code
        bundle.data["state"] = self.getState(bundle.data["state"])[0]
        return bundle

    
    def hydrate_user(self, bundle):
        """ set id instead of uri """   
        if 'user' in bundle.data and bundle.data['user'].isdigit():
            bundle.data['user'] = User.objects.get(id=bundle.data['user'])
        return bundle

    def hydrate_mission(self, bundle):
        """ set id instead of uri """
        if 'mission' in bundle.data and bundle.data['mission'].isdigit():
            bundle.data['mission'] = Mission.objects.get(id=bundle.data['mission'])        
        return bundle  
             


class UserOauthResource(ModelResource):
    user = fields.ToOneField(
        UserResource,
        "user",
        full=True
    )   
    class Meta:
        queryset = UserOauth.objects.all()
        resource_name = 'user_oauth'
        always_return_data = True
        filtering = {
            'consumer_user_id': ALL,
            'consumer': ALL,
            'user': ALL_WITH_RELATIONS
        }

        ordering = filtering
        
        authentication = BasicAuthentication()
        authorization = DjangoAuthorization()

class UserTokenResource(ModelResource):
    user = fields.ToOneField(
        UserResource,
        "user",
        full=True
    )   
    class Meta:
        queryset = UserToken.objects.all()
        resource_name = 'user_token'
        always_return_data = True
        filtering = {
            'user': ALL_WITH_RELATIONS,
            'token': ALL,
            'created_at': ALL
        }

        ordering = filtering
        
        authentication = BasicAuthentication()
        authorization = DjangoAuthorization()


class InstanceResource(AdditionalModelResource):  

    class Meta:    
        queryset = Instance.objects.all()
        additional_detail_fields = {
            'missions': fields.ToManyField(
                'jquest.api.MissionResource', 
                attribute=lambda bundle: Mission.objects.filter(instance=bundle.obj),
                full=True, 
                null=True
            )
        }
        resource_name = 'instance'
        always_return_data = True
        filtering = {
            'slug': ALL,
            'name': ALL,
            'host': ALL,
            'missions__id': ALL
        }

        ordering = filtering
        
        authentication = BasicAuthentication()
        authorization = DjangoAuthorization()


class MissionResource(ModelResource):
    # Instance related to that mission
    instance = fields.ToOneField(
        InstanceResource,
        'instance',
        full=False
    )    

    # parent
    relationships = fields.ToManyField(
        "jquest.api.MissionRelationshipResource",
        attribute=lambda bundle: MissionRelationship.objects.filter(mission=bundle.obj),        
        full=True, 
        null=True
    )

    """
        # All users progressions related to that mission
        progressions = fields.ToManyField(
            to="jquest.api.UserProgressionResource",
            attribute=lambda bundle: UserProgression.objects.filter(mission=bundle.obj), 
            full=True,
            null=True        
        ) 
    """

    class Meta:
        queryset = Mission.objects.all()
        resource_name = 'mission'
        always_return_data = True
        excludes = ("progressions",)
        filtering = {
            'name': ALL,
            'instance': ALL
        }       

        ordering = filtering

        authentication = BasicAuthentication()
        authorization = DjangoAuthorization()

    # Convert image path to an URL
    def dehydrate_image(self, bundle):
        return bundle.request.build_absolute_uri(bundle.data["image"]) if bundle.data["image"] else None 


class MissionRelationshipResource(ModelResource):
    parent  = fields.ToOneField(MissionResource, "parent", full=False)
    mission = fields.ToOneField(MissionResource, "mission", full=False)

    class Meta:
        queryset = MissionRelationship.objects.all()
        resource_name = 'mission_relationship'
        
        authentication = BasicAuthentication()
        authorization = DjangoAuthorization()

class PostResource(ModelResource):
    class Meta:
        queryset = Post.objects.all()
        resource_name = 'post'
        always_return_data = True
        # Exludes located fields
        excludes = ("title_en", "title_fr", "content_en", "content_fr", "excerpt_en", "excerpt_fr")

        filtering = {
            'slug': ALL,
            'id': ALL,
            'created_at': ALL,
            'updated_at': ALL,            
        }
        
        ordering = filtering

        authentication = BasicAuthentication()
        authorization = DjangoAuthorization()



class EntityFamilyResource(ModelResource):
    class Meta:
        queryset = EntityFamily.objects.all()
        resource_name = 'entity_family'
        always_return_data = True   
        
        authentication = BasicAuthentication()
        authorization = DjangoAuthorization()

class EntityResource(ModelResource):
    # Instance related to that mission
    family = fields.ToOneField(
        EntityFamilyResource,
        'family',
        full=True
    )    

    entityeval = fields.ToManyField(
        "jquest.api.EntityEvalResource",
        attribute=lambda bundle: EntityEval.objects.filter(entity=bundle.obj), 
        null=True,
        full=True
    )

    class Meta:
        queryset = Entity.objects.all()
        resource_name = 'entity'
        always_return_data = True
        filtering = {
            'family': ALL_WITH_RELATIONS
        }     
        
        ordering = filtering

        authentication = BasicAuthentication()
        authorization = DjangoAuthorization()

    def apply_filters(self, request, applicable_filters):
        """
        Filter entity by not evaluate by the given user
        """
        base_object_list = super(EntityResource, self).apply_filters(request, applicable_filters)
        not_evaluated_by = request.GET.get('not_evaluated_by', None)
        filters = {}
        if not_evaluated_by:                       
            base_object_list = base_object_list.exclude(entityeval__user__id=not_evaluated_by)

        evaluated_by = request.GET.get('evaluated_by', None)
        if evaluated_by:           
            base_object_list = base_object_list.filter(entityeval__user__id=evaluated_by)

        return base_object_list.filter(**filters).distinct()

    def hydrate_family(self, bundle):
        """ 
        Set id instead of uri 
        """   
        if is_digit_id('family', bundle.data):
            bundle.data['family'] = EntityFamily.objects.get(id=bundle.data['family'])        
        return bundle

    def dehydrate_body(self, bundle):
        """
        Evaluates the body field to show it as a dictionary
        """        
        return eval(bundle.data["body"])


class EntityEvalResource(ModelResource):
    # Instance related to that mission
    entity = fields.ToOneField(
        EntityResource,
        'entity',
        full=False
    )    

    # Instance related to that mission
    user = fields.ToOneField(
        UserResource,
        'user',
        full=True
    )    

    class Meta:
        queryset = EntityEval.objects.all()
        resource_name = 'entity_eval'
        always_return_data = True
        
        authentication = BasicAuthentication()
        authorization = DjangoAuthorization()

    def hydrate(self, bundle):              
        # Is the given entity a digit id ?  
        if is_digit_id('entity', bundle.data):     
            # If yes, got it        
            bundle.data['entity'] = Entity.objects.get(id=bundle.data['entity'])
        # Are we trying to use the fid/family couple to evaluate the entity ?
        elif 'fid' in bundle.data and 'family' in bundle.data:
            # If yes, got the entity
            fid = bundle.data['fid'];
            family = bundle.data['family'];
            bundle.data['entity'] = Entity.objects.get(fid=fid, family=family)
        # Is the given user a digit id ?  
        if is_digit_id('user', bundle.data):
            # If yes, got it        
            bundle.data['user'] = User.objects.get(id=bundle.data['user'])            
        return bundle