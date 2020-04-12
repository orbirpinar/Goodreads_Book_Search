from django.db import models


class Books(models.Model):
	isbn = models.CharField(max_length=13)
	title = models.CharField(max_length=200)
	author = models.CharField(max_length = 50)
	year = models.IntegerField()

	def __str__(self):
		return self.title


