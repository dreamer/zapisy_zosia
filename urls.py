from django.conf.urls.defaults import *
from django.contrib import admin
import registration.views
import blog.views
import lectures.views
import rooms.views
import common.views

import os

admin.autodiscover()
urlpatterns = patterns('',
    # Example:
    # (r'^zapisy_zosia/', include('zapisy_zosia.foo.urls')),

     (r'^admin/(.*)', admin.site.root),

     (r'^register/$', registration.views.register),
     (r'^register/thanks/', registration.views.thanks),

     (r'^logout/$', common.views.logout),
     (r'^login/$', common.views.login),
     # (r'^register/add_org/$', registration.views.add_organization),
     # (r'^register/recover/$', ), # TODO

     (r'^blog/$', blog.views.index),
     (r'^lectures/$', lectures.views.index),
     (r'^rooms/$', rooms.views.index),

     (r'^static_media/(?P<path>.*)$', 'django.views.static.serve',
        {'document_root': os.getcwd()+os.sep+'static_media', 'show_indexes': True}),
)

