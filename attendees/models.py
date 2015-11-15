from django.db import models


class Attendee(models.Model):

    name = models.CharField(max_length=255)
    picture = models.TextField(blank=True)
    company = models.CharField(max_length=255, blank=True)
    description = models.TextField(blank=True)

    linkedin_profile = models.TextField(blank=True)

    def __unicode__(self):
        return self.name


class Concept(models.Model):
    attendee = models.ForeignKey(Attendee, related_name='concepts')

    label = models.CharField(max_length=255)
    score = models.DecimalField(max_digits=10, decimal_places=9)

    def __unicode__(self):
        return self.attendee.name + ' - ' + self.label + ' - ' + str(self.score)
