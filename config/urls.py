from allauth.account.views import LoginView, LogoutView, ConfirmEmailView
from django.conf import settings
from django.conf.urls import include, url
from django.conf.urls.static import static
from django.contrib import admin
from django.views import defaults as default_views
from django.views.generic import TemplateView, RedirectView

# from apis.github.views import GitHubLoginView, FacebookLogin
from apis.betterself.v1.signout.views import SessionLogoutView
from config.settings.constants import LOCAL

react_home_template = 'react/home.html'
react_signup_template = 'react/signup.html'
react_dashboard_template = 'react/dashboard.html'

favicon_view = RedirectView.as_view(url='/static/images/logos/logojoy/favicon.png', permanent=True)

REACT_SIGNUP_TEMPLATE_VIEW = TemplateView.as_view(template_name=react_signup_template)
REACT_DASHBOARD_TEMPLATE_VIEW = TemplateView.as_view(template_name=react_dashboard_template)

urlpatterns = [
    url(r'^$', TemplateView.as_view(template_name=react_home_template), name='home'),
    url(r'^favicon\.ico$', favicon_view),

    url(r'^admin/', include('admin_honeypot.urls', namespace='admin_honeypot')),
    url(settings.ADMIN_URL, include(admin.site.urls)),

    # User Management
    url(r'^users/', include('betterself.users.urls', namespace='users')),

    # SSO Logins such as when GitHub aka
    # /accounts/github/login/
    url(r'^accounts/', include('allauth.urls')),

    # Where most of the frontend interacts with
    url(r'^api/', include('apis.urls')),

    url(r'^dashboard/authenticate$', REACT_DASHBOARD_TEMPLATE_VIEW, name='react-authenticate'),
    url(r'^dashboard-signup/$', REACT_DASHBOARD_TEMPLATE_VIEW, name='react-signup'),
    url(r'^dashboard.*/$', REACT_DASHBOARD_TEMPLATE_VIEW, name='react-dashboard'),
    url(r'^dashboard-login/$', REACT_DASHBOARD_TEMPLATE_VIEW, name='react-login'),
    url(r'^dashboard-logout/$', REACT_DASHBOARD_TEMPLATE_VIEW, name='react-logout'),

    # Specific api-end point for fitbit to redirect for authorization
    # this allows for pulling in Fitbit data using an API Token without being SessionAuthentication
    url(r'^dashboard/fitbit/oauth2/callback/$', REACT_DASHBOARD_TEMPLATE_VIEW, name='fitbit-complete'),

    url(r'^demo-signup/$', REACT_DASHBOARD_TEMPLATE_VIEW, name='react-demo-signup'),
    url(r'^settings/$', REACT_DASHBOARD_TEMPLATE_VIEW, name='react-settings'),

    # you may want to take out api-auth and have all traffic through rest-auth instead
    # im not sure if you even use rest_framework/api-auth anymore
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),

    url(r'^rest-auth/', include('rest_auth.urls')),
    url(r'^rest-auth/registration/account-confirm-email/(?P<key>[-:\w]+)/$', ConfirmEmailView.as_view(),
        name='account_confirm_email'),
    url(r'^rest-auth/registration/', include('rest_auth.registration.urls')),

    url(r'^login/$', LoginView.as_view()),
    url(r'^logout/$', LogoutView.as_view()),
    url(r'^session-logout/$', SessionLogoutView.as_view()),

    url(r'^token-auth/$', LogoutView.as_view(), name='logged-in-token-authorization'),

    # url(r'^rest-auth/github/$', GitHubLoginView.as_view(), name='github_login'),
    # url(r'^rest-auth/facebook/$', FacebookLogin.as_view(), name='fb_login')
]

# might have to double check this, not sure why MEDIA is so oddly pronounced
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    # This allows the error pages to be debugged during development, just visit
    # these url in browser to see how these error pages look like.
    urlpatterns += [
        url(r'^400/$', default_views.bad_request, kwargs={'exception': Exception('Bad Request!')}),
        url(r'^403/$', default_views.permission_denied, kwargs={'exception': Exception('Permission Denied')}),
        url(r'^404/$', default_views.page_not_found, kwargs={'exception': Exception('Page not Found')}),
        url(r'^500/$', default_views.server_error),
    ]

    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

if settings.DJANGO_ENVIRONMENT == LOCAL:
    import debug_toolbar

    urlpatterns += [
        # https://github.com/bernardopires/django-tenant-schemas/issues/222
        # random issue with django 1.11 breaking debug_toolbar
        url(r'^__debug__/', include(debug_toolbar.urls)),
    ]
