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

     # admin related
     (r'^admin/(.*)', admin.site.root),

     # registration related
     (r'^register/$', registration.views.register),
     (r'^register/thanks/', registration.views.thanks),
     # (r'^register/add_org/$', registration.views.add_organization),
     (r'^register/activate/(?P<uidb36>[0-9A-Za-z]+)-(?P<token>.+)/$', registration.views.activate_user),

     # login / logout
     (r'^login/$', common.views.login_view),
     (r'^logout/$', common.views.logout_view),
     (r'^logout/bye/$', common.views.thanks),

     # apps main urls
     (r'^blog/$', blog.views.index),
     (r'^lectures/$', lectures.views.index),
     # temporarly disabled
     # (r'^rooms/$', rooms.views.index),

     # static media
     # note, that thid should be disabled for production code
     (r'^static_media/(?P<path>.*)$', 'django.views.static.serve',
        {'document_root': os.getcwd()+os.sep+'static_media', 'show_indexes': True}),

     # urls required for password change/reset
     (r'^password_change/$', common.views.password_change),
     (r'^password_change/done/$', common.views.password_change_done),

     (r'^password_reset/$', 
         'django.contrib.auth.views.password_reset',
         { 'template_name':'password_reset_form.html' }),
     (r'^password_reset/done/$', 
         'django.contrib.auth.views.password_reset_done',
         { 'template_name':'password_reset_done.html' }),
     (r'^reset/(?P<uidb36>[0-9A-Za-z]+)-(?P<token>.+)/$', 
         'django.contrib.auth.views.password_reset_confirm',
         { 'template_name':'password_reset_confirm.html' }),
     (r'^reset/done/$',
         'django.contrib.auth.views.password_reset_complete',
         { 'template_name':'password_reset_complete.html' }),
     
)

