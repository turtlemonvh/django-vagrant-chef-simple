from django.conf import settings
from django.conf.urls.defaults import *
from django.views.generic.simple import direct_to_template
from django.contrib import admin

admin.autodiscover()

from tastypie.api import Api

from views import *
from apps.survey_browser.api import *

handler500 = "pinax.views.server_error"

urlpatterns = patterns("",
    url(r"^$", direct_to_template, {
        "template": "homepage.html",
    }, name="home"),
    url(r"^admin/", include(admin.site.urls)),
    
    # Link to url files for apps 
    url(r'^browser/', include('homesurvey.apps.survey_browser.urls')),
    
    # Account
    url(r'^accounts/login/$', 'django.contrib.auth.views.login', {'template_name': 'accounts/login.html'}, name="login"),
    url(r'^accounts/logout/$', 'views.logoff', name="logout"),
)

v1_api = Api(api_name='v1')
v1_api.register(UserResource())
v1_api.register(ParticipantFilterResource())
v1_api.register(ParticipantMetaFilterResource())
v1_api.register(ParticipantFilterGroupResource())


urlpatterns += patterns('',
    (r'^api/', include(v1_api.urls)),
)


if settings.SERVE_MEDIA:
    urlpatterns += patterns("",
        url(r"", include("staticfiles.urls")),
    )
