from django.conf import settings
from django.conf.urls import include, url
from django.conf.urls.static import static
from django.views import defaults as default_views
from django.contrib import admin

from rest_framework import routers
from rest_framework.authtoken import views as auth
import regex
from rest_framework_jwt.views import obtain_jwt_token
from allauth.account.views import confirm_email as allauthemailconfirmation

from rest_auth.blog import api

router = routers.DefaultRouter()
router.register(r'blogs', api.BlogListViewSet)
router.register(r'rest_auth', api.BlogViewSet)

urlpatterns = [

    url(r'^api/v1/', include(router.urls)),
    url(settings.ADMIN_URL, admin.site.urls),
    # url(r'^api-token-auth/', auth.obtain_auth_token),
    url(r'^o/', include('oauth2_provider.urls', namespace='oauth2_provider')),
    url(r'^api-token-auth/', obtain_jwt_token),
    url(r'^rest_auth/registration/', include('rest_auth.registration.urls')),
    url(r'^rest_auth/registration/account-confirm-email/(?P<key>{0})/$'.format(regex),allauthemailconfirmation,name="account_confirm_email"),
]

if settings.DEBUG:
    # This allows the error pages to be debugged during development, just visit
    # these url in browser to see how these error pages look like.
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

    urlpatterns += [

        url(r'^400/$', default_views.bad_request, kwargs={'exception': Exception('Bad Request!')}),
        url(r'^403/$', default_views.permission_denied, kwargs={'exception': Exception('Permission Denied')}),
        url(r'^404/$', default_views.page_not_found, kwargs={'exception': Exception('Page not Found')}),
        url(r'^500/$', default_views.server_error),

    ]
    if 'debug_toolbar' in settings.INSTALLED_APPS:
        import debug_toolbar

        urlpatterns = [
                          url(r'^__debug__/', include(debug_toolbar.urls)),
                      ] + urlpatterns
