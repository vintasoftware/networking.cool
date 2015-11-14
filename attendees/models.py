from django.db import models


class Atendee(models.Model):

	name = models.CharField(max_length=255)
	description = models.TextField(blank=True)

	linkedin_profile = models.TextField(blank=True)


class Concept(models.Model):
	atendee = models.ForeignKey(Atendee)

	label = models.CharField(max_length=255)
	score = models.DecimalField(max_digits=10, decimal_places=1)
