# maybe change the location of this file, but don't have a better place at the moment
from django.contrib.auth import get_user_model
from django.db import IntegrityError
from django.db import models
from django.conf import settings
from django.db.models import Q


# Most Django models should be derived from this ... impose that many classes have similar
# create / modify attributes
class BaseModel(models.Model):
    created = models.DateField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

    def __str__(self):
        if hasattr(self, 'name'):
            return '{0}'.format(self.name)
        else:
            class_name = self.__class__.__name__
            return '{0}'.format(class_name)

    def __repr__(self):
        return self.__str__()


class UserGeneratedModelManager(models.Manager):
    # If this ever grows any more complexity in scope, don't do it. Just remove this altogether!
    # This complexity is RARELY worth it as a forewarning to yourself ...
    def create(self, **kwargs):
        # override create because any creating of models not from a data-migration
        # should contain a user
        if 'user' not in kwargs:
            raise IntegrityError('User parameter is required in non data-migration transactions')

        return super().create(**kwargs)


class BaseModelWithUserGeneratedContent(BaseModel):
    objects = UserGeneratedModelManager()
    user = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True)

    class Meta:
        abstract = True

    @property
    def is_user_created(self):
        if self.user:
            return True
        else:
            return False

    # restrict access to objects that only belong to a user or belong to no one
    @classmethod
    def get_user_viewable_objects(cls, user):
        # should split this into 2 filters, when is__null pull cached
        # and then filter what the user can see
        default_user = get_user_model().objects.get(username='default')
        queryset = cls.objects.filter(Q(user=user) | Q(user=default_user))
        return queryset


class BaseModelWithRequiredUser(BaseModel):
    user = models.ForeignKey(settings.AUTH_USER_MODEL)

    class Meta:
        abstract = True

    @property
    def is_user_created(self):
        return True
