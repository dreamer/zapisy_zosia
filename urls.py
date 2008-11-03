from django.conf.urls.defaults import *
from django.contrib import admin
import registration.views

admin.autodiscover()
urlpatterns = patterns('',
    # Example:
    # (r'^zapisy_zosia/', include('zapisy_zosia.foo.urls')),

    # Uncomment this for admin:
     (r'^admin/(.*)', admin.site.root),
     (r'^register/$', registration.views.register),
     (r'^register/thanks/', registration.views.thanks),
     (r'^register/add_org/$', registration.views.add_organization), # TODO
     # (r'^register/recover/$', ), # TODO
)

