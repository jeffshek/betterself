import factory


class UserFactory(factory.django.DjangoModelFactory):
    username = 'default'
    password = factory.PostGenerationMethodCall('set_password', 'password')

    class Meta:
        model = 'users.User'
        django_get_or_create = ('username', )
