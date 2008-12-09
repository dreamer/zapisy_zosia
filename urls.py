from django.conf.urls.defaults import *
from django.contrib import admin
import registration.views
import blog.views
import lectures.views
import rooms.views

admin.autodiscover()
urlpatterns = patterns('',
    # Example:
    # (r'^zapisy_zosia/', include('zapisy_zosia.foo.urls')),

     (r'^admin/(.*)', admin.site.root),

     (r'^register/$', registration.views.register),
     (r'^register/thanks/', registration.views.thanks),
     (r'^register/add_org/$', registration.views.add_organization), # TODO
     # (r'^register/recover/$', ), # TODO

     (r'^blog/$', blog.views.index),
     (r'^lectures/$', lectures.views.index),
     (r'^rooms/list/$', rooms.views.index),
)

