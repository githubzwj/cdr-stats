# -*- coding: utf-8 -*-
#
# CDR-Stats License
# http://www.cdr-stats.org
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.
#
# Copyright (C) 2011-2013 Star2Billing S.L.
#
# The Initial Developer of the Original Code is
# Arezqui Belaid <info@star2billing.com>
#
from django.conf.urls import handler404, handler500,\
    url, patterns, include
from django.conf import settings
from tastypie.api import Api
from api.user_api import UserResource
from api.switch_api import SwitchResource
from api.voip_rate_api import VoipRateResource
from api.voip_call import VoipCallResource
from cdr.urls import urlpatterns as urlpatterns_cdr
from cdr_alert.urls import urlpatterns as urlpatterns_cdr_alert
from user_profile.urls import urlpatterns as urlpatterns_user_profile
from frontend.urls import urlpatterns as urlpatterns_frontend
from voip_billing.urls import urlpatterns as urlpatterns_voip_billing
from api.api_playgrounds.urls import urlpatterns as urlpatterns_api_playgrounds
from frontend_notification.urls import urlpatterns as urlpatterns_frontend_notification
from django.contrib import admin
from dajaxice.core import dajaxice_autodiscover
import os
dajaxice_autodiscover()

try:
    admin.autodiscover()
except admin.sites.AlreadyRegistered:
    # nose imports the admin.py files during tests, so
    # the models have already been registered.
    pass

# tastypie api
tastypie_api = Api(api_name='v1')
tastypie_api.register(UserResource())
tastypie_api.register(SwitchResource())
tastypie_api.register(VoipRateResource())
tastypie_api.register(VoipCallResource())


urlpatterns = patterns('',

    # Uncomment the admin/doc line below and add 'django.contrib.admindocs'
    # to INSTALLED_APPS to enable admin documentation:
    #(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    (r'^admin/', include(admin.site.urls)),

    (r'^i18n/', include('django.conf.urls.i18n')),

    (r'^admin_tools/', include('admin_tools.urls')),

    (r'^api/', include(tastypie_api.urls)),

    # Serve static
    (r'^static/(?P<path>.*)$', 'django.views.static.serve',
        {'document_root': settings.STATIC_ROOT}),

    (r'^favicon\.ico$', 'django.views.generic.simple.redirect_to',
        {'url': 'static/cdr_stats/images/favicon.ico'}),

    (r'^%s/' % settings.DAJAXICE_MEDIA_PREFIX, include('dajaxice.urls')),
)


urlpatterns += urlpatterns_cdr
urlpatterns += urlpatterns_cdr_alert
urlpatterns += urlpatterns_user_profile
urlpatterns += urlpatterns_frontend
urlpatterns += urlpatterns_api_playgrounds
urlpatterns += urlpatterns_frontend_notification
urlpatterns += urlpatterns_voip_billing

urlpatterns += patterns('',
    url("", include('django_socketio.urls')),
)

urlpatterns += patterns('',
    (r'^%s/(?P<path>.*)$' % settings.MEDIA_URL.strip(os.sep),
     'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
)

handler404 = 'cdr_stats.urls.custom_404_view'
handler500 = 'cdr_stats.urls.custom_500_view'


def custom_404_view(request, template_name='404.html'):
    """404 error handler which includes ``request`` in the context.

    Templates: `404.html`
    Context: None
    """
    from django.template import Context, loader
    from django.http import HttpResponseServerError

    t = loader.get_template('404.html')  # Need to create a 404.html template.
    return HttpResponseServerError(t.render(Context({
        'request': request,
    })))


def custom_500_view(request, template_name='500.html'):
    """500 error handler which includes ``request`` in the context.

    Templates: `500.html`
    Context: None
    """
    from django.template import Context, loader
    from django.http import HttpResponseServerError

    t = loader.get_template('500.html')  # Need to create a 500.html template.
    return HttpResponseServerError(t.render(Context({
        'request': request,
    })))
