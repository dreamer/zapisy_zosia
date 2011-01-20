# -*- coding: UTF-8 -*-
from django.db import models
from datetime import datetime

class ZosiaDefinition(models.Model):
	active_definition			= models.BooleanField()
	registration_start			= models.DateTimeField()
	registration_final			= models.DateTimeField()
	lectures_suggesting_start	= models.DateTimeField()
	lectures_suggesting_final	= models.DateTimeField()
	rooming_start				= models.DateTimeField()
	rooming_final				= models.DateTimeField()

