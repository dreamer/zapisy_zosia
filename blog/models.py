# -*- coding: UTF-8 -*-
from django.db import models

class BlogPost(models.Model):
    title = models.CharField(max_length=128)
    text = models.TextField(max_length=2048)

