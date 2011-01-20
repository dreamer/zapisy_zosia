# -*- coding: UTF-8 -*-
from django.contrib.syndication.feeds import Feed
from models import BlogPost

class LatestBlogEntries(Feed):
    title = "ZOSIA feed"
    link = "/blog/"
    description = "Updates on ZOSIA."

    def items(self):
        return BlogPost.objects.order_by('-pub_date')[:5]

