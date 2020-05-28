from django.db import models

# Create your models here.

class Guider(models.Model):
	target 		= models.CharField(max_length = 200)
	site 		= models.CharField(max_length = 3)
	obs_date 	= models.DateTimeField()
	image 		= models.FileField(upload_to = '%Y/%m/%d/')

	def __unicode__(self):
		return self.target
