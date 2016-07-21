from django.contrib.auth import get_user_model

User = get_user_model()


class UsersTestsMixin(object):
    @classmethod
    def create_user(cls, username, email, password):
        user = User.objects.create_user(username=username, email=email, password=password)
        return user
