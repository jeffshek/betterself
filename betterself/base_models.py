# maybe change the location of this file, but don't have a better place at the moment
from django.db import models
from django.conf import settings


# Most Django models should be derived from this ... impose that many classes have similar
# create / modify attributes
class BaseModel(models.Model):
    created = models.DateField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class BaseModelWithUserGeneratedContent(BaseModel):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True)

    class Meta:
        abstract = True

    @property
    def is_user_created(self):
        if self.user:
            return True
        else:
            return False


class BaseModelWithRequiredUser(BaseModel):
    user = models.ForeignKey(settings.AUTH_USER_MODEL)

    class Meta:
        abstract = True

    @property
    def is_user_created(self):
        return True
