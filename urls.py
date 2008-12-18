import os
from django.conf.urls.defaults import *
from django.contrib import admin
import registration.views
import blog.views
import lectures.views
import rooms.views
import common.views
from blog.feeds import *

feeds = {
    'blog': LatestBlogEntries,
}

admin.autodiscover()

urlpatterns = patterns('',
    # Example:
    # (r'^zapisy_zosia/', include('zapisy_zosia.foo.urls')),

     # rss feed
     (r'^feeds/(?P<url>.*)/$', 'django.contrib.syndication.views.feed',
        {'feed_dict': feeds}),

     (r'^admin/(.*)', admin.site.root),

     (r'^register/$', registration.views.register),
     (r'^register/thanks/', registration.views.thanks),

     (r'^logout/$', common.views.logout_view),
     (r'^login/$', common.views.login_view),
     # (r'^register/add_org/$', registration.views.add_organization),
     (r'^register/recover/$', registration.views.recover),

     (r'^blog/$', blog.views.index),
     (r'^lectures/$', lectures.views.index),
     (r'^rooms/$', rooms.views.index),

     (r'^static_media/(?P<path>.*)$', 'django.views.static.serve',
        {'document_root': os.getcwd()+os.sep+'static_media', 'show_indexes': True}),
)

