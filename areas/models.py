from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.postgres.fields import JSONField, ArrayField
from django.urls import reverse
from djgeojson.fields import PolygonField

from main.choices import AREATYPES

# user-created study area to constrain reconciliation
class Area(models.Model):
    # id (pk) auto-maintained, per Django
    owner = models.ForeignKey(settings.AUTH_USER_MODEL,
        related_name='areas', on_delete=models.CASCADE)
    type = models.CharField(max_length=20, choices=AREATYPES)
    title = models.CharField(max_length=255)
    description = models.CharField(max_length=2044)
    # ccodes = ArrayField(models.CharField(max_length=2))
    ccodes = ArrayField(models.CharField(max_length=2),blank=True, null=True)
    geom = JSONField(blank=True, null=True)
    # geom = PolygonField()

    def __str__(self):
        return str(self.id)

    def get_absolute_url(self):
        return reverse('areas:area-update', kwargs={'id': self.id})

    class Meta:
        managed = True
        db_table = 'areas'
        indexes = [
            # models.Index(fields=['', '']),
        ]
# user-created study area to constrain reconciliation
# class AreaL(models.Model):
#     # id (pk) auto-maintained, per Django
#     owner = models.ForeignKey(settings.AUTH_USER_MODEL,
#         related_name='areas', on_delete=models.CASCADE)
#     type = models.CharField(max_length=20, choices=AREATYPES)
#     title = models.CharField(max_length=255)
#     description = models.CharField(max_length=2044)
#     # ccodes = ArrayField(models.CharField(max_length=2))
#     ccodes = ArrayField(models.CharField(max_length=2),blank=True, null=True)
#     geom = JSONField(blank=True, null=True)
#     # geom = PolygonField()
#
#     def __str__(self):
#         return str(self.id)
#
#     def get_absolute_url(self):
#         return reverse('areas:area-update', kwargs={'id': self.id})
#
#     class Meta:
#         managed = True
#         db_table = 'areas'
#         indexes = [
#             # models.Index(fields=['', '']),
#         ]
