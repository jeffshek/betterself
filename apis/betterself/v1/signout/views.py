from django.contrib.auth import logout
from django.views.generic import RedirectView


class SessionLogoutView(RedirectView):
    """
    A view that will logout a user out and redirect to homepage.
    """
    permanent = False
    query_string = True
    pattern_name = 'home'

    def get_redirect_url(self, *args, **kwargs):
        """
        Logout user and redirect to target url.
        """
        if self.request.user.is_authenticated():
            logout(self.request)
        return super(SessionLogoutView, self).get_redirect_url(*args, **kwargs)
